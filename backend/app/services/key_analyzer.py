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
            end = datetime.now(self.utc)
            start = end - timedelta(days=1)
        else:
            start = datetime.fromtimestamp(start_time / 1000, self.utc)
            end = datetime.fromtimestamp(end_time / 1000, self.utc)

        debug.log(f"Processed time range: {start} to {end}")
        # 转换为 naive datetime 用于数据库查询
        start = start.replace(tzinfo=None)
        end = end.replace(tzinfo=None)

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
            start = datetime.fromtimestamp(start_time / 1000, self.utc)
            end = datetime.fromtimestamp(end_time / 1000, self.utc)
            # 转换为 naive datetime
            start = start.replace(tzinfo=None)
            end = end.replace(tzinfo=None)
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
        # 获取所有数据
        all_data_query = select(KeyInfo)
        result = await self.db.execute(all_data_query)
        all_df = pd.DataFrame(
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
        debug.log(f"Total records: {len(all_df)}")

        # 确定时间范围
        if start_time is None or end_time is None:
            end = datetime.now(self.utc)
            start = end - timedelta(days=1)
        else:
            start = datetime.fromtimestamp(start_time / 1000, self.utc)
            end = datetime.fromtimestamp(end_time / 1000, self.utc)

        # 转换为 naive datetime
        start = start.replace(tzinfo=None)
        end = end.replace(tzinfo=None)

        debug.log(f"Processed time range: {start} to {end}")

        # 获取当前时间段的数据
        current_query = select(KeyInfo).where(KeyInfo.created_at.between(start, end))
        result = await self.db.execute(current_query)
        current_df = pd.DataFrame(
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
        debug.log(f"Current period records: {len(current_df)}")

        # 使用正确的数据集进行统计
        df = all_df if start_time is None or end_time is None else current_df
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
        stats_df = all_df if start_time is None or end_time is None else current_df
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
            previous_df = all_df

        # 对数据使用前一个时间段或全部历史数据
        compare_df = (
            previous_df if start_time is not None and end_time is not None else all_df
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
                return float(trend)
            except:
                return 0.0

        summary_stats = {
            "score": {
                "mean": round(current_stats["mean"], 1),
                "max": round(current_stats["max"], 1),
                "count": current_stats["count"],
                "qualified_rate": current_stats["qualified_rate"],
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

        # 生成时间序列数据
        # 使用传入的时间范围，并调整到整点
        end_time = end.replace(minute=0, second=0, microsecond=0)
        start_time = start.replace(minute=0, second=0, microsecond=0)

        # 创建时间索引
        # 根据时间范围长度调整采样频率
        time_delta = end_time - start_time
        if time_delta.days > 7:
            freq = "D"  # 过7天使用天为单位
        elif time_delta.days > 2:
            freq = "6h"  # 2-7天使用6小时为单位
        else:
            freq = "h"  # 2天内使用小时为单位

        time_index = pd.date_range(
            start=start_time, end=end_time, freq=freq, tz=self.utc
        )

        # 确保数据时区一致
        df["created_at"] = pd.to_datetime(df["created_at"])
        if df["created_at"].dt.tz is None:
            df["created_at"] = df["created_at"].dt.tz_localize(self.utc)
        else:
            df["created_at"] = df["created_at"].dt.tz_convert(self.utc)

        # 重采样数据
        hourly_stats = (
            df.set_index("created_at")
            .resample(freq)
            .agg({"score": ["mean", "max", "count"]})
            .fillna(0)
        )

        # 确保有完整的数据
        hourly_stats = hourly_stats.reindex(time_index, fill_value=0)

        # 仅在调试模式下输出辅助信息
        debug.log("\nTime Range:")
        debug.log(f"Start: {start_time}")
        debug.log(f"End: {end_time}")
        debug.log(f"Time Delta: {time_delta}")
        debug.log(f"Sample Frequency: {freq}")
        debug.log("\nOriginal Data Sample:")
        debug.log(df["created_at"].head())
        debug.log("\nHourly Stats Sample:")
        debug.log(hourly_stats.head())

        # 格式化趋势数据
        time_format = "%Y-%m-%d %H:%M" if freq in ["h", "6h"] else "%Y-%m-%d"
        trends = {
            "time_format": "YYYY-MM-DD HH:mm" if freq in ["h", "6h"] else "YYYY-MM-DD",
            "avg_scores": [
                {
                    "time": idx.strftime(time_format),
                    "value": round(float(row[("score", "mean")]), 2),
                }
                for idx, row in hourly_stats.iterrows()
            ],
            "max_scores": [
                {
                    "time": idx.strftime(time_format),
                    "value": round(float(row[("score", "max")]), 2),
                }
                for idx, row in hourly_stats.iterrows()
            ],
            "counts": [
                {
                    "time": idx.strftime(time_format),
                    "value": int(row[("score", "count")]),
                }
                for idx, row in hourly_stats.iterrows()
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
        return {
            "created_at": (
                key.created_at.strftime("%Y-%m-%d %H:%M")
                if key.created_at
                else datetime.now().strftime("%Y-%m-%d %H:%M")
            ),
            "fingerprint": (
                key.fingerprint.upper()[24:40] if key.fingerprint else "N/A"
            ),
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
