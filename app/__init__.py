from flask import Flask
from config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_talisman import Talisman
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

#Create instance folder if it doesn't exist for SQLite database and other instance files
os.makedirs(app.instance_path, exist_ok=True)

csp = {
    'default-src': "'self'",
    'style-src': "'self'",
    'script-src': "'self'",
}#Add security headers, enforce HTTPS in prod. In dev allow HTTP for local testing
Talisman(
    app,
    force_https=os.environ.get('FLASK_ENV') == 'production',
    strict_transport_security=os.environ.get('FLASK_ENV') == 'production',
    strict_transport_security_max_age=31536000,
    content_security_policy = csp
    )

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app) 
login.login_view = 'login'

# --- Context processor to inject forms into templates ---
@app.context_processor
def inject_forms():
    from app.forms import EmptyForm
    return {'logout_form': EmptyForm()}

from app import routes, models, errors 
