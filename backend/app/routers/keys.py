from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..auth import User as UserSchema, get_current_active_user
from ..services.key_analyzer import KeyAnalyzer

router = APIRouter(prefix="/keys", tags=["keys"])


@router.get("/recent")
async def get_recent_keys(
    current_user: UserSchema = Depends(get_current_active_user),
    start: Optional[int] = None,
    end: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    analyzer = KeyAnalyzer(db)
    return await analyzer.get_recent_keys(start_time=start, end_time=end)


@router.get("/high-score")
async def get_high_score_keys(
    current_user: UserSchema = Depends(get_current_active_user),
    start: Optional[int] = None,
    end: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    analyzer = KeyAnalyzer(db)
    return await analyzer.get_high_score_keys(start_time=start, end_time=end)
