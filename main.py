import os
import sqlite3
import asyncio
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from werkzeug.security import generate_password_hash, check_password_hash
from security import gen_salt, derive_key, encrypt_data, decrypt_data


conn = sqlite3.connect('passvault.db', check_same_thread=False)
db = conn.cursor()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.add_middleware(
    SessionMiddleware,
    secret_key=os.urandom(24),
    https_only=True
)



@app.get("/")
def home(request: Request):
    if "user" not in request.session:
        return RedirectResponse('/login')

    entry = db.execute("SELECT service, username, category FROM passwords WHERE user_id = ?",(request.session['user_id'],))
    entries = entry.fetchall()
    if not entries:
        entries = None

    return templates.TemplateResponse(
        "dashboard.html", 
        {"request": request, "title": "FastAPI Demo", "name": "User"}, entries=entries
    )


@app.post("/login")
async def login(request: Request):
    form_data = await request.form()
    username = form_data.get('username')
    password = form_data.get('password')

    db.execute("SELECT id, hashed_password, salt FROM users WHERE username = ?", (username,))
    user = db.fetchone()

    if user and check_password_hash(user[1], password):
        request.session['user_id'] = user[0]
        #flash("loged in")
        return RedirectResponse('/')
    else:
        return templates.TemplateResponse(
        "login.html", 
        {"request": request, "title": "FastAPI Demo", "name": "User"}, error="Invalid Credentials"
    )


@app.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "title": "FastAPI Demo", "name": "User"},
    )

