from .companies.routes import companies_bp


def register_blueprints(app):
    app.register_blueprint(companies_bp, url_prefix="/api/companies")
