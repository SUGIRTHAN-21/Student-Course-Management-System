import sqlite3
import hashlib
import os

# Database file path
DB_FILE = 'student_course_management.db'

def create_connection():
    connection = None
    try:
        connection = sqlite3.connect(DB_FILE)
        print("SQLite connection successful")
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite: {e}")
    return connection

def create_tables(connection):
    cursor = connection.cursor()
    
    # Create users table
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('student', 'admin')) DEFAULT 'student',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    # Create courses table
    create_courses_table = """
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        description TEXT,
        credits INTEGER DEFAULT 3,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    # Create enrollments table
    create_enrollments_table = """
    CREATE TABLE IF NOT EXISTS enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
        UNIQUE (user_id, course_id)
    )
    """
    
    # Execute create table queries
    try:
        cursor.execute(create_users_table)
        print("Users table created successfully")
        
        cursor.execute(create_courses_table)
        print("Courses table created successfully")
        
        cursor.execute(create_enrollments_table)
        print("Enrollments table created successfully")
        
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()

def add_sample_data(connection):
    cursor = connection.cursor()
    
    # Add admin user
    admin_password = hashlib.sha256("admin123".encode()).hexdigest()
    add_admin = """
    INSERT OR IGNORE INTO users (name, email, password, role)
    VALUES (?, ?, ?, ?)
    """
    admin_data = ("Admin User", "admin@example.com", admin_password, "admin")
    
    # Add student user
    student_password = hashlib.sha256("student123".encode()).hexdigest()
    add_student = """
    INSERT OR IGNORE INTO users (name, email, password, role)
    VALUES (?, ?, ?, ?)
    """
    student_data = ("Student User", "student@example.com", student_password, "student")
    
    # Add sample courses
    add_course = """
    INSERT OR IGNORE INTO courses (code, title, description, credits)
    VALUES (?, ?, ?, ?)
    """
    courses_data = [
        ("CS101", "Introduction to Computer Science", "Basic concepts of programming and computer science", 1),
        ("CS201", "Data Structures", "Study of data structures and algorithms", 1),
        ("CS301", "Database Systems", "Introduction to database design and SQL", 3),
        ("MATH101", "Calculus I", "Differential and integral calculus", 4),
        ("PHYS101", "Physics I", "Introduction to mechanics and thermodynamics", 4),
        ("CS102", "C Programming", "Fundamentals of C programming language", 1),
        ("CS103", "C++ Programming", "Object-oriented programming with C++", 2),
        ("CS104", "Java Programming", "Introduction to Java and OOP concepts", 4),
        ("CS105", "Python Programming", "Python programming for beginners and professionals", 1),
        ("CS106", "Web Designing", "HTML, CSS, JavaScript, and UI design principles", 3),
        ("STAT101", "Statistics", "Basic statistics and probability", 3),
        ("ADV101", "Advertising", "Principles of marketing and advertising", 2),
        ("DA101", "Data Analytics", "Introduction to data analysis techniques", 3),
        ("DS101", "Data Science", "Machine learning, AI, and data science concepts", 1),
        ("ARM101", "ARM Architecture", "Understanding ARM-based systems and programming", 3)
    
    ]
    
    try:
        # Check if admin user exists
        cursor.execute("SELECT id FROM users WHERE email = 'admin@example.com'")
        if not cursor.fetchone():
            cursor.execute(add_admin, admin_data)
            print("Admin user added")
        
        # Check if student user exists
        cursor.execute("SELECT id FROM users WHERE email = 'student@example.com'")
        if not cursor.fetchone():
            cursor.execute(add_student, student_data)
            print("Student user added")
        
        # Add courses if they don't exist
        for course in courses_data:
            cursor.execute("SELECT id FROM courses WHERE code = ?", (course[0],))
            if not cursor.fetchone():
                cursor.execute(add_course, course)
                connection.commit()
                print(f"Course {course[0]} added")
        
        connection.commit()
        print("Sample data added successfully")
        
    except sqlite3.Error as e:
        print(f"Error adding sample data: {e}")
    finally:
        cursor.close()

def main():
    # Check if database file exists
    db_exists = os.path.exists(DB_FILE)
    
    # Create connection
    connection = create_connection()
    
    if connection:
        try:
            # Create tables
            create_tables(connection)
            
            # Add sample data
            add_sample_data(connection)
            
        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            if connection:
                connection.close()
                print("SQLite connection closed")

if __name__ == "__main__":
    main()

