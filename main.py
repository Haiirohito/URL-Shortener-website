from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse

from url_shortener import URLShortener


app = FastAPI()
shortener = URLShortener()


@app.get("/")
async def read_root():
    return {"message": "Welcome to URL Shortener"}


@app.post("/shorten")
async def shorten(request: Request):
    data = await request.json()
    long_url = data.get("url")
    if not long_url:
        raise HTTPException(status_code=400, detail="URL is required")
    short_url = shortener.shorten_url(long_url)
    return {"short_url": short_url}


@app.get("/{short_id}")
async def resolve(short_id: str):
    long_url = shortener.resolve_url(short_id)
    if long_url:
        return RedirectResponse(url=long_url)
    raise HTTPException(status_code=404, detail="URL not found")
