submission.md 1

# Submission

I chose Flask as I've built a small app in Flask before and Python is the quickest language for me to build in.

My first step was to created a list of web app vulns, particularly around login forms. 

I then chose the ones I thought I could create defenses against in the small time I had to build, test and ship it to you.


## Defensive Measures Implemented

- CSRF token to prevent Cross-Site Request Forgery attacks.
- Username max length validation to prevent DoS attacks
- Password mininum and maximum chars validation to prevent brute force and DoS attacks
- Password hashing to avoid storing password in plaintext 
- Generic error messages on failed login to prevent username enumeration
- Authentication on all pages to prevent forced browsing
- Parameterised queries for SQL callsby default using SQLAlchemy
- Basic HTTP security headers to prevent XSS and clickjacking
- Cookies with cookie flags set to prevent CSRF and XSS
- Input validation on the client side and server side to prevent SQLi and XSS attacks.
- Rate-limiting by IP and username to prevent brute force attacks 


## Tech used

- Password hashing (Werkzeug)
- CSRF protection (Flask-WTF)
- Rate limiting (Flask-Limiter)
- Account lockout after failed logins
- Open redirect prevention for `next` parameter
- Secure session cookie settings
- Security headers (Flask-Talisman)
- POST-only logout with CSRF

## Recommendations for future hardening 

- Session expiration
- TLS so HTTPS in prod
- Logging and monitoring
- Log rate limiting
- MFA 
- Captcha
- Password checks against known weak passwords when they are being set / reset.
- Password reset
- HSTS header and Secure Cookie flag when served over HTTPS
- WAF

## AI services and models used

I have a chatbot I created a few years ago for my pen testing work called Hacky McHack Face. It uses Open AIs 5.2 model. I used this to troubleshoot my code and sanity check the choices I made re my security controls. I also used it to create parts of my README.md and this file, SUBMISSION.md 

I wrote my code in Visual Studio and had Co-Pilot version
0.37.9 enabled.

When ChatGPT got laggy I switched to a free version of Claude using Sonnet 4.6.


## How I implemented my security controls

1. CSRF Protection (Flask-WTF)

Mitigates:

Cross-Site Request Forgery (CSRF)

Implementation:

All forms use FlaskForm

{{ form.hidden_tag() }} includes CSRF token

Logout is POST-only and CSRF-protected

How to Test:

Remove the CSRF token from a form submission using DevTools → request should fail.

Attempt cross-site POST → request should be rejected.

2. Input Validation (Length + Format Controls)

Mitigates:

Denial of Service (DoS) via oversized payloads

Injection attempts

Malformed input

Implementation:

Username maximum length enforced

Password minimum and maximum length enforced

Email validation enabled

Server-side validation via WTForms (never trust client-side validation)

How to Test:

Attempt to submit overly long usernames/passwords.

Attempt invalid email formats.

3. Password Hashing

Mitigates:

Credential disclosure if database is compromised

Implementation:

Passwords hashed using Werkzeug generate_password_hash

Verified using check_password_hash

No plaintext passwords stored

How to Test:

Inspect database — password column contains hash, not plaintext.

4. Generic Authentication Errors

Mitigates:

Username enumeration

Implementation:

Login failure message is always:

"Your email or password is incorrect."

No distinction between unknown user and bad password

How to Test:

Attempt login with:

Valid email + wrong password

Invalid email
→ Same error message should be shown.

5. Authentication Required on Protected Routes

Mitigates:

Forced browsing / unauthorized access

Implementation:

@login_required applied to protected routes

login.login_view configured

How to Test:

Attempt direct access to /dashboard while not logged in.

Should redirect to login page with ?next= parameter.

6. Parameterized Queries (SQLAlchemy ORM)

Mitigates:

SQL Injection (SQLi)

Implementation:

All DB calls use SQLAlchemy ORM:

sa.select(User).where(User.email == form.email.data.lower())

No raw SQL string concatenation

How to Test:

Attempt SQL injection payload in login form.

Query should not break or return unintended results.

7. HTTP Security Headers (Flask-Talisman)

Mitigates:

XSS

Clickjacking

Implementation:

Content Security Policy (CSP)


Secure header enforcement

How to Test:

Inspect response headers in browser DevTools.

Confirm CSP and other security headers are present.

8. Secure Session Cookie Configuration

Mitigates:

XSS session theft

CSRF

Cookie interception

Implementation:

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = True (in prod)

SESSION_COOKIE_SAMESITE = 'Lax'

How to Test:

Inspect session cookie in DevTools → confirm flags are set.

9. Rate Limiting (Flask-Limiter)

Mitigates:

Brute force attacks

Credential stuffing

Implementation:

IP-based rate limiting:

@limiter.limit("5 per minute")

Account lockout after 5 failed login attempts

15-minute temporary lockout window

How to Test:

Attempt 5 failed logins in 1 minute - app returns 429 Too Many Requests error.

Trigger account lockout and you will get blocked for 15 minutes.

10. Account Lockout Logic

Mitigates:

Targeted brute force attacks against specific accounts

Implementation:

failed_logins counter in DB

lockout_until timestamp

Reset on successful login

How to Test:

Fail login 5 times and your account gets locked.

Wait or reset DB to restore access.


------------------------------------------------


Hope to speak soon! 

Cheers

Brig Lewis
