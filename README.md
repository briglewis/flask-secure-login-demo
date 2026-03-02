
# 🔐 Flask Secure Login Application

A security-focused Flask authentication application demonstrating defensive controls aligned with modern web security best practices and OWASP guidance.

This project implements secure authentication, session management, brute-force protection, CSRF protection, and HTTP security hardening.

---

## 🚀 Features

* User authentication (Flask-Login)
* Secure password hashing (Werkzeug)
* CSRF protection (Flask-WTF)
* Rate limiting (Flask-Limiter)
* Account lockout after failed logins
* Secure session cookie configuration
* Open redirect prevention
* SQL injection prevention via SQLAlchemy ORM
* Security headers via Flask-Talisman
* Custom 429 rate limit error handling

---

## 🛡 Security Controls Implemented

| Control                  | Threat Mitigated           |
| ------------------------ | -------------------------- |
| CSRF tokens              | Cross-Site Request Forgery |
| Password hashing         | Credential disclosure      |
| Generic login errors     | Username enumeration       |
| Input validation         | DoS / injection attempts   |
| SQLAlchemy ORM           | SQL injection              |
| Login rate limiting      | Brute force attacks        |
| Account lockout          | Targeted brute force       |
| Secure cookies           | Session theft              |
| CSP + security headers   | XSS / Clickjacking         |
| Authentication guards    | Forced browsing            |
| Open redirect validation | Redirect abuse             |

See `SUBMISSION.md` for detailed explanations and testing steps.

---

# 🧰 Tech Stack

* Python 3.14
* Flask
* Flask-Login
* Flask-WTF
* Flask-Migrate
* Flask-Limiter
* Flask-Talisman
* SQLAlchemy
* SQLite (development)

---

# 📦 Project Structure

```
flaskLoginApp/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── templates/
│   └── static/
│
├── migrations/
├── instance/
├── config.py
├── micrologin.py
├── requirements.txt
└── README.md
```

---

# 🖥 How to Run Locally

## 1️⃣ Clone Repository

```bash
git clone https://github.com/briglewis/flask-secure-login-demo.git
cd YOUR_REPO
```

---

## 2️⃣ Create Virtual Environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file:

```bash
touch .env
```

Add:

```
SECRET_KEY=replace_with_secure_random_value
FLASK_ENV=development
```

Generate a secure key:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

⚠️ Do not commit `.env` to version control.

---

## 5️⃣ Run Database Migrations

```bash
python3 -m flask --app micrologin db upgrade
```

This creates:

```
instance/app.db
```

---

## 6️⃣ Start Development Server

```bash
python3 -m flask --app micrologin run --debug
```

Open:

```
http://127.0.0.1:5000
```

---

# 🔎 Testing Security Controls

### Brute Force Protection

* Attempt more than 5 failed logins within one minute
* Receive HTTP 429 response

### Account Lockout

* Fail login 5 times
* Account locks for 15 minutes

### CSRF Protection

* Remove CSRF token via DevTools → request fails

### Open Redirect Protection

Try:

```
/login?next=http://evil.com
```

Redirect should default to dashboard.

### Session Cookie Flags

Inspect cookies:

* HttpOnly
* Secure (in production)
* SameSite=Lax

### Security Headers

Inspect response headers for:

* Content-Security-Policy
* Strict-Transport-Security (production)
* X-Frame-Options

---

# ⚠️ Production Notes

For production deployment:

* Use a strong `SECRET_KEY`
* Use HTTPS
* Use Redis for Flask-Limiter storage
* Use PostgreSQL instead of SQLite
* Disable debug mode
* Set `FLASK_ENV=production`
* Enforce HSTS

---

# 📄 Submission

Please see `SUBMISSION.md` for:

* Design decisions
* Threat model considerations
* Security implementation details
* Testing methodology

---

# 📚 Security Alignment

This project mitigates risks aligned with:

* OWASP Top 10 (2025)
* Authentication and session management best practices
* Defense-in-depth principles

---

# 📬 License

This project is provided for educational and demonstration purposes.