import os
import sqlite3
import asyncio
from typing import Annotated
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils import strength, retime, hasher, verify
from fastapi import FastAPI, Request, status, Form
from starlette.middleware.sessions import SessionMiddleware
from security import gen_salt, derive_key, encrypt_data, decrypt_data
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse


conn = sqlite3.connect('passvault.db', check_same_thread=False)
db = conn.cursor()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.add_middleware(
    SessionMiddleware,
    secret_key=os.urandom(24),
    https_only=False,
    max_age= 14400
)


@app.get("/")
def home(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse('/login')

    entry = db.execute("SELECT service, username, category FROM passwords WHERE user_id = ?",(request.session['user_id'],))
    entries = entry.fetchall()
    if not entries:
        entries = None

    return templates.TemplateResponse(
        "dashboard.html", 
        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "entries": entries}
    )


@app.post("/login")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()], request: Request):
    if request.session.get("user_id"):
        return RedirectResponse('/logout')
    
    db.execute("SELECT id, hashed_password, salt FROM users WHERE username = ?", (username,))
    user = db.fetchone()
    
    if user and check_password_hash(user[1], password):
        request.session["user_id"] = user[0]
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse(
        "login.html", 
        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P" , "error": "Invalid Credentials"}
    )

@app.get("/login")
def get_login(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse('/logout')
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P"},
    )

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse('/')

@app.post("/register")
async def register(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    #form_data = await request.form()
    #username = form_data.get("username")
    #password = form_data.get("password")

    # Check if username already exists
    db.execute("SELECT id FROM users WHERE username = ?", (username,))
    if db.fetchone():
        return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)
    
    hashed_password = generate_password_hash(password)
    salt = gen_salt()

    # Save username and hashed_password to database
    db.execute("INSERT INTO users (username, hashed_password, salt) VALUES (?, ?, ?)", (username, hashed_password, salt))
    conn.commit()

    return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)

@app.post("/api/checkUsername")
async def checkUsername(request: Request):
    json_data = await request.json()
    username = json_data.get("username")
    db.execute("SELECT id FROM users WHERE username = ?", (username,))
    if db.fetchone():
        return JSONResponse(content={"status": True})
    return JSONResponse(content={"status": False})


@app.get("/register")
def get_register(request: Request):
    return templates.TemplateResponse(
        "register.html", 
        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P"},
    )
    


@app.api_route('/add-password', methods=['GET', 'POST'])
async def add_password(request: Request):
    if not request.session.get("user_id", None):
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    if request.method == 'POST':
        form_data = await request.form()
   
        service = form_data.get('service').upper()
        username = form_data.get("username")
        password = form_data.get("password")
        category = form_data.get('category').upper()

        master_password = form_data.get('master_password')
        db.execute("SELECT username, hashed_password, salt FROM users WHERE id = ?", (request.session['user_id'],))
        user = db.fetchone()
        salt = user[2]
        check = db.execute("SELECT service, username FROM passwords WHERE service = ? AND username = ?", (service, username))
        if check.fetchone() :
            print("Username already exists!")
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        if user and check_password_hash(user[1], master_password):

            # encrypt the password before saving
            encrypted_password = encrypt_data(derive_key(master_password,salt), password)
            db.execute("INSERT INTO passwords (user_id, service, username, password_encrypted, category) VALUES (?, ?, ?, ?, ?)",
                       (request.session['user_id'], service, username, encrypted_password, category))
            conn.commit()

            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse('/logout')

    elif request.method == 'GET':
        return templates.TemplateResponse(
        "add_password.html", 
        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P"},
    )


@app.post('/del-password')
async def delete_password(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    form_data = await request.form()
    
    service = form_data.get('service').upper()
    
    username = form_data.get("username")
    
    master_password = form_data.get("master_password")
    
    db.execute("SELECT username, hashed_password FROM users WHERE id = ?", (request.session['user_id'],))
    
    user = db.fetchone()
    
    if not user or not check_password_hash(user[1], master_password):
        
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    check = db.execute("SELECT service, username FROM passwords WHERE user_id = ? AND service = ? AND username = ?", (request.session['user_id'], service, username))
    
    if not check.fetchone():
        
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    db.execute("DELETE FROM passwords WHERE user_id = ? AND service = ? AND username = ?", (request.session['user_id'], service, username))
    conn.commit()
        
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        
@app.get('/del-password')
def get_del_password(request: Request):
    return templates.TemplateResponse(
                        "del_password.html", 
                        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P"},
                    )



@app.api_route('/passwords', methods=['GET', 'POST'])
async def passwords(request: Request):
    if not request.session.get("user_id", None):
        return templates.TemplateResponse(
        "error.html", 
        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "error": "401 Unauthorized"},
    )
    if request.method == 'POST':
        form_data = await request.form()
   
        password = form_data.get("password")

        db.execute("SELECT username, hashed_password FROM users WHERE id = ?", (request.session['user_id'],))
        user = db.fetchone()
        username = user[0]
        if user and check_password_hash(user[1], password):
            salt = db.execute("SELECT salt FROM users WHERE username = ?", (username,)).fetchone()[0]
            entry = db.execute("SELECT service, username, password_encrypted, category, updated_at FROM passwords WHERE user_id = ?", (request.session['user_id'],))
            entries = entry.fetchall()
            decrypted_entries = []
            for e in entries:
                decrypted_password = decrypt_data(derive_key(password,salt), e[2])
                decrypted_entries.append((e[0], e[1], decrypted_password, e[3], e[4]))

            if not decrypted_entries:
                decrypted_entries = None

            return templates.TemplateResponse(
                            "passwords.html", 
                            {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "entries": decrypted_entries},
                        )
        else:
            return RedirectResponse('/logout')

    elif request.method == 'GET':
        entry = db.execute("SELECT service, username, password_encrypted, category, updated_at FROM passwords WHERE user_id = ?", (request.session['user_id'],))
        entries = entry.fetchall()
        raw_entries = [(e[0], e[1], "********", e[3], e[4]) for e in entries]
        return templates.TemplateResponse(
        "passwords.html", 
        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "entries": raw_entries},
    )


@app.post('/api/passwords_strength')
async def password_strength(request: Request):
    json_data = await request.json()
    
    password = json_data.get("password")

    stren = strength(password)
    entropy = stren[0]
    time_score = retime(stren[1])

    spicer = 0 #spicer is solely to make progress bar feel more alive without unnecessarily increasing the complexity of program
    if time_score[1] >= 1:
        import random
        spicer = random.uniform(0, 1)
        #spicer = float(f"0.{str(int(entropy))}") #untag it incase unpredictability bicomes an issue;

    score = round(((time_score[1]*10) + spicer), 2)

    
    colour = round(
        (((score-1)/99)*256)
    )
    return JSONResponse(content={"entropy"   : entropy,
                                 "time_score": min(score, 100),
                                 "est_time"  : time_score[0],
                                 "colour"    : colour
                                 })

@app.get("/passwords_strength")
def get_password_strength(request: Request):
    return templates.TemplateResponse(
                        "password_strength.html", 
                        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P"},
                    )

@app.post('/hash_password')
async def hash_passwords(request: Request):
    form_data = await request.form()
    
    password = form_data.get("password")

    stren = hasher(password)

    return templates.TemplateResponse(
                            "hash_password.html", 
                            {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "eval": stren},
                        )
@app.get("/hash_password")
def get_hash_passwords(request: Request):
    return templates.TemplateResponse(
                        "hash_password.html", 
                        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P"},
                    )


@app.post('/verifyHash')
async def verifyHash(request: Request):
    form_data = await request.form()
    
    password = form_data.get("password")
    phash = form_data.get("hash")
    algo = form_data.get("algorithm")

    if algo not in ["SHA-224", "SHA-256", "SHA-384", "SHA-512"]:
        return templates.TemplateResponse(
                            "verify_hash.html", 
                            {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "eval": "Invalid Algorithm"},
                        )

    stren = verify(phash, password, algo)
    e = "Matched" if stren else "Not Matched"
    return templates.TemplateResponse(
                            "verify_hash.html", 
                            {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "eval": e},
                        )
@app.get("/verifyHash")
def get_verifyHash(request: Request):
    return templates.TemplateResponse(
                        "verify_hash.html", 
                        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P"},
                    )







#@app.exception_handler(404)
#def page_not_found(request: Request):
#    return templates.TemplateResponse('error.html',
#    {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P"},
#    error="404- Not Found",
#    ), 404
#@app.exception_handler(500)
#def internal_server_error(request: Request):
#    return templates.TemplateResponse('error.html', 
#    {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P"},
#    error="500- Internal Server Error",
#    ), 500
#@app.exception_handler(Exception)
#def handle_exception(e, request: Request):
#    return templates.TemplateResponse('error.html', 
#    {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P"},
#    error="-An error occurred: " + str(e),
#    ), 500
#


if __name__ == '__main__':
    os.system("uvicorn main:app --reload")