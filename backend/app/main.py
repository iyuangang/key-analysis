from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .config import current_config
from .utils.debug import debug
from .routers import auth, users, keys, statistics

app = FastAPI()


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
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(keys.router)
app.include_router(statistics.router)
