#!/bin/bash

# 开发环境
export ENV=development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产环境
# export ENV=production
# uvicorn app.main:app --host 0.0.0.0 --port 8000
