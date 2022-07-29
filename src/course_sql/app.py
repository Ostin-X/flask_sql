from src.course_sql.extensions.extensions import app
from src.course_sql.routes.api import *


def create_app():
    app.register_blueprint(api_bp)
    # db.init_app(app)
    return app


if __name__ == '__main__':
    db.init_app(app)
    app = create_app()
    app.run(debug=True, port=5000, host='127.0.0.1')
