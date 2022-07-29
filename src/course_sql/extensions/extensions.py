from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_location = 'postgresql://ASP:qwe@localhost/coursessql'
db_test_location = 'postgresql://postgres:scxscx@localhost/test_coursessql'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ASP:qwe@localhost/coursessql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
