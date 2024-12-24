import logging
import sys
from logging.handlers import RotatingFileHandler
import os


def setup_logger(name: str, log_file: str, level=logging.INFO):
    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")

    handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(console_handler)

    return logger


# 创建日志目录
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 设置不同的日志记录器
app_logger = setup_logger("app", "logs/app.log")
access_logger = setup_logger("access", "logs/access.log")
error_logger = setup_logger("error", "logs/error.log")
