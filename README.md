# 🔐 Password Manager Pro

> A secure, full-stack password manager built with **FastAPI**, focused on encryption, performance, and clean UI.

---
---
### Try in Github Codespaces
 [![Try in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/codeyy/Password-Manager-PRO)

Note: This environment is for demonstration purposes. Data stored in this session is ephemeral and will be deleted when the Codespace is closed.
```
Codespace creation can take upto 3-4 minutes.
after which the web app will start automatically

Incase you have popups disabled in your browser
You will have to go to " PORTS " bellow,
Then find port named "App Preview (8000)"
and ctrl+click the url nest to it,
to manually start the web-application
```
---
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

### 🐳 Run with Docker (Recommended)
> The fastest way to get the app running without manual configuration.

#### Option 1: Docker Compose (One-Click Setup)
```
If you want a truly "plug and play" experience that handles port mapping and database persistence automatically:

Open your terminal in the project root.

Run the command:

Bash
docker compose up -d
Open your browser to http://localhost:8000.
```

#### Option 2: Docker Desktop GUI
```
If you prefer using the Docker Desktop interface:

Go to the Images tab and click the Run icon on password-manager-pro.

Crucial: Click on Optional Settings.

In the Host Port field, enter 8000.

Click Run and access the app at localhost:8000.
```

```
Note: The app is configured to listen on 0.0.0.0 inside the container. If you encounter a connection error, ensure your Host Port is mapped to 8000.
```


### With source code

#### 1️⃣ Clone the repository

```bash
git clone https://github.com/codeyy/Password-Manager-PRO
cd Password-Manager-PRO
```

#### 2️⃣ Create a virtual environment

```bash
python -m venv venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
```

#### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

#### 4️⃣ Run the application

```bash
uvicorn app.main:app
Note: run this from root directory only i.e. Password-Manager-PRO
```

#### 5️⃣ Then open:

```
http://localhost:8000/
in your browser
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
