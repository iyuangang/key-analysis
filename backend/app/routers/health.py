from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils.redis import redis_client

router = APIRouter()


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    health = {"status": "healthy", "database": "up", "redis": "up", "details": {}}

    try:
        # 检查数据库连接
        await db.execute("SELECT 1")
    except Exception as e:
        health["status"] = "unhealthy"
        health["database"] = "down"
        health["details"]["database_error"] = str(e)

    try:
        # 检查Redis连接
        redis_client.client.ping()
    except Exception as e:
        health["status"] = "unhealthy"
        health["redis"] = "down"
        health["details"]["redis_error"] = str(e)

    return health
