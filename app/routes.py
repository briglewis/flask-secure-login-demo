from app import app, db, limiter
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm
from flask_login import current_user, login_user
import sqlalchemy as sa
from app.models import User
from flask_login import login_required, logout_user
from urllib.parse import urlsplit
from datetime import datetime, timedelta

@app.get("/_debug/context")
def debug_context():
    ctx = {}
    app.update_template_context(ctx)
    return {
        "has_logout_form": "logout_form" in ctx,
        "keys_sample": sorted(list(ctx.keys()))[:20]
    }

@app.route('/', methods=['GET', 'POST'])
def home():
     return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()

    if form.validate_on_submit():
        user= db.session.scalar(
            sa.select(User).where(User.email == form.email.data.lower()))
        
        """sanity checks to verify user lookup and password check are working as expected"""
        print("user:", user)
        print("password ok:", user and user.check_password(form.password.data))

        # --- Account lockout check ---
        if user and user.lockout_until and user.lockout_until > datetime.utcnow():
            flash("Account temporarily locked. Try again later.")
            return redirect(url_for('login'))
        
        # --- Failed login ---
        if user is None or not user.check_password(form.password.data):
            if user:
                user.failed_logins += 1

                if user.failed_logins >= 5:
                    user.lockout_until = datetime.utcnow() + timedelta(minutes=15)

                db.session.commit()

            flash('Your email or password is incorrect.')
            return redirect(url_for('login'))

        # --- Successful login ---
        user.failed_logins = 0
        user.lockout_until = None
        db.session.commit()

        login_user(user)

        next_page = request.args.get('next')
        if next_page:
            parts = urlsplit(next_page)
            if parts.scheme or parts.netloc or not next_page.startswith('/'):
                next_page = None

        return redirect(next_page or url_for('dashboard'))

    return render_template('login.html', title='Sign in', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Welcome')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('429.html', error=e), 429