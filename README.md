# fastapi-library-borrow

CSDN 周三热点配套项目：**内存版图书借阅 API**（FastAPI）。

## 环境

- Python 3.10+
- Windows / macOS / Linux

## 安装

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
```

## 启动

```bash
uvicorn main:app --host 127.0.0.1 --port 8765
```

打开 Swagger：`http://127.0.0.1:8765/docs`

## 接口一览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/books` | 图书列表 |
| POST | `/books` | 新增图书 |
| POST | `/books/{id}/borrow` | 借阅（已借出返回 409） |
| POST | `/books/{id}/return` | 归还（未借出返回 409） |

## 验收（跟做清单）

1. `GET /health` → `{"status":"ok"}`
2. `POST /books` 创建一本书
3. `POST /books/1/borrow` → `borrowed: true`
4. 再次 borrow → **409**
5. `POST /books/1/return` → `returned: true`
6. `GET /books` 中 `available` 恢复为 `true`

## 关联文章

**项目搭建详解**：[docs/GUIDE.md](docs/GUIDE.md)  
CSDN 稿件见博主「周三热点实战」系列；**项目名 = 本仓库名**。
