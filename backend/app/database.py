from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import os

# 获取当前文件所在目录的上级目录路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 读取配置文件
with open(os.path.join(BASE_DIR, "config.json")) as f:
    config = json.load(f)

# 构建数据库URL
db_config = config["database"]
SQLALCHEMY_DATABASE_URL = f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
