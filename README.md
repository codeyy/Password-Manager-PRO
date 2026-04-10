# 🔐 Password Manager Pro

> A secure, full-stack password manager built with **FastAPI**, focused on encryption, performance, and clean UI.

---
##
 [![Try in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/codeyy/Password-Manager-PRO)

Note: This environment is for demonstration purposes. Data stored in this session is ephemeral and will be deleted when the Codespace is closed.
```
Codespace creation can take upto 3-4 minutes.
after which the web app will start automatically

Incase you have popups disabled
you will have to go to ``ports`` bellow, then find port named ``App Preview (8000)`` and ctrl click the url to manually start the web app
```
---

## 🏷️ Tags

`fastapi` `python` `cybersecurity` `encryption` `password-manager` `sqlite` `sqlalchemy` `jinja2` `aes` `pbkdf2`

---

## 🚀 Overview

Password Manager Pro is a **secure web application** that allows users to register, authenticate, and manage their credentials safely. All sensitive data is encrypted before storage using strong cryptographic practices.

Designed with both **security and performance in mind**, the application handles large datasets efficiently while maintaining a clean, modern interface.

---

## ⚡ Features

* **User Authentication** — Session-based login system using secure middleware
* **Strong Key Derivation** — PBKDF2-HMAC with **`600,000 iterations`**
* **AES Encryption (Fernet)** — Passwords encrypted before storage
* **Password Management** — Add, view, and delete credentials
* **Password Strength Checker** — Built-in analysis tool
* **Modern UI** — Glassmorphism + cyber-style interface with animations
* **Persistent Sessions** — Users stay logged in securely
* **API + Web Hybrid** — REST endpoints + Jinja-rendered frontend

---

## 🧠 Tech Stack

### Backend

* **FastAPI** (core framework)
* **Uvicorn** (ASGI server)
* **SQLAlchemy** (ORM)
* **itsdangerous / werkzeug** (security utilities)

### Frontend

* **Jinja2 Templates**
* **HTML, CSS, JavaScript**

### Security

* **cryptography (Fernet / AES)**
* **PBKDF2-HMAC (600k iterations)**

### Database

* **SQLite3**

---

## 🏗️ Architecture

* FastAPI with modular **routers** for separation of concerns
* Jinja templates rendered server-side
* Secure encryption layer via `security.py`
* SQLite database managed through SQLAlchemy ORM

---

## 🔗 Routes / Endpoints

### Auth

* `/login`
* `/logout`
* `/register`
* `/api/checkUsername`

### Core App

* `/`
* `/passwords`
* `/add-password`
* `/del-password`
* `/del_passwords_fromPasswords`

### Utilities

* `/api/passwords_strength`
* `/passwords_strength`
* `/hash_password`
* `/verifyHash`

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/codeyy/Password-Manager-PRO
cd Password-Manager-PRO
```

### 2️⃣ Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the application

```bash
uvicorn app.main:app
Note: run this from root directory only i.e. Password-Manager-PRO
```

Then open:

```
http://localhost:8000/
```

---

## 🔑 Security Design

* Passwords are **never stored in plaintext**
* Encryption handled using **Fernet (AES-based symmetric encryption)**
* Keys derived using **PBKDF2-HMAC with 600,000 iterations**
* Each user has a uniquely derived encryption key
* Session-based authentication using secure middleware

---

## 🧪 Performance

* Tested with **1000+ stored passwords**
* Minimal latency under load
* Efficient database queries via SQLAlchemy

---

## 🧠 Learning Outcomes

This project demonstrates:

* Building full-stack apps using FastAPI
* Designing secure authentication systems
* Implementing encryption & key derivation properly
* Structuring scalable backend systems with routers
* Creating polished UI with modern CSS techniques

---

## 🧑‍💻 Author

-**`Agam Kumar`**

[GitHub](https://github.com/codeyy)

---
