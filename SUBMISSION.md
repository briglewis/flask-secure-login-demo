# 🔐 Submission

## 📌 Overview

I chose Flask for this project because I have prior experience building small applications with it, and Python allows me to rapidly prototype secure functionality.

My initial step was to identify common web application vulnerabilities — particularly those affecting authentication and login workflows. I then prioritised controls that could be realistically implemented, tested, and validated within the time available.

This submission focuses on practical, defensive security controls aligned with modern web security best practices and OWASP guidance.

---

# 🛡 Defensive Measures Implemented

* CSRF protection to prevent Cross-Site Request Forgery
* Username length validation to reduce DoS risk
* Password minimum and maximum length validation
* Secure password hashing (no plaintext storage)
* Generic authentication error messages to prevent username enumeration
* Authentication enforcement on protected routes
* Parameterised queries via SQLAlchemy ORM
* HTTP security headers (CSP, clickjacking protection)
* Secure session cookie configuration
* Client-side and server-side input validation
* Rate limiting and account lockout to mitigate brute force attacks

---

# 🧰 Technologies Used

* Flask
* Flask-Login (authentication/session management)
* Flask-WTF (CSRF + form validation)
* Flask-Limiter (rate limiting)
* Flask-Talisman (security headers)
* SQLAlchemy (ORM / SQL injection prevention)
* Werkzeug (password hashing utilities)

---

# 🚀 How I Implemented the Security Controls

---

## 1️⃣ CSRF Protection (Flask-WTF)

**Mitigates:**
Cross-Site Request Forgery (CSRF)

**Implementation:**

* All forms inherit from `FlaskForm`
* `{{ form.hidden_tag() }}` injects a CSRF token
* Logout is POST-only and CSRF-protected

**How to Test:**

* Remove CSRF token via DevTools → request fails
* Attempt cross-site POST → request rejected

---

## 2️⃣ Input Validation (Length + Format Controls)

**Mitigates:**

* Denial of Service via oversized payloads
* Injection attempts
* Malformed input

**Implementation:**

* Username maximum length enforced
* Password minimum and maximum length enforced
* Email format validation enabled
* Server-side validation via WTForms (client-side validation is never trusted)

**How to Test:**

* Submit overly long usernames/passwords
* Submit invalid email formats

---

## 3️⃣ Password Hashing

**Mitigates:**
Credential disclosure in the event of database compromise

**Implementation:**

* Passwords hashed using `generate_password_hash`
* Verified using `check_password_hash`
* No plaintext passwords stored

**How to Test:**

* Inspect database → password column contains hashes, not plaintext

---

## 4️⃣ Generic Authentication Errors

**Mitigates:**
Username enumeration

**Implementation:**

* Login failure message is always:

  > "Your email or password is incorrect."

* No distinction between unknown user and incorrect password

**How to Test:**

* Valid email + wrong password
* Invalid email
  → Same error message returned

---

## 5️⃣ Authentication Required on Protected Routes

**Mitigates:**
Forced browsing / unauthorised access

**Implementation:**

* `@login_required` applied to protected routes
* `login.login_view` configured

**How to Test:**

* Attempt direct access to `/dashboard` while not authenticated
* Should redirect to login page with `?next=` parameter

---

## 6️⃣ Parameterised Queries (SQLAlchemy ORM)

**Mitigates:**
SQL Injection (SQLi)

**Implementation:**

* All database queries use SQLAlchemy ORM:

```python
sa.select(User).where(User.email == form.email.data.lower())
```

* No raw SQL string concatenation

**How to Test:**

* Attempt SQL injection payload in login form
* Query should not break or return unintended results

---

## 7️⃣ HTTP Security Headers (Flask-Talisman)

**Mitigates:**

* Cross-Site Scripting (XSS)
* Clickjacking

**Implementation:**

* Content Security Policy (CSP)
* Secure header enforcement

**How to Test:**

* Inspect response headers in DevTools
* Confirm CSP and other headers are present

---

## 8️⃣ Secure Session Cookie Configuration

**Mitigates:**

* XSS session theft
* CSRF abuse
* Cookie interception

**Implementation:**

```python
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # In production
SESSION_COOKIE_SAMESITE = 'Lax'
```

**How to Test:**

* Inspect session cookie in DevTools
* Confirm flags are correctly set

---

## 9️⃣ Rate Limiting (Flask-Limiter)

**Mitigates:**

* Brute force attacks
* Credential stuffing

**Implementation:**

* IP-based rate limiting:

```python
@limiter.limit("5 per minute")
```

* Account lockout after 5 failed login attempts
* 15-minute temporary lockout window

**How to Test:**

* Attempt 5 failed logins within one minute → receive HTTP 429
* Trigger account lockout → blocked for 15 minutes

---

## 🔟 Account Lockout Logic

**Mitigates:**
Targeted brute force attacks against specific accounts

**Implementation:**

* `failed_logins` counter stored in database
* `lockout_until` timestamp enforced
* Counters reset on successful login

**How to Test:**

* Fail login 5 times which should trigger account lock
* Wait for lockout window or reset database

---

# 🔮 Recommendations for Future Hardening

* Session expiration and rotation
* Enforced HTTPS in production
* Centralised logging and monitoring
* Structured security logging for rate limits
* Multi-Factor Authentication (MFA)
* CAPTCHA on repeated failures
* Password checks against known compromised password lists
* Secure password reset workflow
* Full HSTS enforcement in production
* Web Application Firewall (WAF)

---

# 🤖 AI Tools Used

I used a personal security-focused chatbot I developed for penetration testing support. It leverages OpenAI’s GPT-5.2 model. I used it to:

* Troubleshoot implementation issues
* Sanity check defensive control choices
* Refine documentation (README and SUBMISSION)

I developed the code in Visual Studio Code with GitHub Copilot enabled (v0.37.9).

When performance issues occurred, I temporarily used Claude Sonnet 4.6 (free tier) for additional debugging support.

---

# 📚 Security Alignment

This project aligns with:

* OWASP Top 10
* Authentication & Session Management best practices
* Defense-in-depth principles
* Secure SDLC thinking

---

Hope to speak soon.

Cheers,
**Brig Lewis**

---
