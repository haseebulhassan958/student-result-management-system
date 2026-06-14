from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Student, Result
from predictor import predict_grade

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey123'

db.init_app(app)

# Database tables creation
with app.app_context():
    db.create_all()

# ── Routes ──────────────────────────────────────

# Home page
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Add student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student = Student(
            name=request.form['name'],
            roll_number=request.form['roll_number'],
            class_name=request.form['class_name']
        )
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_student.html')

# Add result
@app.route('/add_result/<int:student_id>', methods=['GET', 'POST'])
def add_result(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        result = Result(
            student_id=student_id,
            subject=request.form['subject'],
            marks_obtained=float(request.form['marks_obtained']),
            total_marks=float(request.form['total_marks']),
            semester=request.form['semester']
        )
        db.session.add(result)
        db.session.commit()
        flash('Result added successfully!', 'success')
        return redirect(url_for('student_detail', student_id=student_id))
    return render_template('add_result.html', student=student)

# Student detail + AI prediction
@app.route('/student/<int:student_id>')
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    results = Result.query.filter_by(student_id=student_id).all()
    prediction = None
    if results:
        prediction = predict_grade(results)
    return render_template('student_detail.html', student=student, results=results, prediction=prediction)

# Delete student
@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    Result.query.filter_by(student_id=student_id).delete()
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'danger')
    return redirect(url_for('index'))

# Student edit karo
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.roll_number = request.form['roll_number']
        student.class_name = request.form['class_name']
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('student_detail', student_id=student_id))
    return render_template('edit_student.html', student=student)

# Delete result
@app.route('/delete_result/<int:result_id>')
def delete_result(result_id):
    result = Result.query.get_or_404(result_id)
    student_id = result.student_id
    db.session.delete(result)
    db.session.commit()
    flash('Result deleted successfully!', 'danger')
    return redirect(url_for('student_detail', student_id=student_id))

# Search student by roll number
@app.route('/search', methods=['GET', 'POST'])
def search():
    student = None
    error = None
    if request.method == 'POST':
        roll_number = request.form['roll_number'].strip()
        student = Student.query.filter_by(roll_number=roll_number).first()
        if not student:
            error = f'No student found with roll number: {roll_number}'
    return render_template('search.html', student=student, error=error)

if __name__ == '__main__':
    app.run(debug=True)