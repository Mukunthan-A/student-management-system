import sys

# Updated absolute imports to reference the modules under the packages
from models.student import Student
from services import student_service
import database


def display_menu() -> None:
    """Displays the main menu interface."""
    print("\n" + "=" * 5 + " Student Management System " + "=" * 5)
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. View Top Performers")
    print("7. View Total Student Count")
    print("8. Exit")
    print("=" * 37)


def get_integer_input(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def get_float_input(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter a valid decimal number.")


def handle_add_student() -> None:
    print("\n--- Add New Student ---")
    student_id = get_integer_input("Enter Student ID: ")
    
    # Check if student ID already exists before proceeding
    if student_service.find_student(student_id) is not None:
        print(f"Error: A student with ID {student_id} already exists.")
        return

    name = input("Enter Name: ").strip()
    age = get_integer_input("Enter Age: ")
    department = input("Enter Department: ").strip()
    email = input("Enter Email: ").strip()
    cgpa = get_float_input("Enter CGPA: ")

    new_student = Student(student_id, name, age, department, email, cgpa)
    
    if student_service.add_student(new_student):
        print("\nStudent added successfully!")
    else:
        print("\nFailed to add student. Please verify your input and try again.")


def handle_view_students() -> None:
    print("\n--- All Students ---")
    students = student_service.get_all_students()
    
    if not students:
        print("No student records found in the database.")
        return

    for student in students:
        print(student)


def handle_search_student() -> None:
    print("\n--- Search Student ---")
    student_id = get_integer_input("Enter Student ID to Search: ")
    student = student_service.find_student(student_id)

    if student:
        print("\nStudent Found:")
        print(student)
    else:
        print(f"No student found with ID {student_id}.")


def handle_update_student() -> None:
    print("\n--- Update Student Information ---")
    student_id = get_integer_input("Enter Student ID to Update: ")
    student = student_service.find_student(student_id)

    if not student:
        print(f"No student found with ID {student_id}.")
        return

    print(f"\nCurrent Record: {student}")
    print("Leave field blank and press Enter to keep current value.")

    name = input(f"Enter Name [{student.name}]: ").strip() or student.name    
    age_input = input(f"Enter Age [{student.age}]: ").strip()
    age = int(age_input) if age_input else student.age
    department = input(f"Enter Department [{student.department}]: ").strip() or student.department
    email = input(f"Enter Email [{student.email}]: ").strip() or student.email
    cgpa_input = input(f"Enter CGPA [{student.cgpa}]: ").strip()
    cgpa = float(cgpa_input) if cgpa_input else student.cgpa

    if student_service.update_student(student_id, name, age, department, email, cgpa):
        print("\nStudent record updated successfully!")
    else:
        print("\nFailed to update student record.")


def handle_delete_student() -> None:
    print("\n--- Delete Student Record ---")
    student_id = get_integer_input("Enter Student ID to Delete: ")
    
    # Confirm deletion
    student = student_service.find_student(student_id)
    if not student:
        print(f"No student found with ID {student_id}.")
        return

    confirm = input(f"Are you sure you want to delete {student.name} (ID: {student_id})? (y/n): ").strip().lower()
    if confirm == 'y':
        if student_service.delete_student(student_id):
            print("\nStudent record deleted successfully!")
        else:
            print("\nFailed to delete student record.")
    else:
        print("\nDeletion cancelled.")


def handle_top_students() -> None:
    print("\n--- Top Performers ---")
    limit = get_integer_input("How many top students would you like to view? (Default is 5): ")
    students = student_service.top_students(limit=limit)
    
    if not students:
        print("No student records found.")
        return

    for idx, student in enumerate(students, start=1):
        print(f"{idx}. {student.name} - CGPA: {student.cgpa} ({student.department})")


def handle_count_students() -> None:
    count = student_service.count_students()
    print(f"\nTotal registered students in database: {count}")


def main() -> None:
    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            handle_add_student()
        elif choice == "2":
            handle_view_students()
        elif choice == "3":
            handle_search_student()
        elif choice == "4":
            handle_update_student()
        elif choice == "5":
            handle_delete_student()
        elif choice == "6":
            handle_top_students()
        elif choice == "7":
            handle_count_students()
        elif choice == "8":
            print("\nExiting System. Closing database connections. Goodbye!")
            database.close()
            sys.exit(0)
        else:
            print("Invalid choice. Please choose a number between 1 and 8.")


if __name__ == "__main__":
    main()