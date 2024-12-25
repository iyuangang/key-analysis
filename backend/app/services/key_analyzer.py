import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Optional
from ..models import KeyInfo
from datetime import datetime, timedelta
from sqlalchemy import text, func, select
import pytz
import json
from ..config import current_config
from ..utils.debug import debug
from ..utils.redis import redis_client


class KeyAnalyzer:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.utc = pytz.UTC

    async def get_recent_keys(
        self, start_time: Optional[int] = None, end_time: Optional[int] = None
    ) -> List[Dict]:
        cache_key = f"recent_keys:{start_time}:{end_time}"
        cached_data = redis_client.get(cache_key)
        if cached_data:
            debug.log(f"Recent keys cache hit")
            return cached_data

        debug.log(f"Recent keys cache miss")
        debug.log(f"Getting recent keys for time range: {start_time} to {end_time}")

        # 如果没有指定时间范围，默认使用最近24小时
        if start_time is None or end_time is None:
            # 获取当前时间的 UTC 时间戳（毫秒）
            current_timestamp = int(datetime.now(self.utc).timestamp() * 1000)
            end_time = current_timestamp
            start_time = current_timestamp - 24 * 60 * 60 * 1000  # 24小时的毫秒数

        # 将毫秒时间戳转换为本地时间
        local_tz = pytz.timezone("Asia/Shanghai")
        end = datetime.fromtimestamp(end_time / 1000).astimezone(local_tz)
        start = datetime.fromtimestamp(start_time / 1000).astimezone(local_tz)

        # 转换为 UTC 时间
        # end = end.astimezone(self.utc)
        # start = start.astimezone(self.utc)

        # 移除时区信息以匹配数据库中的 naive datetime
        end = end.replace(tzinfo=None)
        start = start.replace(tzinfo=None)

        debug.log(f"Final time range - start: {start}, end: {end}")

        result = await self.db.execute(
            select(KeyInfo)
            .where(KeyInfo.created_at.between(start, end))
            .order_by(KeyInfo.id.desc())
            .limit(10)
        )
        results = result.scalars().all()
        debug.log(f"Found {len(results)} recent keys")
        formatted_results = [self._format_key_info(key) for key in results]
        redis_client.set(cache_key, formatted_results)
        return formatted_results

    async def get_high_score_keys(
        self, start_time: Optional[int] = None, end_time: Optional[int] = None
    ) -> List[Dict]:
        cache_key = f"high_score_keys:{start_time}:{end_time}"
        cached_data = redis_client.get(cache_key)
        if cached_data:
            debug.log(f"High score keys cache hit")
            return cached_data

        debug.log(f"High score keys cache miss")
        debug.log(f"Fetching high score keys from database")
        # 构建基本查询
        query = select(KeyInfo).where(KeyInfo.score > 400)

        # 添加时间范围过滤
        if start_time is not None and end_time is not None:
            # 将毫秒时间戳转换为本地时间
            local_tz = pytz.timezone("Asia/Shanghai")
            end = datetime.fromtimestamp(end_time / 1000).astimezone(local_tz)
            start = datetime.fromtimestamp(start_time / 1000).astimezone(local_tz)

            # 移除时区信息以匹配数据库中的 naive datetime
            end = end.replace(tzinfo=None)
            start = start.replace(tzinfo=None)

            debug.log(f"Using time range - start: {start}, end: {end}")
            query = query.where(KeyInfo.created_at.between(start, end))

        result = await self.db.execute(query.order_by(KeyInfo.score.desc()).limit(10))
        formatted_results = [
            self._format_key_info(key) for key in result.scalars().all()
        ]
        redis_client.set(cache_key, formatted_results)
        return formatted_results

    async def get_statistics(
        self, start_time: Optional[int] = None, end_time: Optional[int] = None
    ) -> Dict:
        cache_key = f"statistics:{start_time}:{end_time}"
        cached_data = redis_client.get(cache_key)
        if cached_data:
            debug.log(f"Statistics cache hit")
            return cached_data

        debug.log(f"Statistics cache miss")
        debug.log(f"Getting statistics for time range: {start_time} to {end_time}")

        # 确定时间范围
        if start_time is None or end_time is None:
            # 获取当前时间的 UTC 时间戳（毫秒）
            current_timestamp = int(datetime.now(self.utc).timestamp() * 1000)
            end_time = current_timestamp
            start_time = current_timestamp - 24 * 60 * 60 * 1000  # 24小时的毫秒数

        # 将毫秒时间戳转换为本地时间
        local_tz = pytz.timezone("Asia/Shanghai")
        end = datetime.fromtimestamp(end_time / 1000).astimezone(local_tz)
        start = datetime.fromtimestamp(start_time / 1000).astimezone(local_tz)

        # 移除时区信息以匹配数据库中的 naive datetime
        end = end.replace(tzinfo=None)
        start = start.replace(tzinfo=None)

        debug.log(f"Final time range - start: {start}, end: {end}")

        # 获取当前时间段的数据
        current_query = select(KeyInfo).where(KeyInfo.created_at.between(start, end))
        result = await self.db.execute(current_query)
        current_df = pd.DataFrame(
            [
                {
                    "id": row.id,
                    "created_at": row.created_at,  # 数据库返回的是 naive 时间
                    "fingerprint": row.fingerprint,
                    "repeat_letter_score": row.repeat_letter_score,
                    "increasing_letter_score": row.increasing_letter_score,
                    "decreasing_letter_score": row.decreasing_letter_score,
                    "magic_letter_score": row.magic_letter_score,
                    "score": row.score,
                    "unique_letters_count": row.unique_letters_count,
                }
                for row in result.scalars().all()
            ]
        )
        debug.log(f"Current period records: {len(current_df)}")

        # 使用正确的数据集进行统计
        df = current_df if start_time is None or end_time is None else current_df
        if df.empty:
            debug.log("Warning: No data available for the selected period")
            # 返回空的统计数据结构
            return {
                "score_distribution": {
                    "histogram": [],
                    "bins": [],
                    "mean": 0,
                    "median": 0,
                    "std": 0,
                    "min": 0,
                    "max": 0,
                    "q1": 0,
                    "q3": 0,
                    "total_count": 0,
                    "qualified_count": 0,
                },
                "correlation_matrix": {},
                "summary_stats": {
                    "score": {
                        "mean": 0,
                        "max": 0,
                        "count": 0,
                        "qualified_rate": 0,
                        "mean_trend": 0,
                        "max_trend": 0,
                        "count_trend": 0,
                        "qualified_trend": 0,
                    }
                },
                "score_types_stats": {},
                "trends": {
                    "time_format": "YYYY-MM-DD HH:mm",
                    "avg_scores": [],
                    "max_scores": [],
                    "counts": [],
                },
            }

        # 确保DataFrame中的时间戳使用UTC时区
        df["created_at"] = pd.to_datetime(df["created_at"]).dt.tz_convert("UTC")

        # 分离数值列用于相关性分析
        numeric_columns = [
            "repeat_letter_score",
            "increasing_letter_score",
            "decreasing_letter_score",
            "magic_letter_score",
            "score",
            "unique_letters_count",
        ]
        numeric_df = df[numeric_columns]

        # 计算趋势数据
        def safe_calc(series, func):
            try:
                result = func(series)
                # 处理无穷大和 NaN 值
                if pd.isna(result) or np.isinf(result):
                    return 0.0
                return float(result)
            except:
                return 0.0

        # 使用正确的数据集计算统计数据
        stats_df = current_df if start_time is None or end_time is None else current_df
        current_stats = {
            "mean": safe_calc(stats_df["score"], lambda x: x.mean()),
            "max": safe_calc(stats_df["score"], lambda x: x.max()),
            "count": len(stats_df),
            "qualified_rate": (
                len(stats_df[stats_df["score"] > 400]) / max(len(stats_df), 1)
            ),
        }

        # 计算上一个时间段的数据
        if start_time is not None and end_time is not None:
            time_delta = end - start
            previous_start = start - time_delta
            previous_end = start
            previous_query = select(KeyInfo).where(
                KeyInfo.created_at.between(previous_start, previous_end)
            )
            result = await self.db.execute(previous_query)
            previous_df = pd.DataFrame(
                [
                    {
                        "id": row.id,
                        "created_at": row.created_at,
                        "fingerprint": row.fingerprint,
                        "repeat_letter_score": row.repeat_letter_score,
                        "increasing_letter_score": row.increasing_letter_score,
                        "decreasing_letter_score": row.decreasing_letter_score,
                        "magic_letter_score": row.magic_letter_score,
                        "score": row.score,
                        "unique_letters_count": row.unique_letters_count,
                    }
                    for row in result.scalars().all()
                ]
            )
        else:
            # 如果是全部数据使用同样的数据作为对比
            previous_df = current_df

        # 对数据使用前一时间段或全部历史数据
        compare_df = (
            previous_df
            if start_time is not None and end_time is not None
            else current_df
        )
        previous_stats = {
            "mean": safe_calc(compare_df["score"], lambda x: x.mean()),
            "max": safe_calc(compare_df["score"], lambda x: x.max()),
            "count": len(compare_df),
            "qualified_rate": (
                len(compare_df[compare_df["score"] > 400]) / max(len(compare_df), 1)
            ),
        }

        # 计算趋势变化
        def calculate_trend(current: float, previous: float) -> float:
            if previous == 0:
                return 0 if current == 0 else 1
            try:
                trend = (current - previous) / previous
                # 处理无穷大和 NaN 值
                if pd.isna(trend) or np.isinf(trend):
                    return 0.0
                # 限制趋势值的范围
                return max(min(float(trend), 10.0), -10.0)
            except:
                return 0.0

        summary_stats = {
            "score": {
                "mean": round(float(current_stats["mean"]), 1),
                "max": round(float(current_stats["max"]), 1),
                "count": int(current_stats["count"]),
                "qualified_rate": float(current_stats["qualified_rate"]),
                "mean_trend": calculate_trend(
                    current_stats["mean"], previous_stats["mean"]
                ),
                "max_trend": calculate_trend(
                    current_stats["max"], previous_stats["max"]
                ),
                "count_trend": calculate_trend(
                    current_stats["count"], previous_stats["count"]
                ),
                "qualified_trend": calculate_trend(
                    current_stats["qualified_rate"], previous_stats["qualified_rate"]
                ),
            }
        }

        # 确保数据时区一致
        df["created_at"] = pd.to_datetime(df["created_at"])
        if df["created_at"].dt.tz is None:
            local_tz = pytz.timezone("Asia/Shanghai")
            df["created_at"] = df["created_at"].apply(lambda x: local_tz.localize(x))

        # 生成时间序列数据
        # 使用传入的时间范围，并调整到整点
        end_time = end.replace(minute=0, second=0, microsecond=0)
        start_time = start.replace(minute=0, second=0, microsecond=0)

        # 确定时间频率
        time_delta = end_time - start_time
        if time_delta.days > 30:
            freq = "D"  # 按天统计
        elif time_delta.days > 7:
            freq = "6h"  # 按6小时统计
        else:
            freq = "h"  # 按小时统计

        # 生成时间序列数据
        hourly_stats = (
            df.groupby(pd.Grouper(key="created_at", freq=freq))
            .agg({"score": ["mean", "max", "count"]})
            .fillna(0)
        )  # 填充缺失值

        # 格式化趋势数据
        time_format = "%Y-%m-%d %H:%M" if freq in ["h", "6h"] else "%Y-%m-%d"
        trends = {
            "time_format": "YYYY-MM-DD HH:mm" if freq in ["h", "6h"] else "YYYY-MM-DD",
            "avg_scores": [
                {
                    "time": idx.tz_localize(None).strftime(time_format),
                    "value": round(float(row[("score", "mean")]), 2),
                }
                for idx, row in hourly_stats.iterrows()
                if not pd.isna(row[("score", "mean")])
            ],
            "max_scores": [
                {
                    "time": idx.tz_localize(None).strftime(time_format),
                    "value": round(float(row[("score", "max")]), 2),
                }
                for idx, row in hourly_stats.iterrows()
                if not pd.isna(row[("score", "max")])
            ],
            "counts": [
                {
                    "time": idx.tz_localize(None).strftime(time_format),
                    "value": int(row[("score", "count")]),
                }
                for idx, row in hourly_stats.iterrows()
                if not pd.isna(row[("score", "count")])
            ],
        }

        debug.log("\nFormatted Trends Data:")
        debug.log(json.dumps(trends, indent=2))

        result = {
            "score_distribution": self._get_score_distribution(df),
            "correlation_matrix": self._get_correlation_matrix(numeric_df),
            "summary_stats": summary_stats,
            "score_types_stats": self._get_score_types_stats(df),
            "trends": trends,
        }
        redis_client.set(cache_key, result)
        return result

    def _format_key_info(self, key: KeyInfo) -> Dict:
        # 数据库返回的是 naive 时间，需要先添加本地时区信息
        created_at = key.created_at if key.created_at else datetime.now()
        if created_at.tzinfo is None:
            local_tz = pytz.timezone("Asia/Shanghai")
            created_at = local_tz.localize(created_at)
        return {
            "created_at": created_at.strftime("%Y-%m-%d %H:%M"),
            "fingerprint": key.fingerprint.upper()[24:40] if key.fingerprint else "N/A",
            "score": key.score or 0,
            "unique_letters_count": key.unique_letters_count or 0,
        }

    def _get_score_distribution(self, df: pd.DataFrame) -> Dict:
        scores = df["score"].values
        hist, bins = np.histogram(scores, bins=20)

        # 计算基本统计量
        def safe_stat(func, default=0.0):
            try:
                value = float(func())
                return default if pd.isna(value) or np.isinf(value) else value
            except:
                return default

        stats = {
            "mean": safe_stat(lambda: np.mean(scores)),
            "median": safe_stat(lambda: np.median(scores)),
            "std": safe_stat(lambda: np.std(scores)),
            "min": safe_stat(lambda: np.min(scores)),
            "max": safe_stat(lambda: np.max(scores)),
            "q1": safe_stat(lambda: np.percentile(scores, 25)),
            "q3": safe_stat(lambda: np.percentile(scores, 75)),
        }

        return {
            "histogram": hist.tolist(),
            "bins": bins.tolist(),
            **stats,
            "total_count": len(scores),
            "qualified_count": int(np.sum(scores > 400)),
        }

    @staticmethod
    def _get_correlation_matrix(df: pd.DataFrame) -> Dict:
        """计算相关性矩阵，只处理数值列"""
        corr_matrix = df.fillna(0).corr().round(3)
        # 处理无穷大和 NaN 值
        corr_matrix = corr_matrix.replace([np.inf, -np.inf], 0)
        corr_matrix = corr_matrix.fillna(0)
        return corr_matrix.to_dict()

    @staticmethod
    def _get_score_types_stats(df: pd.DataFrame) -> Dict:
        score_columns = [
            "repeat_letter_score",
            "increasing_letter_score",
            "decreasing_letter_score",
            "magic_letter_score",
        ]
        stats = df[score_columns].fillna(0).describe()
        # 处理无穷大和 NaN 值
        stats = stats.replace([np.inf, -np.inf], 0)
        stats = stats.fillna(0)
        return stats.to_dict()
