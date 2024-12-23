import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from ..models import KeyInfo
from datetime import datetime, timedelta
from sqlalchemy import text, func
import pytz
import json


class KeyAnalyzer:
    def __init__(self, db: Session):
        self.db = db
        self.utc = pytz.UTC

    def get_recent_keys(
        self, start_time: Optional[int] = None, end_time: Optional[int] = None
    ) -> List[Dict]:
        # 如果没有指定时间范围，默认使用最近24小时
        if start_time is None or end_time is None:
            end = datetime.now(self.utc)
            start = end - timedelta(days=1)
        else:
            start = datetime.fromtimestamp(start_time / 1000, self.utc)
            end = datetime.fromtimestamp(end_time / 1000, self.utc)

        query = (
            self.db.query(KeyInfo)
            .filter(KeyInfo.created_at.between(start, end))
            .order_by(KeyInfo.id.desc())
            .limit(10)
        )
        return [self._format_key_info(key) for key in query.all()]

    def get_high_score_keys(
        self, start_time: Optional[int] = None, end_time: Optional[int] = None
    ) -> List[Dict]:
        # 构建基础查询
        query = self.db.query(KeyInfo).filter(KeyInfo.score > 400)

        # 添加时间范围过滤
        if start_time is not None and end_time is not None:
            start = datetime.fromtimestamp(start_time / 1000, self.utc)
            end = datetime.fromtimestamp(end_time / 1000, self.utc)
            query = query.filter(KeyInfo.created_at.between(start, end))

        query = query.order_by(KeyInfo.score.desc()).limit(10)
        return [self._format_key_info(key) for key in query.all()]

    def get_statistics(
        self, start_time: Optional[int] = None, end_time: Optional[int] = None
    ) -> Dict:
        # 获取所有数据
        all_data_query = self.db.query(KeyInfo)
        all_df = pd.read_sql(all_data_query.statement, self.db.bind)

        # 确定时间范围
        if start_time is None or end_time is None:
            end = datetime.now(self.utc)
            start = end - timedelta(days=1)
        else:
            start = datetime.fromtimestamp(start_time / 1000, self.utc)
            end = datetime.fromtimestamp(end_time / 1000, self.utc)

        # 获取当前时间段的数据
        current_query = self.db.query(KeyInfo).filter(
            KeyInfo.created_at.between(start, end)
        )
        current_df = pd.read_sql(current_query.statement, self.db.bind)

        # 获取上一个时间段的数据
        if start_time is None or end_time is None:
            # 默认情况下，对比前一天
            previous_start = start - timedelta(days=1)
            previous_end = start
        else:
            # 自定义时间范围，使用相同长度的前一个时间段
            time_delta = end - start
            previous_start = start - time_delta
            previous_end = start

        previous_query = self.db.query(KeyInfo).filter(
            KeyInfo.created_at.between(previous_start, previous_end)
        )
        previous_df = pd.read_sql(previous_query.statement, self.db.bind)

        # 使用正确的数据集进行统计
        df = all_df if start_time is None or end_time is None else current_df

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

        # 对比数据使用前一个时间段或全部历史数据
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
            freq = "D"  # 超过7天使用天为单位
        elif time_delta.days > 2:
            freq = "6H"  # 2-7天使用6小时为单位
        else:
            freq = "H"  # 2天内使用小时为单位

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

        # 调试信息
        print("\nTime Range:")
        print(f"Start: {start_time}")
        print(f"End: {end_time}")
        print(f"Time Delta: {time_delta}")
        print(f"Sample Frequency: {freq}")
        print("\nOriginal Data Sample:")
        print(df["created_at"].head())
        print("\nHourly Stats Sample:")
        print(hourly_stats.head())

        # 格式化趋势数据
        time_format = "%Y-%m-%d %H:%M" if freq in ["H", "6H"] else "%Y-%m-%d"
        trends = {
            "time_format": "YYYY-MM-DD HH:mm" if freq in ["H", "6H"] else "YYYY-MM-DD",
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

        print("\nFormatted Trends Data:")
        print(json.dumps(trends, indent=2))

        return {
            "score_distribution": self._get_score_distribution(df),
            "correlation_matrix": self._get_correlation_matrix(numeric_df),
            "summary_stats": summary_stats,
            "score_types_stats": self._get_score_types_stats(df),
            "trends": trends,
        }

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
