import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware

from app.api.endpoints import router

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"

# Initialize app
app = FastAPI(title="Password Manager PRO", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Add middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.urandom(24),
    https_only=False,
    max_age=84000,
)

# Include routers
app.include_router(router)

# Exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> HTMLResponse:
    """Handle HTTP exceptions (404, 415, 403, etc.)."""
    templates = Jinja2Templates(directory=TEMPLATES_DIR)
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={"error": f"{exc.status_code} {exc.detail}"},
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> HTMLResponse:
    """Handle unexpected server errors (500)."""
    templates = Jinja2Templates(directory=TEMPLATES_DIR)
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={"error": "A serious server error occurred."},
        status_code=500,
    )

if __name__ == "__main__":
    print("Starting Password Manager PRO...")