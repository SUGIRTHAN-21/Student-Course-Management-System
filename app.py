from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
import sqlite3
import hashlib
import os
from models import User, Course, Enrollment

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('login'))
        if session.get('user_role') != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user_model = User()
        user = user_model.get_user_by_email(email)
        
        if user:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == user['password']:
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_email'] = user['email']
                session['user_role'] = user['role']
                
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
        
        flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
            
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        user_model = User()
        if user_model.get_user_by_email(email):
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        user_id = user_model.create_user(name, email, hashed_password, 'student')
        
        if user_id:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    enrollment_model = Enrollment()
    enrollments = enrollment_model.get_user_enrollments(session['user_id'])
    
    return render_template('dashboard.html', 
                          enrollments=enrollments, 
                          user_name=session['user_name'])

@app.route('/courses')
@login_required
def courses():
    course_model = Course()
    enrollment_model = Enrollment()
    
    all_courses = course_model.get_all_courses()
    
    # Debugging statement
    print("DEBUG: Courses fetched from DB:", all_courses)
    
    enrolled_courses = enrollment_model.get_enrolled_course_ids(session['user_id'])
    
    return render_template('courses.html', 
                          courses=all_courses, 
                          enrolled_courses=enrolled_courses,
                          is_admin=(session.get('user_role') == 'admin'))

@app.route('/enroll/<int:course_id>')
@login_required
def enroll(course_id):
    enrollment_model = Enrollment()
    
    if enrollment_model.is_enrolled(session['user_id'], course_id):
        flash('You are already enrolled in this course', 'warning')
    else:
        if enrollment_model.create_enrollment(session['user_id'], course_id):
            flash('Enrollment successful!', 'success')
        else:
            flash('Enrollment failed. Please try again.', 'danger')
    
    return redirect(url_for('courses'))

@app.route('/unenroll/<int:course_id>')
@login_required
def unenroll(course_id):
    enrollment_model = Enrollment()
    
    if enrollment_model.delete_enrollment(session['user_id'], course_id):
        flash('Course unenrolled successfully', 'success')
    else:
        flash('Unenrollment failed. Please try again.', 'danger')
    
    return redirect(url_for('courses'))

@app.route('/course/add', methods=['GET', 'POST'])
@admin_required
def add_course():
    if request.method == 'POST':
        course_code = request.form['course_code']
        title = request.form['title']
        description = request.form['description']
        credits = int(request.form['credits'])
        
        course_model = Course()
        
        if course_model.get_course_by_code(course_code):
            flash('Course code already exists', 'danger')
            return redirect(url_for('courses'))
        
        if course_model.create_course(course_code, title, description, credits):
            flash('Course added successfully', 'success')
        else:
            flash('Failed to add course. Please try again.', 'danger')
        
        return redirect(url_for('courses'))
    
    return render_template('add_course.html')

@app.route('/course/edit/<int:course_id>', methods=['POST'])
@admin_required
def edit_course(course_id):
    if request.method == 'POST':
        course_code = request.form['course_code']
        title = request.form['title']
        description = request.form['description']
        credits = int(request.form['credits'])
        
        course_model = Course()
        
        if course_model.update_course(course_id, course_code, title, description, credits):
            flash('Course updated successfully', 'success')
        else:
            flash('Failed to update course. Please try again.', 'danger')
    
    return redirect(url_for('courses'))

@app.route('/course/delete/<int:course_id>')
@admin_required
def delete_course(course_id):
    course_model = Course()
    
    if course_model.delete_course(course_id):
        flash('Course deleted successfully', 'success')
    else:
        flash('Failed to delete course. Please try again.', 'danger')
    
    return redirect(url_for('courses'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# Debugging route to check database courses
@app.route('/test_courses')
def test_courses():
    course_model = Course()
    courses = course_model.get_all_courses()
    return jsonify([{ "code": c[0], "name": c[1], "credits": c[3] } for c in courses])

if __name__ == '__main__':
    app.run(debug=True)
