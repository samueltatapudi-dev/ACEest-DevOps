from .flaskapp import create_app

# Expose a Flask app object for tests: `from app import app`
app = create_app()

