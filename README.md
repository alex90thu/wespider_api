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
uvicorn wespider_api.app:app --reload --host localhost --port 7000
```

3. Test:

```bash
curl -X POST "http://localhost:7000/summarize" -H "Content-Type: application/json" -d '{"query":"上海交通大学","top":2,"max_age_days":14}'
```

Docs & notes

- Swagger UI: `http://localhost:7000/docs`
- This service returns raw article JSON from the upstream `miku_ai.get_wexin_article` call.
- Configure host/port via environment or your process supervisor; defaults shown above.

License: MIT
