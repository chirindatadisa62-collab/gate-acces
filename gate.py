from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Use environment variable for database URL, fallback to SQLite for local development
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # For production (PostgreSQL on Railway/Render)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # For local development (SQLite)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gate.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    fee_cleared = db.Column(db.Boolean, default=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        student_number = request.form['student_number']
        return redirect(url_for('check_access', student_number=student_number))
    return render_template('index.html')

@app.route('/check/<student_number>')
def check_access(student_number):
    print(f"DEBUG: Processing student number: {student_number}")  # Debug log

    student = Student.query.filter_by(student_number=student_number).first()
    if student:
        print(f"DEBUG: Found student: {student.name}, Fee cleared: {student.fee_cleared}")  # Debug log
        if student.fee_cleared:
            message = f"Access granted for {student.name} (Student Number: {student.student_number})"
            access = True
        else:
            message = f"Access denied. Fees not cleared for {student.name} (Student Number: {student.student_number})"
            access = False
    else:
        print(f"DEBUG: Student {student_number} not found")  # Debug log
        message = f"Student number {student_number} not found."
        access = False

    response = render_template('result.html', message=message, access=access, debug_student_number=student_number)
    # Add cache control headers to prevent browser caching
    response = app.make_response(response)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    # Get port from environment variable (for hosting services)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
