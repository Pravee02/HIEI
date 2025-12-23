from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
# Trigger deployment update

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hiei.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret')

from models import db
db.init_app(app)

from routes.auth_routes import auth_bp
from routes.inflation_routes import inflation_bp
from routes.data_routes import data_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(inflation_bp, url_prefix='/api/inflation')
app.register_blueprint(data_bp, url_prefix='/api/data')

# Ensure DB tables exist (Required for Render/Gunicorn)
# Render Ephemeral Disk: SQLite will reset on deploy, but need to ensure path exists.
db_file_path = os.path.join(basedir, 'hiei.db')
print(f"Database Path: {db_file_path}")

with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")

@app.route('/')
def home():
    return {"message": "HIEI Backend Running"}

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000)
