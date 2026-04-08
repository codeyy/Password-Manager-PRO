"""
Password Manager Pro - API Endpoints
Handles authentication, password management, and security utilities.
"""

import os
from pathlib import Path
from typing import Annotated

from sqlalchemy.orm import Session
from sqlalchemy import and_, delete
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi import APIRouter, Depends, Request, Response, status, Form
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.users import User
from app.models.database import get_db
from app.models.passwords import PasswordEntry
from app.services.strength_eval import strength, retime, hasher, verify
from app.core.security import gen_salt, derive_key, encrypt_data, decrypt_data

# ============================================================================
# Configuration
# ============================================================================

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATES = os.path.join(BASE_DIR, "app/", "templates")
templates = Jinja2Templates(directory=TEMPLATES)


# ============================================================================
# Authentication Endpoints
# ============================================================================

@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    """Dashboard - displays user's stored passwords."""
    if not request.session.get("user_id"):
        return RedirectResponse(url='/login')

    entries = db.query(
        PasswordEntry.service, 
        PasswordEntry.username, 
        PasswordEntry.category
    ).filter(PasswordEntry.user_id == request.session['user_id']).all()
    
    if not entries:
        entries = None

    indc = request.session.get("_flashMsg")
    request.session["_flashMsg"] = False
    
    return templates.TemplateResponse(
        request=request, 
        name="dashboard.html", 
        context={
            "title": "Password_Manager_Pro", 
            "name": "P-M-P", 
            "entries": entries, 
            "indc": indc
        }
    )


@router.get("/login")
def get_login(request: Request):
    """Login page - GET request."""
    if request.session.get("user_id"):
        return RedirectResponse(url='/logout')
    
    indc = request.session.get("_flashMsg")
    request.session["_flashMsg"] = False
    
    return templates.TemplateResponse(
        request=request, 
        name="login.html", 
        context={
            "title": "Password_Manager_Pro", 
            "name": "P-M-P", 
            "indc": indc
        }
    )


@router.post("/login")
async def login(
    username: Annotated[str, Form()], 
    password: Annotated[str, Form()], 
    request: Request,
    response: Response, 
    db: Session = Depends(get_db)
):
    """Login endpoint - validates credentials and creates session."""
    if request.session.get("user_id"):
        return RedirectResponse(url='/logout')

    user = db.query(
        User.id, 
        User.hashed_password, 
        User.salt
    ).filter(User.username == username).first()
    
    if user and check_password_hash(user[1], password):
        response.set_cookie(
            key="session",
            value="token",
            max_age=36000,
            httponly=True,
            secure=True,
            samesite="lax"
        )
        request.session["user_id"] = user[0]
        request.session["_flashMsg"] = "Logged In"
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse(
        request=request, 
        name="login.html", 
        context={
            "title": "Password_Manager_Pro", 
            "name": "P-M-P", 
            "error": "Invalid Credentials"
        }
    )


@router.get("/register")
def get_register(request: Request):
    """Registration page - GET request."""
    indc = request.session.get("_flashMsg")
    request.session["_flashMsg"] = False
    
    return templates.TemplateResponse(
        request=request, 
        name="register.html", 
        context={
            "title": "Password_Manager_Pro", 
            "name": "P-M-P", 
            "indc": indc
        }
    )


@router.post("/register")
async def register(
    request: Request, 
    username: Annotated[str, Form()], 
    password: Annotated[str, Form()], 
    db: Session = Depends(get_db)
):
    """Register new user - creates account with hashed password."""
    if db.query(User.id).filter(User.username == username).first():
        return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)
    
    new_user = User(
        username=username,
        hashed_password=generate_password_hash(password),
        salt=gen_salt()
    )
    db.add(new_user)
    db.commit()

    request.session["_flashMsg"] = "Registered"
    return RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)


@router.api_route('/logout', methods=['GET', 'POST'])
def logout(request: Request):
    """Logout endpoint - clears user session."""
    request.session.clear()
    return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)


@router.post("/api/checkUsername")
async def check_username(request: Request, db: Session = Depends(get_db)):
    """API endpoint - checks if username exists."""
    json_data = await request.json()
    x = db.query(User.id).filter(User.username == json_data.get("username")).all()
    
    return JSONResponse(content={"status": bool(x)})


# ============================================================================
# Password Management Endpoints
# ============================================================================

@router.get('/add-password')
async def get_add_password(request: Request):
    """Add password page - GET request."""
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": "401 - Un Authorized Access"}
        )
    
    return templates.TemplateResponse(
        request=request, 
        name="add_password.html", 
        context={
            "title": "Password_Manager_Pro", 
            "name": "P-M-P"
        }
    )


@router.post('/add-password')
async def add_password(
    request: Request, 
    username: Annotated[str, Form()],
    password: Annotated[str, Form()], 
    service: Annotated[str, Form()], 
    category: Annotated[str, Form()],
    master_password: Annotated[str, Form()],
    db: Session = Depends(get_db)
):
    """Add new password entry - encrypts and stores password."""
    service = service.upper()
    category = category.upper() if category != "N/A" else "___"
    
    user = db.query(
        User.username, 
        User.hashed_password, 
        User.salt
    ).filter(User.id == request.session['user_id']).first()
    
    salt = user[2]
    
    # Check for duplicate entries
    check = db.query(PasswordEntry.username).filter(
        and_(
            PasswordEntry.user_id == request.session['user_id'],
            PasswordEntry.service == service,
            PasswordEntry.username == username
        )
    ).all()
    
    if check:
        request.session["_flashMsg"] = "Username and service already exists!"
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    if user and check_password_hash(user[1], master_password):
        encrypted_password = encrypt_data(derive_key(master_password, salt), password)
        
        new_password = PasswordEntry(
            user_id=request.session['user_id'],
            service=service,
            username=username,
            password_encrypted=encrypted_password,
            category=category
        )
        db.add(new_password)
        db.commit()
        
        request.session["_flashMsg"] = "Password added successfully"
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    request.session["_flashMsg"] = "Wrong Master Password"
    return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/passwords')
async def get_passwords(request: Request, db: Session = Depends(get_db)):
    """View passwords page - GET request with masked passwords."""
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": "401 - Un Authorized Access"}
        )

    entries = db.query(
        PasswordEntry.service, 
        PasswordEntry.username, 
        PasswordEntry.password_encrypted, 
        PasswordEntry.category, 
        PasswordEntry.updated_at
    ).filter(PasswordEntry.user_id == user_id).all()

    # Mask passwords on GET request
    raw_entries = [(e[0], e[1], "********", e[3], e[4]) for e in entries]

    indc = request.session.get("_flashMsg")
    request.session["_flashMsg"] = False
    
    return templates.TemplateResponse(
        request=request, 
        name="passwords.html", 
        context={
            "title": "Password_Manager_Pro", 
            "name": "P-M-P", 
            "entries": raw_entries, 
            "indc": indc
        }
    )


@router.post('/passwords')
async def post_passwords(request: Request, db: Session = Depends(get_db)):
    """View passwords - decrypts passwords after master password verification."""
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": "401 - Un Authorized Access"}
        )
    
    form_data = await request.form()
    password = form_data.get("password")

    user = db.query(
        User.hashed_password, 
        User.salt
    ).filter(User.id == user_id).first()
    
    if not user or not check_password_hash(user[0], password):
        request.session["_flashMsg"] = "Wrong Master Password"
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    salt = user[1]
    entries = db.query(
        PasswordEntry.service, 
        PasswordEntry.username, 
        PasswordEntry.password_encrypted, 
        PasswordEntry.category, 
        PasswordEntry.updated_at
    ).filter(PasswordEntry.user_id == user_id).all()
    
    decrypted_entries = [
        (e[0], e[1], decrypt_data(derive_key(password, salt), e[2]), e[3], e[4])
        for e in entries
    ]

    if not decrypted_entries:
        decrypted_entries = None

    return templates.TemplateResponse(
        request=request, 
        name="passwords.html", 
        context={
            "title": "Password_Manager_Pro", 
            "name": "P-M-P", 
            "entries": decrypted_entries
        }
    )


@router.get('/del-password')
def get_del_password(request: Request):
    """Delete password page - GET request."""
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": "401 - Un Authorized Access"}
        )
    
    return templates.TemplateResponse(
        request=request, 
        name="del_password.html", 
        context={
            "title": "Password_Manager_Pro", 
            "name": "P-M-P"
        }
    )


@router.post('/del-password')
async def delete_password(request: Request, db: Session = Depends(get_db)):
    """Delete password entry - removes single password after verification."""
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": "401 - Un Authorized Access"}
        )
    
    form_data = await request.form()
    service = form_data.get('service').upper()
    username = form_data.get("username")
    master_password = form_data.get("master_password")

    user = db.query(
        User.username, 
        User.hashed_password
    ).filter(User.id == user_id).first()
    
    if not user or not check_password_hash(user[1], master_password):    
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    # Verify entry exists
    entry = db.query(
        PasswordEntry.service, 
        PasswordEntry.username
    ).filter(
        and_(
            PasswordEntry.user_id == user_id,
            PasswordEntry.service == service,
            PasswordEntry.username == username
        )
    ).first()
    
    if not entry:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    # Delete entry
    stmt = delete(PasswordEntry).where(
        and_(
            PasswordEntry.user_id == user_id,
            PasswordEntry.service == service,
            PasswordEntry.username == username
        )
    )
    db.execute(stmt)
    db.commit()

    request.session["_flashMsg"] = "Deletion Successfull"   
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.post('/del_passwords_fromPasswords')
async def delete_multiple_passwords(request: Request, db: Session = Depends(get_db)):
    """Delete multiple passwords - batch deletion capability."""
    json_data = await request.json()
    delete_these = json_data.get("deleteThese")
    master_password = json_data.get("password")

    user = db.query(
        User.username, 
        User.hashed_password
    ).filter(User.id == request.session['user_id']).first()
    
    if not user or not check_password_hash(user[1], master_password):
        request.session["_flashMsg"] = "Wrong Password"
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    user_id = request.session['user_id']
    
    # Delete each entry
    for service, username in delete_these:
        stmt = delete(PasswordEntry).where(
            and_(
                PasswordEntry.user_id == user_id,
                PasswordEntry.service == service,
                PasswordEntry.username == username
            )
        )
        db.execute(stmt)
    
    db.commit()

    request.session["_flashMsg"] = "Deletion Successfull"
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


# ============================================================================
# Security Utilities Endpoints
# ============================================================================

@router.get("/passwords_strength")
def get_password_strength(request: Request):
    """Password strength checker page - GET request."""
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "title": "Password_Manager_Pro", 
                "name": "P-M-P", 
                "error": "401 - Un Authorized Access"
            }
        )
    
    return templates.TemplateResponse(
        request=request, 
        name="password_strength.html", 
        context={
            "title": "Password_Manager_Pro", 
            "name": "P-M-P"
        }
    )


@router.post('/api/passwords_strength')
async def password_strength_api(request: Request):
    """API endpoint - analyzes password strength and entropy."""
    json_data = await request.json()
    password = json_data.get("password")

    stren = strength(password)
    entropy = stren[0]
    time_score = retime(stren[1])

    spcr = 0 
    if time_score[1] >= 1:
        spcr = float(f"0.{str(int(entropy))}")

    score = round(((time_score[1] * 10) + spcr), 2)
    
    colour = round((((score - 1) / 99) * 256))
    
    return JSONResponse(content={
        "entropy": entropy,
        "time_score": min(score, 100),
        "est_time": time_score[0],
        "colour": colour
    })


@router.get("/hash_password")
def get_hash_passwords(request: Request):
    """Hash password page - GET request."""
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "title": "Password_Manager_Pro", 
                "name": "P-M-P", 
                "error": "401 - Un Authorized Access"
            }
        )
    
    return templates.TemplateResponse(
        request=request, 
        name="hash_password.html", 
        context={
            "title": "Password_Manager_Pro", 
            "name": "P-M-P"
        }
    )


@router.post('/hash_password')
async def hash_password(
    request: Request, 
    password: Annotated[str, Form()], 
    algorithm: Annotated[str, Form()]
):
    """Hash password - generates hash using specified algorithm."""
    if not request.session.get("user_id"):
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "title": "Password_Manager_Pro", 
                "name": "P-M-P", 
                "error": "401 - Un Authorized Access"
            }
        )
    
    head = f"{algorithm} Hash ==> "
    stren = hasher(password, algorithm.replace("-", ""))

    return templates.TemplateResponse(
        request=request, 
        name="hash_password.html", 
        context={
            "title": "Password_Manager_Pro", 
            "name": "P-M-P",  
            "eval": [head, stren]
        }
    )


@router.get("/verifyHash")
def get_verify_hash(request: Request):
    """Verify hash page - GET request."""
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": "401 - Un Authorized Access"}
        )
    
    return templates.TemplateResponse(
        request=request, 
        name="verify_hash.html", 
        context={
            "title": "Password_Manager_Pro", 
            "name": "P-M-P"
        }
    )


@router.post('/verifyHash')
async def verify_hash(
    request: Request, 
    password: Annotated[str, Form()],
    phash: Annotated[str, Form()], 
    algorithm: Annotated[str, Form()]
):
    """Verify hash - compares password against hash with specified algorithm."""
    user_id = request.session.get("user_id")
    if not user_id:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": "401 - Un Authorized Access"}
        )

    if algorithm.strip() not in ["SHA-224", "SHA-256", "SHA-384", "SHA-512"]:
        return templates.TemplateResponse(
            request=request, 
            name="verify_hash.html", 
            context={
                "title": "Password_Manager_Pro", 
                "name": "P-M-P",  
                "eval": "Invalid Algorithm"
            }
        )

    stren = verify(phash, password, algorithm.replace("-", ""))
    result = "Matched !" if stren else "Did Not Match"
    
    return templates.TemplateResponse(
        request=request, 
        name="verify_hash.html", 
        context={
            "title": "Password_Manager_Pro", 
            "name": "P-M-P", 
            "eval": result
        }
    )
