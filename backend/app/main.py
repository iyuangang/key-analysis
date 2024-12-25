from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.db import init_db
from .config import current_config
from .utils.debug import debug
from .routers import auth, users, keys, statistics

app = FastAPI(
    title="Key Analysis API",
    description="A FastAPI application for key analysis",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event():
    debug.log("Starting up application...")
    await init_db()
    debug.log("Application startup completed")


# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=current_config["cors"]["origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(keys.router, prefix="/api", tags=["keys"])
app.include_router(statistics.router, prefix="/api", tags=["statistics"])
