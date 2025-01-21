from fastapi.responses import FileResponse, RedirectResponse
from fastapi import APIRouter, HTTPException

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

import random
import string
import qrcode
import os

from .database import database, urls

router = APIRouter()


def generate_short_url():
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))


class ShortenRequest(BaseModel):
    original_url: str
    custom_alias: Optional[str] = None
    expiry_date: Optional[datetime] = None


@router.post("/shorten")
async def shorten_url(request: ShortenRequest):
    original_url = request.original_url
    custom_alias = request.custom_alias
    expiry_date = request.expiry_date

    if not original_url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Invalid URL format.")

    if expiry_date and expiry_date <= datetime.utcnow():
        raise HTTPException(
            status_code=400, detail="Expiry date must be in the future."
        )

    # Check for custom alias
    if custom_alias:
        query = urls.select().where(urls.c.custom_alias == custom_alias)
        existing = await database.fetch_one(query)
        if existing:
            raise HTTPException(status_code=400, detail="Custom alias already in use.")
        short_url = custom_alias
    else:
        short_url = generate_short_url()

    query = urls.insert().values(
        original_url=original_url,
        shortened_url=short_url,
        custom_alias=custom_alias,
        expiry_date=expiry_date,
    )
    await database.execute(query)

    return {"shortened_url": f"{short_url}"}


@router.get("/{shortened_url}")
async def redirect_to_original(shortened_url: str):
    query = urls.select().where(
        (urls.c.shortened_url == shortened_url) | (urls.c.custom_alias == shortened_url)
    )
    result = await database.fetch_one(query)
    if result:
        if result["expiry_date"] and datetime.utcnow() > result["expiry_date"]:
            raise HTTPException(status_code=404, detail="URL has expired.")

        return RedirectResponse(result["original_url"])

    raise HTTPException(status_code=404, detail="URL not found")


@router.get("/qrcode/{shortened_url}")
async def generate_qr_code(shortened_url: str):
    domain = os.getenv("APP_DOMAIN", "http://127.0.0.1:8000")

    query = urls.select().where(
        (urls.c.shortened_url == shortened_url) | (urls.c.custom_alias == shortened_url)
    )
    result = await database.fetch_one(query)

    if not result:
        raise HTTPException(status_code=404, detail="URL not found")

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"{domain}/{shortened_url}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    qr_path = f"qrcodes/{shortened_url}.png"
    os.makedirs("qrcodes", exist_ok=True)
    img.save(qr_path)

    # Check if file was saved
    if not os.path.exists(qr_path):
        raise HTTPException(status_code=500, detail="Failed to generate QR code image.")

    return FileResponse(qr_path, media_type="image/png")
