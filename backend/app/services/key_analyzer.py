import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Optional, Any, Tuple
from ..models import KeyInfo
from datetime import datetime, timedelta
from sqlalchemy import select
import pytz
import json
from ..utils.debug import debug
from ..utils.redis import redis_client


class TimeRange:
    def __init__(self, start: datetime, end: datetime):
        self.start = start
        self.end = end

    @classmethod
    def from_timestamps(cls, start_ms: Optional[int], end_ms: Optional[int]) -> 'TimeRange':
        utc = pytz.UTC
        if start_ms is None or end_ms is None:
            return cls(None, None)

        local_tz = pytz.timezone("Asia/Shanghai")
        end = datetime.fromtimestamp(end_ms / 1000).astimezone(local_tz)
        start = datetime.fromtimestamp(start_ms / 1000).astimezone(local_tz)
        
        return cls(start.replace(tzinfo=None), end.replace(tzinfo=None))


class StatisticsCalculator:
    NUMERIC_COLUMNS = [
        "repeat_letter_score",
        "increasing_letter_score",
        "decreasing_letter_score",
        "magic_letter_score",
        "score",
        "unique_letters_count",
    ]
    
    SCORE_COLUMNS = [
        "repeat_letter_score",
        "increasing_letter_score",
        "decreasing_letter_score",
        "magic_letter_score",
    ]

    @staticmethod
    def safe_calc(series: pd.Series, func: callable, default: float = 0.0) -> float:
        try:
            result = func(series)
            return default if pd.isna(result) or np.isinf(result) else float(result)
        except:
            return default

    @staticmethod
    def calculate_trend(current: float, previous: float) -> float:
        if previous == 0:
            return 0 if current == 0 else 1
        try:
            trend = (current - previous) / previous
            if pd.isna(trend) or np.isinf(trend):
                return 0.0
            return max(min(float(trend), 10.0), -10.0)
        except:
            return 0.0

    @classmethod
    def get_score_distribution(cls, df: pd.DataFrame) -> Dict:
        scores = df["score"].values
        hist, bins = np.histogram(scores, bins=20)

        stats = {
            "mean": cls.safe_calc(scores, np.mean),
            "median": cls.safe_calc(scores, np.median),
            "std": cls.safe_calc(scores, np.std),
            "min": cls.safe_calc(scores, np.min),
            "max": cls.safe_calc(scores, np.max),
            "q1": cls.safe_calc(scores, lambda x: np.percentile(x, 25)),
            "q3": cls.safe_calc(scores, lambda x: np.percentile(x, 75)),
        }

        return {
            "histogram": hist.tolist(),
            "bins": bins.tolist(),
            **stats,
            "total_count": len(scores),
            "qualified_count": int(np.sum(scores > 400)),
        }

    @classmethod
    def get_correlation_matrix(cls, df: pd.DataFrame) -> Dict:
        corr_matrix = df.fillna(0).corr().round(3)
        corr_matrix = corr_matrix.replace([np.inf, -np.inf], 0).fillna(0)
        return corr_matrix.to_dict()

    @classmethod
    def get_score_types_stats(cls, df: pd.DataFrame) -> Dict:
        stats = df[cls.SCORE_COLUMNS].fillna(0).describe()
        return stats.replace([np.inf, -np.inf], 0).fillna(0).to_dict()


class KeyAnalyzer:
    CACHE_EXPIRY = 300  # 5 minutes
    HIGH_SCORE_THRESHOLD = 400
    DEFAULT_LIMIT = 10

    def __init__(self, db: AsyncSession):
        self.db = db
        self.utc = pytz.UTC

    def _format_key_info(self, key: KeyInfo) -> Dict:
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

    async def get_recent_keys(
        self, start_time: Optional[int] = None, end_time: Optional[int] = None
    ) -> List[Dict]:
        cache_key = f"recent_keys:{start_time}:{end_time}"
        if cached_data := redis_client.get(cache_key):
            debug.log("Recent keys cache hit")
            return cached_data

        debug.log(f"Recent keys cache miss")
        time_range = TimeRange.from_timestamps(start_time, end_time)
        
        query = select(KeyInfo).order_by(KeyInfo.id.desc())
        if time_range.start is not None and time_range.end is not None:
            query = query.where(KeyInfo.created_at.between(time_range.start, time_range.end))
        
        result = await self.db.execute(query.limit(self.DEFAULT_LIMIT))
        formatted_results = [self._format_key_info(key) for key in result.scalars().all()]
        redis_client.set(cache_key, formatted_results, ttl=self.CACHE_EXPIRY)
        return formatted_results

    async def get_high_score_keys(
        self, start_time: Optional[int] = None, end_time: Optional[int] = None
    ) -> List[Dict]:
        cache_key = f"high_score_keys:{start_time}:{end_time}"
        if cached_data := redis_client.get(cache_key):
            debug.log("High score keys cache hit")
            return cached_data

        debug.log("High score keys cache miss")
        query = select(KeyInfo).where(KeyInfo.score > self.HIGH_SCORE_THRESHOLD)

        time_range = TimeRange.from_timestamps(start_time, end_time)
        if time_range.start is not None and time_range.end is not None:
            query = query.where(KeyInfo.created_at.between(time_range.start, time_range.end))

        result = await self.db.execute(query.order_by(KeyInfo.score.desc()).limit(self.DEFAULT_LIMIT))
        formatted_results = [self._format_key_info(key) for key in result.scalars().all()]
        redis_client.set(cache_key, formatted_results, ttl=self.CACHE_EXPIRY)
        return formatted_results

    async def _get_dataframe(self, time_range: TimeRange) -> Tuple[pd.DataFrame, pd.DataFrame]:
        current_query = select(KeyInfo)
        if time_range.start is not None and time_range.end is not None:
            current_query = current_query.where(
                KeyInfo.created_at.between(time_range.start, time_range.end)
            )
        result = await self.db.execute(current_query)
        
        current_df = pd.DataFrame([{
                    "id": row.id,
            "created_at": row.created_at,
                    "fingerprint": row.fingerprint,
                    "repeat_letter_score": row.repeat_letter_score,
                    "increasing_letter_score": row.increasing_letter_score,
                    "decreasing_letter_score": row.decreasing_letter_score,
                    "magic_letter_score": row.magic_letter_score,
                    "score": row.score,
                    "unique_letters_count": row.unique_letters_count,
        } for row in result.scalars().all()])

        if current_df.empty:
            return current_df, current_df

        if time_range.start is not None and time_range.end is not None:
            previous_start = time_range.start - (time_range.end - time_range.start)
            previous_query = select(KeyInfo).where(
                KeyInfo.created_at.between(previous_start, time_range.start)
            )
            result = await self.db.execute(previous_query)
            previous_df = pd.DataFrame([{
                        "id": row.id,
                        "created_at": row.created_at,
                        "fingerprint": row.fingerprint,
                        "repeat_letter_score": row.repeat_letter_score,
                        "increasing_letter_score": row.increasing_letter_score,
                        "decreasing_letter_score": row.decreasing_letter_score,
                        "magic_letter_score": row.magic_letter_score,
                        "score": row.score,
                        "unique_letters_count": row.unique_letters_count,
            } for row in result.scalars().all()])
        else:
            previous_df = current_df

        return current_df, previous_df

    def _calculate_trends(self, df: pd.DataFrame, time_range: TimeRange) -> Dict[str, Any]:
        local_tz = pytz.timezone("Asia/Shanghai")

        if time_range.start is None or time_range.end is None:
            if df.empty:
                return {
                    "time_format": "YYYY-MM-DD HH:mm",
                    "avg_scores": [],
                    "max_scores": [],
                    "counts": [],
                }
            
            df["created_at"] = pd.to_datetime(df["created_at"])
            start_time = df["created_at"].min()
            end_time = df["created_at"].max()
        else:
            end_time = time_range.end.replace(minute=0, second=0, microsecond=0)
            start_time = time_range.start.replace(minute=0, second=0, microsecond=0)
            
            end_time = local_tz.localize(end_time)
            start_time = local_tz.localize(start_time)
        
        time_delta = end_time - start_time

        freq = "D" if time_delta.days > 30 else "6h" if time_delta.days > 7 else "h"
        time_format = "%Y-%m-%d %H:%M" if freq in ["h", "6h"] else "%Y-%m-%d"

        df["created_at"] = pd.to_datetime(df["created_at"])
        if df["created_at"].dt.tz is None:
            df["created_at"] = df["created_at"].apply(lambda x: local_tz.localize(x))
        else:
            df["created_at"] = df["created_at"].dt.tz_convert(local_tz)

        df = df.set_index("created_at")
        hourly_stats = (
            df.groupby(pd.Grouper(freq=freq))
            .agg({"score": ["mean", "max", "count"]})
            .fillna(0)
        )

        return {
            "time_format": f"YYYY-MM-DD HH:mm" if freq in ["h", "6h"] else "YYYY-MM-DD",
            "avg_scores": [
                {
                    "time": idx.strftime(time_format),
                    "value": round(float(row[("score", "mean")]), 2)
                }
                for idx, row in hourly_stats.iterrows()
                if not pd.isna(row[("score", "mean")])
            ],
            "max_scores": [
                {
                    "time": idx.strftime(time_format),
                    "value": round(float(row[("score", "max")]), 2)
                }
                for idx, row in hourly_stats.iterrows()
                if not pd.isna(row[("score", "max")])
            ],
            "counts": [
                {
                    "time": idx.strftime(time_format),
                    "value": int(row[("score", "count")])
                }
                for idx, row in hourly_stats.iterrows()
                if not pd.isna(row[("score", "count")])
            ]
        }

    async def get_statistics(
        self, start_time: Optional[int] = None, end_time: Optional[int] = None
    ) -> Dict[str, Any]:
        cache_key = f"statistics:{start_time}:{end_time}"
        if cached_data := redis_client.get(cache_key):
            debug.log("Statistics cache hit")
            return cached_data

        debug.log("Statistics cache miss")
        time_range = TimeRange.from_timestamps(start_time, end_time)
        current_df, previous_df = await self._get_dataframe(time_range)

        if current_df.empty:
            return self._get_empty_statistics()

        current_stats = {
            "mean": StatisticsCalculator.safe_calc(current_df["score"], lambda x: x.mean()),
            "max": StatisticsCalculator.safe_calc(current_df["score"], lambda x: x.max()),
            "count": len(current_df),
            "qualified_rate": len(current_df[current_df["score"] > self.HIGH_SCORE_THRESHOLD]) / max(len(current_df), 1),
        }

        previous_stats = {
            "mean": StatisticsCalculator.safe_calc(previous_df["score"], lambda x: x.mean()),
            "max": StatisticsCalculator.safe_calc(previous_df["score"], lambda x: x.max()),
            "count": len(previous_df),
            "qualified_rate": len(previous_df[previous_df["score"] > self.HIGH_SCORE_THRESHOLD]) / max(len(previous_df), 1),
        }

        summary_stats = {
            "score": {
                "mean": round(float(current_stats["mean"]), 1),
                "max": round(float(current_stats["max"]), 1),
                "count": int(current_stats["count"]),
                "qualified_rate": float(current_stats["qualified_rate"]),
                "mean_trend": StatisticsCalculator.calculate_trend(
                    current_stats["mean"], previous_stats["mean"]
                ),
                "max_trend": StatisticsCalculator.calculate_trend(
                    current_stats["max"], previous_stats["max"]
                ),
                "count_trend": StatisticsCalculator.calculate_trend(
                    current_stats["count"], previous_stats["count"]
                ),
                "qualified_trend": StatisticsCalculator.calculate_trend(
                    current_stats["qualified_rate"], previous_stats["qualified_rate"]
                ),
            }
        }

        numeric_df = current_df[StatisticsCalculator.NUMERIC_COLUMNS]
        result = {
            "score_distribution": StatisticsCalculator.get_score_distribution(current_df),
            "correlation_matrix": StatisticsCalculator.get_correlation_matrix(numeric_df),
            "summary_stats": summary_stats,
            "score_types_stats": StatisticsCalculator.get_score_types_stats(current_df),
            "trends": self._calculate_trends(current_df, time_range),
        }

        redis_client.set(cache_key, result, ttl=self.CACHE_EXPIRY)
        return result

    def _get_empty_statistics(self) -> Dict[str, Any]:
        return {
            "score_distribution": {
                "histogram": [], "bins": [], "mean": 0, "median": 0,
                "std": 0, "min": 0, "max": 0, "q1": 0, "q3": 0,
                "total_count": 0, "qualified_count": 0,
            },
            "correlation_matrix": {},
            "summary_stats": {
                "score": {
                    "mean": 0, "max": 0, "count": 0, "qualified_rate": 0,
                    "mean_trend": 0, "max_trend": 0, "count_trend": 0, "qualified_trend": 0,
                }
            },
            "score_types_stats": {},
            "trends": {
                "time_format": "YYYY-MM-DD HH:mm",
                "avg_scores": [], "max_scores": [], "counts": [],
            },
        }
