from src.course_sql.config import app
from src.course_sql.api.routes import *


def create_app():
    app.register_blueprint(api_bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host='127.0.0.1')
