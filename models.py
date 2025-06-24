import sqlite3
from sqlite3 import Error
import os

# Database file path
DB_FILE = 'student_course_management.db'

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = sqlite3.connect(DB_FILE)
            # Configure SQLite to return rows as dictionaries
            self.connection.row_factory = sqlite3.Row
        except Error as e:
            print(f"Error connecting to SQLite database: {e}")
    
    def execute_query(self, query, params=None):
        try:
            # Check if connection exists, reconnect if necessary
            if not self.connection:
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor
        except Error as e:
            print(f"Error executing query: {e}")
            return None
    
    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        results = []
        if cursor:
            try:
                results = [dict(row) for row in cursor.fetchall()]
            finally:
                cursor.close()
        return results
    
    def fetch_one(self, query, params=None):
        cursor = self.execute_query(query, params)
        result = None
        if cursor:
            try:
                row = cursor.fetchone()
                if row:
                    result = dict(row)
            finally:
                cursor.close()
        return result
    
    def execute_insert(self, query, params=None):
        cursor = self.execute_query(query, params)
        last_id = None
        if cursor:
            try:
                last_id = cursor.lastrowid
            finally:
                cursor.close()
        return last_id
    
    def execute_update(self, query, params=None):
        cursor = self.execute_query(query, params)
        affected_rows = 0
        if cursor:
            try:
                affected_rows = cursor.rowcount
            finally:
                cursor.close()
        return affected_rows > 0
    
    def close(self):
        if self.connection:
            self.connection.close()


class User(Database):
    def create_user(self, name, email, password, role='student'):
        query = """
        INSERT INTO users (name, email, password, role)
        VALUES (?, ?, ?, ?)
        """
        return self.execute_insert(query, (name, email, password, role))
    
    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = ?"
        return self.fetch_one(query, (user_id,))
    
    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE email = ?"
        return self.fetch_one(query, (email,))
    
    def update_user(self, user_id, name, email, role=None):
        if role:
            query = """
            UPDATE users 
            SET name = ?, email = ?, role = ?
            WHERE id = ?
            """
            return self.execute_update(query, (name, email, role, user_id))
        else:
            query = """
            UPDATE users 
            SET name = ?, email = ?
            WHERE id = ?
            """
            return self.execute_update(query, (name, email, user_id))
    
    def update_password(self, user_id, password):
        query = "UPDATE users SET password = ? WHERE id = ?"
        return self.execute_update(query, (password, user_id))
    
    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE id = ?"
        return self.execute_update(query, (user_id,))
    
    def get_all_users(self):
        query = "SELECT id, name, email, role FROM users ORDER BY name"
        return self.fetch_all(query)


class Course(Database):
    def create_course(self, code, title, description, credits):
        query = """
        INSERT INTO courses (code, title, description, credits)
        VALUES (?, ?, ?, ?)
        """
        return self.execute_insert(query, (code, title, description, credits))
    
    def get_course_by_id(self, course_id):
        query = "SELECT * FROM courses WHERE id = ?"
        return self.fetch_one(query, (course_id,))
    
    def get_course_by_code(self, code):
        query = "SELECT * FROM courses WHERE code = ?"
        return self.fetch_one(query, (code,))
    
    def update_course(self, course_id, code, title, description, credits):
        query = """
        UPDATE courses 
        SET code = ?, title = ?, description = ?, credits = ?
        WHERE id = ?
        """
        return self.execute_update(query, (code, title, description, credits, course_id))
    
    def delete_course(self, course_id):
        query = "DELETE FROM courses WHERE id = ?"
        return self.execute_update(query, (course_id,))
    
    def get_all_courses(self):
        query = "SELECT * FROM courses ORDER BY code"
        return self.fetch_all(query)


class Enrollment(Database):
    def create_enrollment(self, user_id, course_id):
        query = """
        INSERT INTO enrollments (user_id, course_id)
        VALUES (?, ?)
        """
        return self.execute_insert(query, (user_id, course_id))
    
    def delete_enrollment(self, user_id, course_id):
        query = """
        DELETE FROM enrollments 
        WHERE user_id = ? AND course_id = ?
        """
        return self.execute_update(query, (user_id, course_id))
    
    def is_enrolled(self, user_id, course_id):
        query = """
        SELECT * FROM enrollments 
        WHERE user_id = ? AND course_id = ?
        """
        result = self.fetch_one(query, (user_id, course_id))
        return result is not None
    
    def get_user_enrollments(self, user_id):
        query = """
        SELECT c.*, e.enrollment_date 
        FROM courses c
        JOIN enrollments e ON c.id = e.course_id
        WHERE e.user_id = ?
        ORDER BY e.enrollment_date DESC
        """
        return self.fetch_all(query, (user_id,))
    
    def get_course_enrollments(self, course_id):
        query = """
        SELECT u.id, u.name, u.email, e.enrollment_date
        FROM users u
        JOIN enrollments e ON u.id = e.user_id
        WHERE e.course_id = ?
        ORDER BY e.enrollment_date
        """
        return self.fetch_all(query, (course_id,))
    
    def get_enrolled_course_ids(self, user_id):
        query = "SELECT course_id FROM enrollments WHERE user_id = ?"
        results = self.fetch_all(query, (user_id,))
        return [result['course_id'] for result in results]