from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..auth import User as UserSchema, get_current_active_user
from ..services.key_analyzer import KeyAnalyzer

router = APIRouter(tags=["statistics"])


@router.get("/statistics")
async def get_statistics(
    current_user: UserSchema = Depends(get_current_active_user),
    start: Optional[int] = None,
    end: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    analyzer = KeyAnalyzer(db)
    return await analyzer.get_statistics(start_time=start, end_time=end)
