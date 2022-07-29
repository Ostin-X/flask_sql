from src.course_sql.extensions.extensions import app, db_location
from src.course_sql.routes.api import *


def create_app():
    app.register_blueprint(api_bp)
    # db.init_app(app)
    return app


if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = db_location
    db.init_app(app)
    app = create_app()
    print(db_location.split('/')[-1])
    app.run(debug=True, port=5000, host='127.0.0.1')
