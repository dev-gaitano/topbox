from .auth.routes import auth_bp
from .companies.routes import companies_bp


def register_blueprints(app):
    app.register_blueprint(companies_bp, url_prefix="/api/companies")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
