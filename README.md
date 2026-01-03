# Wespider API

A small FastAPI service that exposes Weixin article search results as JSON. Originally adapted from the Miku Spider examples.

Quick start

1. Install dependencies and the `miku_ai` package (this project uses it as a dependency):

```bash
python -m pip install -r requirements.txt
# or, if you are developing miku_ai locally:
# pip install -e /path/to/Miku_Spider
```

2. Run the service:

```bash
# 推荐（使用 conda 环境）
conda create -n wespider python=3.10 -y
conda activate wespider
pip install -r requirements.txt
# 安装本仓库为可编辑包（将使用本地 miku_ai）
pip install -e ..

# 启动服务（开发时，在激活的 conda 环境中运行）
uvicorn wespider_api.wespider_api.app:app --reload --host 127.0.0.1 --port 7000

# 或者不激活环境，使用 conda run：
conda run -n wespider uvicorn wespider_api.wespider_api.app:app --host 127.0.0.1 --port 7000
```

3. Test:

```bash
curl -X POST "http://localhost:7000/summarize" -H "Content-Type: application/json" -d '{"query":"artificial intelligence","top":2,"max_age_days":14}'
```

Docs & notes

- Swagger UI: `http://localhost:7000/docs`
- This service returns raw article JSON from the upstream `miku_ai.get_wexin_article` call.
- Configure host/port via environment or your process supervisor; defaults shown above.

测试与运行（快速验证）

- 用 curl 验证 `/summarize`（示例）：

```bash
curl -X POST "http://127.0.0.1:7000/summarize" -H "Content-Type: application/json" -d '{"query":"artificial intelligence","top":2,"max_age_days":14}'
```

- 在 conda 环境中运行测试套件：

```bash
conda run -n wespider pytest -q
```

查看运行日志

- 前台运行（直接在终端），日志会输出到当前终端：

```bash
uvicorn wespider_api.wespider_api.app:app --reload --host 127.0.0.1 --port 7000
```

- 后台/无交互运行，使用 `nohup` 或重定向到文件，然后用 `tail -f` 查看：

```bash
nohup uvicorn wespider_api.wespider_api.app:app --host 127.0.0.1 --port 7000 > /tmp/uvicorn.log 2>&1 &
tail -f /tmp/uvicorn.log
```

- 如果通过 `systemd` 管理（示例 service 名称 `wespider`），查看 journal 日志：

```bash
journalctl -u wespider -f
```

- 在容器中运行时，使用 `docker`：

```bash
docker logs -f <container-name-or-id>
```

- 快速排查端口占用（例如 7000）：

```bash
lsof -iTCP:7000 -sTCP:LISTEN -P -n
```

使用带时间戳的日志 wrapper

- 项目包含 `run_with_timestamps.py`，它会启动 `uvicorn` 并把 stdout/stderr 每行前加时间戳写入 `/tmp/uvicorn_timestamped.log`，便于排查和归档。

- 在 `wespider` conda 环境中后台运行（示例）：

```bash
conda run -n wespider nohup python wespider_api/run_with_timestamps.py 127.0.0.1 7000 > /tmp/run_with_timestamps.out 2>&1 &
```

- 日志文件：

```
/tmp/uvicorn_timestamped.log
```

- 实时查看：

```bash
tail -f /tmp/uvicorn_timestamped.log
```

- 停止服务：查到 wrapper 进程并杀掉（示例）：

```bash
ps aux | grep run_with_timestamps.py
kill <PID>
```

- 说明与注意事项：
	- `run_with_timestamps.py` 会直接使用运行命令的 Python，可通过 `conda run -n wespider` 确保使用 `wespider` 环境；
	- 如果遇到 `No module named uvicorn` 错误，请先在该环境中安装 `uvicorn`：`conda run -n wespider pip install uvicorn` 或 `pip install -r requirements.txt`。

License: MIT
