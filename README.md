Flask-based Student Course Management System with MySQL as the database. The project should support CRUD operations, authentication (password hashing), and course enrollments. Follow the structure below and provide the necessary Python, HTML, and CSS files. Keep JavaScript inside the HTML files. The application should have separate CSS files for styling each HTML page.

### **Project Structure & Functionality**  

```
StudentCourseManagement/
│── app.py                      # Main Flask application with route handling
│── config.py                   # Stores database configuration (MySQL credentials)
│── requirements.txt             # List of required Python dependencies
│── static/
│   │── css/
│   │   │── login.css            # Styles for login page
│   │   │── register.css         # Styles for registration page
│   │   │── dashboard.css        # Styles for dashboard page
│   │   │── courses.css          # Styles for courses page
│── templates/
│   │── base.html                # Common layout with navbar
│   │── login.html               # User login form with password hashing
│   │── register.html            # User registration form (stores hashed password)
│   │── dashboard.html           # Student dashboard showing enrolled courses
│   │── courses.html             # Page listing available courses (CRUD for admin)
│── models.py                    # Database models for Users, Courses, Enrollments
│── db_init.py                   # Initializes DB, creates tables, adds sample data
│── README.md                     # Documentation on how to run the project
```

### **Page-wise Functionalities:**
1. **`app.py` (Main Flask App)**
   - Handles routing for login, registration, course management.
   - Implements secure authentication (password hashing).
   - Manages student course enrollments and course listings.

2. **`models.py` (Database Models & CRUD)**
   - Defines `User`, `Course`, and `Enrollment` tables.
   - Implements functions for adding, retrieving, updating, and deleting records.
   - Includes joins for fetching student enrollments.

3. **`db_init.py` (Database Setup & Triggers)**
   - Creates MySQL tables and necessary constraints.
   - Adds triggers for automatic updates (e.g., auto-remove enrollments on course deletion).
   - Inserts sample data.

4. **HTML Pages (Inside `templates/` Folder):**
   - **`base.html`** → Common template (Navbar + Layout).
   - **`login.html`** → Login form (validates user, redirects to dashboard).
   - **`register.html`** → Registration form (hashes password, saves user).
   - **`dashboard.html`** → Displays enrolled courses (Fetch from DB).
   - **`courses.html`** → Shows available courses with enroll/unenroll options.

5. **CSS Files (Inside `static/css/` Folder)**
   - Each page has a separate CSS file for better styling.
