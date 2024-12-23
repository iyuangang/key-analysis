from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import get_db, config
from .services.key_analyzer import KeyAnalyzer
from typing import Optional

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config["cors"]["origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/keys/recent")
async def get_recent_keys(
    start: Optional[int] = None,
    end: Optional[int] = None,
    db: Session = Depends(get_db),
):
    analyzer = KeyAnalyzer(db)
    return analyzer.get_recent_keys(start_time=start, end_time=end)


@app.get("/api/keys/high-score")
async def get_high_score_keys(
    start: Optional[int] = None,
    end: Optional[int] = None,
    db: Session = Depends(get_db),
):
    analyzer = KeyAnalyzer(db)
    return analyzer.get_high_score_keys(start_time=start, end_time=end)


@app.get("/api/statistics")
async def get_statistics(
    start: Optional[int] = None,
    end: Optional[int] = None,
    db: Session = Depends(get_db),
):
    analyzer = KeyAnalyzer(db)
    return analyzer.get_statistics(start_time=start, end_time=end)
