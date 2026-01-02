import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from miku_ai import get_wexin_article

app = FastAPI(title="Wespider API")

class QueryReq(BaseModel):
    query: str
    top: int = 5
    max_age_days: Optional[int] = 14

@app.post("/summarize")
async def summarize(req: QueryReq):
    """Return raw article JSON from miku_ai."""
    try:
        articles = await get_wexin_article(req.query, top_num=req.top, max_age_days=req.max_age_days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching articles: {e}")

    return {"count": len(articles), "articles": articles}

if __name__ == "__main__":
    import uvicorn
    host = os.getenv('WSP_HOST', 'localhost')
    port = int(os.getenv('WSP_PORT', '7000'))
    uvicorn.run("wespider_api.app:app", host=host, port=port, reload=True)
