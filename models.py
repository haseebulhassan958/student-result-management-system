from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    results = db.relationship('Result', backref='student', lazy=True)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    marks_obtained = db.Column(db.Float, nullable=False)
    total_marks = db.Column(db.Float, nullable=False)
    semester = db.Column(db.String(20), nullable=False)

    @property
    def percentage(self):
        return (self.marks_obtained / self.total_marks) * 100

    @property
    def grade(self):
        p = self.percentage
        if p >= 90: return 'A+'
        elif p >= 80: return 'A'
        elif p >= 70: return 'B'
        elif p >= 60: return 'C'
        elif p >= 50: return 'D'
        else: return 'F'