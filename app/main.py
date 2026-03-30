import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, HTTPException
from app.api.endpoints import router
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


app.add_middleware(
    SessionMiddleware,
    secret_key=os.urandom(24),
    https_only=False,
    max_age= 84000, 
)

app.include_router(router)


# 1. Handle Known HTTP Errors (404, 415, 403, etc.)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    TEMPLATES = os.path.join(BASE_DIR, "app\\templates")
    templates = Jinja2Templates(directory=TEMPLATES)
    return templates.TemplateResponse(
    request=request,
    name="error.html",
    context={"error": str(exc.status_code)+" "+str(exc.detail)},
    status_code=exc.status_code
)

# 2. Handle Unexpected Server Errors (500)
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    TEMPLATES = os.path.join(BASE_DIR, "app\\templates")
    templates = Jinja2Templates(directory=TEMPLATES)
    return templates.TemplateResponse(
    request=request,
    name="error.html",
    context={"error": "A serious server error occurred."},
    status_code=500
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)