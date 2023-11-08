import csv
import sqlite3
import random
import re

# Function to validate and reformat phone numbers
def format_phone_number(phone_number):
    # Extract digits from the phone number

    # Iterate through the digits and add them until 'x' is encountered or 10 digits are added
    formatted_number = ''
    for i in phone_number:
        if i != 'x':
            formatted_number += i
        if i == 'x':
            break

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


def import_data_from_csv(csv_file_path, db_file_path):
    # List of possible faculty advisors
    faculty_advisors = ['Bob Builder', 'Handy Mandy', 'Fixit Felix']

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Open the CSV file and insert data into the Students table
    with open(csv_file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header row if it exists in the CSV file

        # Initialize StudentId counter
        student_id = 1

        for row in csvreader:
            # Extract data from CSV row
            first_name, last_name, address, city, state, zip_code, mobile_phone, major, gpa = row

            # Format phone number and zip code
            formatted_zip_code = format_zip_code(zip_code)

            # Randomly select a faculty advisor from the list
            faculty_advisor = random.choice(faculty_advisors)

            # Format phone number
            formatted_phone_number = format_phone_number(mobile_phone)

            # Insert data into the Students table with incremented StudentId, formatted phone number, zip code, random faculty advisor, and isDeleted set to 0
            cursor.execute('''INSERT INTO Students (StudentId, FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNumber, Major, GPA, FacultyAdvisor, isDeleted)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)''',
                           (student_id, first_name, last_name, address, city, state, formatted_zip_code,
                            formatted_phone_number, major, gpa, faculty_advisor))

            # Increment StudentId for the next record
            student_id += 1

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("Data has been successfully imported from the CSV file to the Students table with formatted MobilePhoneNumbers, ZipCodes, randomly assigned FacultyAdvisors, and isDeleted set to 0.")

csv_file_path = '/Users/SamuelNavias/Documents/CPSC_Courses/CPSC-408/students.csv'
db_file_path = '/Users/SamuelNavias/Documents/CPSC_Courses/CPSC-408/StudentsDB.db'
import_data_from_csv(csv_file_path, db_file_path)
