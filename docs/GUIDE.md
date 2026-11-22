# 图书借阅 L1 · 项目搭建与跟做详解

> 项目仓库：https://github.com/Jxg516/fastapi-library-borrow  
> 快速上手：见仓库根目录 [README.md](../README.md)

## 4.1 你将完成什么（验收标准）

1. 本地启动服务，打开 Swagger `/docs`。  
2. 新增一本书，`GET /books` 能看到且 `available=true`。  
3. `borrow` 成功后再借同一本 → **409**。  
4. `return` 后 `available` 恢复为 `true`；未借出时 return → **409**。  
5. 故意提交非法字段（如空 title）→ **422**（校验层，不是业务层）。

## 4.2 仓库里有什么（结构说明）

| 文件 | 作用 |
|------|------|
| `main.py` | 路由：health / 建书 / 借 / 还 |
| `requirements.txt` | `fastapi` + `uvicorn` 版本锁定 |
| `README.md` | 跟做步骤：venv、启动、curl 清单 |
| `docs/GUIDE.md` | 本文：详解与跟做主线 |
| `.gitignore` | 忽略 `.venv`、`.env`、`__pycache__` 等 |

数据在**内存字典**，重启丢数据——L1 先把 HTTP 语义练熟。

## 4.3 接口与状态（跟做时对照表）

| 方法 | 路径 | 成功 | 常见失败 |
|------|------|------|----------|
| GET | `/health` | 200 + ok | 端口未启 |
| POST | `/books` | 201 | 422 校验失败 |
| POST | `/books/{id}/borrow` | 200 | 404 无书；409 已借出 |
| POST | `/books/{id}/return` | 200 | 404 无书；409 未借出 |

**状态机**：每本书只有 `available: true/false`。借书 true→false；还书 false→true。

## 4.4 推荐跟做顺序

1. `git clone https://github.com/Jxg516/fastapi-library-borrow`（或下载 ZIP）。  
2. 按 **README** 建 venv、`pip install`、启动 `uvicorn`（示例端口 8765，可改）。  
3. 先用 **Swagger** 点通 borrow → 再点一次看 409 → 再点 return。  
4. 再用 README 里的 curl（或 PowerShell `Invoke-RestMethod`）复现。  
5. 对照 **4.1 验收清单** 打勾；有一项不过，先看 **4.6**，不要跳步改库表。

## 4.5 设计取舍（为什么这样做）

- **POST 改状态**：借/还不是 GET，避免幂等读误当写操作。  
- **422 vs 409**：前者 JSON 不合法，后者业务不允许。  
- **return 接口**：借→还闭环，比只 borrow 更易有完成感。  
- **不接 MySQL**：L1 不与热点大仓拼复杂度；持久化可开分支演进。

## 4.6 常见报错（先查这几条）

| 现象 | 可能原因 |
|------|----------|
| `ModuleNotFoundError: fastapi` | 未激活 venv 或未 `pip install -r requirements.txt` |
| 端口占用 | 换 `--port` 或关掉旧 uvicorn |
| 409 already borrowed | 先 return 再借 |
| 422 Unprocessable | 检查 `title`/`author` 是否为空或超长 |

## 4.7 和热点大项目的体力账

跟紧巨型 Agent 仓库常要环境矩阵、前端构建、模型路径一起上。本仓控制在少量文件、五个接口，精力放在 **Swagger 跟做 + 状态码理解**。热点看方向，小 API 练合约。
