from src.course_sql.config import db


class GroupModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), unique=True, nullable=False)
    students = db.relationship("StudentModel", backref="students")

    def __repr__(self):
        return f'<group {self.id}>'


student_course_association = db.Table('student_course_association',
                                      db.Column('course_id', db.Integer, db.ForeignKey('course_model.id'),
                                                primary_key=True),
                                      db.Column('student_id', db.Integer, db.ForeignKey('student_model.id'),
                                                primary_key=True)
                                      )


class CourseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(100))

    def __repr__(self):
        return f'<group {self.id}>'


class StudentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group_model.id'), nullable=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    # studying = db.relationship('StudentCourseAssociation', backref='studied')
    studying = db.relationship('CourseModel', secondary=student_course_association, backref='studied')

    def __repr__(self):
        return f'<group {self.id}>'
