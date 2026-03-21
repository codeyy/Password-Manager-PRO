import os
import asyncio
from pathlib import Path
from typing import Annotated
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi import Request, status, Form, APIRouter, Depends
from sqlalchemy import and_, delete
from app.services.strength_eval import strength, retime, hasher, verify
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from app.core.security import gen_salt, derive_key, encrypt_data, decrypt_data
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.passwords import PasswordEntry
from app.models.users import User



router = APIRouter()


BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATES = os.path.join(BASE_DIR, "app\\templates")
templates = Jinja2Templates(directory=TEMPLATES)

@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("user_id"):
        return RedirectResponse('/login')

    entries = db.query(PasswordEntry.service, PasswordEntry.username, PasswordEntry.category).filter(PasswordEntry.user_id == request.session['user_id']).all()
    if not entries:
        entries = None

    indc = request.session.get("_flashMsg")
    request.session["_flashMsg"] = False
    return templates.TemplateResponse(
        "dashboard.html", 
        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "entries": entries, "indc": indc}
    )


@router.post("/login")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()], request: Request, db: Session = Depends(get_db)):
    if request.session.get("user_id"):
        return RedirectResponse('/logout')

    user = db.query(User.id, User.hashed_password, User.salt).filter(User.username == username).first()

    if user and check_password_hash(user[1], password):
        request.session["user_id"] = user[0]
        request.session["_flashMsg"] = "Logged In"
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse(
        "login.html", 
        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "error": "Invalid Credentials"},
    )

@router.get("/login")
def get_login(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse('/logout')
    indc = request.session.get("_flashMsg")
    request.session["_flashMsg"] = False
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "indc": indc},
    )

@router.api_route('/logout', methods=['GET', 'POST'])
def logout(request: Request):
    request.session.clear()
    return RedirectResponse('/')

@router.post("/register")
async def register(request: Request, username: Annotated[str, Form()], password: Annotated[str, Form()], db: Session = Depends(get_db)):

    if db.query(User.id).filter(User.username == username).first():
        return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)
    
    new_user = User(
        username=username,
        hashed_password=generate_password_hash(password),
        salt=gen_salt()
    )
    db.add(new_user)
    db.commit()

    request.session["_flashMsg"] = "Registered"
    return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)

@router.post("/api/checkUsername")
async def checkUsername(request: Request, db: Session = Depends(get_db)):
    json_data = await request.json()
    x = db.query(User.id).filter(User.username == json_data.get("username")).all()
    if x != []:
        return JSONResponse(content={"status": True})
    return JSONResponse(content={"status": False})


@router.get("/register")
def get_register(request: Request): 
    indc = request.session.get("_flashMsg")
    request.session["_flashMsg"] = False
    return templates.TemplateResponse(
        "register.html", 
        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "indc": indc},
    )
    

@router.api_route('/add-password', methods=['GET', 'POST'])
async def add_password(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
    "error.html", 
    {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "error": "401 - Un Authorized Access"},
    )
    if request.method == 'POST':
        form_data = await request.form()
   
        service = form_data.get('service').upper()
        username = form_data.get("username")
        password = form_data.get("password")
        category = form_data.get('category').upper()

        master_password = form_data.get('master_password')
        
        user = db.query(User.username, User.hashed_password, User.salt).filter(User.id == (request.session['user_id'])).all()[0]
        salt = user[2]

        check = db.query(PasswordEntry.username).filter(PasswordEntry.username == username).all()
        if check != []:
            print("Username already exists!")
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        if user and check_password_hash(user[1], master_password):
            encrypted_password = encrypt_data(derive_key(master_password,salt), password)
            new_password = PasswordEntry(
                user_id = request.session['user_id'],
                service = service,
                username = username,
                password_encrypted = encrypted_password,
                category = category
            )
            db.add(new_password)
            db.commit()

            request.session["_flashMsg"] = "Password added successfully"
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse('/logout')

    elif request.method == 'GET':
        user_id = request.session.get("user_id")
        if not user_id:
            return templates.TemplateResponse(
        "error.html", 
        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "error": "401 - Un Authorized Access"},
    )

        return templates.TemplateResponse(
        "add_password.html", 
        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P"},
    )


@router.post('/del-password')
async def delete_password(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
    "error.html", 
    {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "error": "401 - Un Authorized Access"},
    )
    
    form_data = await request.form()
    
    service = form_data.get('service').upper()
    
    username = form_data.get("username")
    
    master_password = form_data.get("master_password")

    user = db.query(User.username, User.hashed_password).filter(User.id == request.session['user_id']).first()
    
    if not user or not check_password_hash(user[1], master_password):
        
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    #check = db.execute("SELECT service, username FROM passwords WHERE user_id = ? AND service = ? AND username = ?", (request.session['user_id'], service, username))
    user = db.query(PasswordEntry.service, PasswordEntry.username).filter(
        and_(
            PasswordEntry.user_id == request.session['user_id'],
            PasswordEntry.service == service,
            PasswordEntry.username == username
        )
    ).first()
    if not user:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    print(user)
    
    #db.execute("DELETE FROM passwords WHERE user_id = ? AND service = ? AND username = ?", (request.session['user_id'], service, username))
    #conn.commit()
    
    stmt = delete(PasswordEntry).where(
        and_(
            PasswordEntry.user_id == request.session['user_id'],
            PasswordEntry.service == service,
            PasswordEntry.username == username
        )
    )
    db.execute(stmt)
    db.commit()

    request.session["_flashMsg"] = "Deletion Successfull"   
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        
@router.get('/del-password')
def get_del_password(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
    "error.html", 
    {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "error": "401 - Un Authorized Access"},
    )
    return templates.TemplateResponse(
                        "del_password.html", 
                        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P"},
                    )



@router.api_route('/passwords', methods=['GET', 'POST'])
async def passwords(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
    "error.html", 
    {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "error": "401 - Un Authorized Access"},
    )
    if request.method == 'POST':
        form_data = await request.form()
   
        password = form_data.get("password")

        user = db.query(User.username, User.hashed_password).filter(User.id == request.session['user_id']).first()
        username = user[0]
        if user and check_password_hash(user[1], password):
            salt = db.query(User.salt).filter(User.username == username).first()
            entries = db.query(PasswordEntry.service, PasswordEntry.username, PasswordEntry.password_encrypted, PasswordEntry.category, PasswordEntry.updated_at).filter(User.id == request.session['user_id']).all()
            
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
        user_id = request.session.get("user_id")
        if not user_id:
            return templates.TemplateResponse(
        "error.html", 
        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "error": "401 - Un Authorized Access"},
        )
        #entry = db.execute("SELECT service, username, password_encrypted, category, updated_at FROM passwords WHERE user_id = ?", (request.session['user_id'],))
        entries = db.query(PasswordEntry.service, PasswordEntry.username, PasswordEntry.password_encrypted, PasswordEntry.category, PasswordEntry.updated_at).filter(User.id == request.session['user_id']).all()

        raw_entries = [(e[0], e[1], "********", e[3], e[4]) for e in entries]
        return templates.TemplateResponse(
        "passwords.html", 
        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "entries": raw_entries},
    )


@router.post('/api/passwords_strength')
async def password_strength(request: Request):
    json_data = await request.json()
    
    password = json_data.get("password")

    stren = strength(password)
    entropy = stren[0]
    time_score = retime(stren[1])

    spcr = 0 
    if time_score[1] >= 1:
        #import random
        #spcr = random.uniform(0, 1)
        spcr = float(f"0.{str(int(entropy))}") #untag it incase unpredictability bicomes an issue;

    score = round(((time_score[1]*10) + spcr), 2)

    
    colour = round(
        (((score-1)/99)*256)
    )
    return JSONResponse(content={"entropy"   : entropy,
                                 "time_score": min(score, 100),
                                 "est_time"  : time_score[0],
                                 "colour"    : colour
                                 })

@router.get("/passwords_strength")
def get_password_strength(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
    "error.html", 
    {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "error": "401 - Un Authorized Access"},
    )
    return templates.TemplateResponse(
                        "password_strength.html", 
                        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P"},
                    )

@router.post('/hash_password')
async def hash_passwords(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
    "error.html", 
    {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "error": "401 - Un Authorized Access"},
    )
    form_data = await request.form()
    
    password = form_data.get("password")

    stren = hasher(password)

    return templates.TemplateResponse(
                            "hash_password.html", 
                            {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "eval": stren},
                        )
@router.get("/hash_password")
def get_hash_passwords(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
    "error.html", 
    {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "error": "401 - Un Authorized Access"},
    )
    return templates.TemplateResponse(
                        "hash_password.html", 
                        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P"},
                    )


@router.post('/verifyHash')
async def verifyHash(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
    "error.html", 
    {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "error": "401 - Un Authorized Access"},
    )
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
@router.get("/verifyHash")
def get_verifyHash(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
    "error.html", 
    {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P", "error": "401 - Un Authorized Access"},
    )
    return templates.TemplateResponse(
                        "verify_hash.html", 
                        {"request": request, "title": "Password_Manager_Pro", "name": "P-M-P"},
                    )


