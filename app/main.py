from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from .database import engine, metadata
from .routes import router
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)
