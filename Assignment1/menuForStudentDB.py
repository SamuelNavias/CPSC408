import sqlite3
import re
import random

# Connect to the SQLite database
conn = sqlite3.connect('/Users/SamuelNavias/Documents/CPSC_Courses/CPSC-408/StudentsDB.db')
cursor = conn.cursor()

def menu():
    print("Menu:")
    print("1. Display all students")
    print("2. Add a new student")
    print("3. Update student information")
    print("4. Soft delete a student")
    print("5. Search students")
    print("6. Exit")
    choice = input("Enter your choice: ")
    return choice

def format_phone_number(phone_number):
    # Iterate through the digits and add them until 'x' is encountered
    formatted_number = ''
    for i in phone_number:
        if i != 'x':
            formatted_number += i
        if i == 'x':
            break
    # Now all non numeric characters are removed and the relavent pieces of the phone number are extracted
    formatted_number = re.sub(r'\D', '', formatted_number)
    formatted_number = formatted_number[-10:]

    # Add dashes to the formatted number
    formatted_number = re.sub(r'(\d{3})(\d{3})(\d{4})', r'\1-\2-\3', formatted_number)

    return formatted_number


# Function to validate and reformat zip codes
def format_zip_code(zip_code):
    pattern = r'^\d{5}$'
    if re.match(pattern, zip_code):
        return zip_code
    else:
        digits = re.sub(r'\D', '', zip_code)
        if len(digits) == 5:
            return digits
        else:
            return None

# Function to display all students
def display_all_students():
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    for student in students:
        print(student)

# Function to add a new student
def add_student():
    # Get input from user for new student details
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    address = input("Enter address: ")
    city = input("Enter city: ")
    state = input("Enter state: ")
    zip_code = input("Enter zip code: ")
    mobile_phone = input("Enter mobile phone number: ")
    major = input("Enter major: ")
    gpa = input("Enter GPA: ")

    # Format phone number and zip code
    formatted_zip_code = format_zip_code(zip_code)
    formatted_phone_number = format_phone_number(mobile_phone)

    faculty_advisors = ['Bob Builder', 'Handy Mandy', 'Fixit Felix']
    # Randomly select a faculty advisor from the list
    faculty_advisor = random.choice(faculty_advisors)

    # Insert new student data into the Students table
    cursor.execute('''INSERT INTO Students (FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNumber, Major, GPA, FacultyAdvisor, isDeleted)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)''',
                   (first_name, last_name, address, city, state, formatted_zip_code,
                    formatted_phone_number, major, gpa, faculty_advisor))
    conn.commit()
    print("New student added successfully.")

def update_student():
    student_id = input("Enter the StudentId of the student you want to update: ")
    new_major = input("Enter new major (leave empty to keep unchanged): ")
    new_advisor = input("Enter new advisor (leave empty to keep unchanged): ")
    new_phone_number = input("Enter new phone number (leave empty to keep unchanged): ")

    # Check if any changes are made
    if not any([new_major, new_advisor, new_phone_number]):
        print("No changes made.")
        return

    # Update student information in the Students table
    update_query = "UPDATE Students SET "
    update_values = []
    if new_major:
        update_query += "Major=?, "
        update_values.append(new_major)
    if new_advisor:
        update_query += "FacultyAdvisor=?, "
        update_values.append(new_advisor)
    if new_phone_number:
        formatted_phone_number = format_phone_number(new_phone_number)
        update_query += "MobilePhoneNumber=? "
        update_values.append(formatted_phone_number)

    # Remove the trailing comma and add WHERE clause
    if update_query.endswith(", "):
        update_query = update_query[:-2]  # Remove the trailing comma and space
        update_query += "WHERE StudentId=? AND isDeleted=0"
    else:
        update_query += "WHERE StudentId=? AND isDeleted=0"

    update_values.append(student_id)

    cursor.execute(update_query, tuple(update_values))
    conn.commit()
    print("Student information updated successfully.")


def soft_delete_student():
    student_id = input("Enter the StudentId of the student you want to soft delete: ")

    # Soft delete student by setting isDeleted attribute to 1
    cursor.execute("UPDATE Students SET isDeleted=1 WHERE StudentId=? AND isDeleted=0", (student_id,))
    conn.commit()
    print("Student soft deleted successfully.")

# Function to search students by major, GPA, city, state, or advisor
def search_students():
    print("Search students by major, GPA, city, state, or advisor")
    search_key = input("Enter search keyword: ")

    # Search students by major, GPA, city, state, or advisor
    cursor.execute('''SELECT * FROM Students WHERE 
                      (Major LIKE ? OR GPA LIKE ? OR City LIKE ? OR State LIKE ? OR FacultyAdvisor LIKE ?) 
                      AND isDeleted=0''', ('%' + search_key + '%', '%' + search_key + '%',
                                            '%' + search_key + '%', '%' + search_key + '%', '%' + search_key + '%'))
    students = cursor.fetchall()

    if students:
        print("Search results:")
        for student in students:
            print(student)
    else:
        print("No matching students found.")


# Main program loop
while True:
    choice = menu()

    if choice == "1":
        display_all_students()
    elif choice == "2":
        add_student()
    elif choice == "3":
        update_student()
    elif choice == "4":
        soft_delete_student()
    elif choice == "5":
        search_students()
    elif choice == "6":
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please try again.")
