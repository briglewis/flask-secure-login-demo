from datetime import datetime
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

class User(UserMixin, db.Model):
    """User account model for authentication and login management."""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))

    failed_logins: so.Mapped[int] = so.mapped_column(default=0)
    
    lockout_until: so.Mapped[Optional[datetime]] = so.mapped_column(nullable=True)

    def set_password(self, password):
        """Hash and store the user's password securely."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify a password attempt against the stored hash."""
        return check_password_hash(self.password_hash, password)


"""Callback for Flask-Login to load a user from the session"""
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

