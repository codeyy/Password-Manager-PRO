import os
from fastapi import FastAPI
from app.api.endpoints import router
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Mount static files (CSS/JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_middleware(
    SessionMiddleware,
    secret_key=os.urandom(24),
    https_only=False,
    max_age= 14400
)
# Include the routes we defined in endpoints.py
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)