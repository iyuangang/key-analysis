import os
import json

# 获取环境变量，默认为开发环境
ENV = os.getenv("ENV", "development")

# 获取配置文件路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

# 加载配置文件
try:
    with open(CONFIG_PATH) as f:
        file_config = json.load(f)
except Exception as e:
    print(f"Error loading config file: {e}")
    file_config = {}

# 环境配置
config = {
    "development": {
        "debug": True,
        "cors": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "http://0.0.0.0:5173",
            ]
        },
        "redis": file_config.get("redis", {}),  # 从配置文件加载 Redis 配置
    },
    "production": {
        "debug": False,
        "cors": {"origins": ["https://your-production-domain.com"]},
        "redis": file_config.get("redis", {}),  # 从配置文件加载 Redis 配置
    },
}

# 获取当前环境的配置
current_config = config[ENV]

# 添加数据库和 Redis 配置
current_config.update(
    {"database": file_config.get("database", {}), "redis": file_config.get("redis", {})}
)
