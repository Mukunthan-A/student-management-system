from typing import List, Optional
import psycopg2
from database import connect
from models.student import Student

def add_student(student:Student) -> bool:
    sql = """
        INSERT INTO students (id, name, age, department, email, cgpa)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    
    conn = connect()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, student.to_tuple())
            conn.commit()
            return True
    except psycopg2.DatabaseError as e:
        print(f"Error adding student: {e}")
        conn.rollback()
        return False
    

def get_all_students()-> List[Student]:
    sql = "SELECT id, name, age, department, email, cgpa FROM students;"
    conn = connect()
    students = []
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                students.append(Student(*row))
    except psycopg2.DatabaseError as e:
        print(f"Error fetching students: {e}")
        
    return students



def find_student(student_id: int) -> Optional[Student]:
    sql = "SELECT id, name, age, department, email, cgpa FROM students WHERE id = %s;"
    conn = connect()
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (student_id,))
            row = cursor.fetchone()
            if row:
                return Student(*row)
    except psycopg2.DatabaseError as e:
        print(f"Error finding student: {e}")
        
    return None



def update_student(student_id: int, name: str, age: int, department: str, email: str, cgpa: float) -> bool:
    sql = """
        UPDATE students 
        SET name = %s, age = %s, department = %s, email = %s, cgpa = %s
        WHERE id = %s;
    """
    conn = connect()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, age, department, email, cgpa, student_id))
            conn.commit()
            return cursor.rowcount > 0
    except psycopg2.DatabaseError as e:
        print(f"Error updating student: {e}")
        conn.rollback()
        return False
    


def delete_student(student_id: int) -> Optional[Student]:
    sql = "DELETE FROM students WHERE id = %s;"
    conn = connect()
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (student_id,))
            return cursor.rowcount > 0
    except psycopg2.DatabaseError as e:
        print(f"Error finding student: {e}")
        conn.rollback()
        return False
    



def top_students(limit: int = 5) -> List[Student]:
    sql = """
        SELECT id, name, age, department, email, cgpa 
        FROM students 
        ORDER BY cgpa DESC 
        LIMIT %s;
    """
    conn = connect()
    students = []
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (limit,))
            rows = cursor.fetchall()
            for row in rows:
                students.append(Student(*row))
    except psycopg2.DatabaseError as e:
        print(f"Error fetching top students: {e}")
        
    return students



def count_students() -> int :
   sql = "SELECT COUNT(*) FROM students;"
   conn = connect()              
    
   try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                return result[0]
   except psycopg2.DatabaseError as e:
        print(f"Error counting students: {e}")
        
   return 0
