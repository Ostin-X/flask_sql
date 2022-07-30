from src.course_sql.extensions.extensions import app
from src.course_sql.routes.api import api_bp, db


def create_app():
    app.register_blueprint(api_bp)
    # app.config.from_object('extensions.config.ProdConfig')
    db.init_app(app)
    return app


if __name__ == '__main__':
    app.config.from_object('extensions.config.ProdConfig')
    app = create_app()
    app.run()
