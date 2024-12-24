import os

# 获取环境变量，默认为开发环境
ENV = os.getenv("ENV", "development")

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
    },
    "production": {
        "debug": False,
        "cors": {"origins": ["https://your-production-domain.com"]},
    },
}

# 获取当前环境的配置
current_config = config[ENV]
