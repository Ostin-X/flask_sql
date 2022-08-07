from src.course_sql.extensions.extensions import app
from src.course_sql.routes.api import api_bp, db
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    app.register_blueprint(api_bp)
    db.init_app(app)

    swagger_url = '/swagger'
    api_url = '/static/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={
            'app_name': 'Flask SQL'
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)

    return app


if __name__ == '__main__':
    app.config.from_object('extensions.config.ProdConfig')
    app = create_app()
    app.run()
