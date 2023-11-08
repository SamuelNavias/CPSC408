# Assignment 1

* This assignment has two main pieces:
* Moving data from a csv file into a SQLite database.
  - Moving the data from the csv was a very standard process so I'll only note some of the pieces of my program that are more specific to the assignment.
  - I chose to reformat the phone numbers by using a function that got rid of extension codes and country codes and also ensured that dashes were used.  So all of the numbers were in the format ###-###-####
  - For the faculty advisors I chose to make a list of three people that were randomly assigned to each student.
  - Finally, I also decided to make sure each zip code was strictly 5 integers #####.
* Making a console application that allows a user to connect to and interact with the data in the SQLite database.
  - My Python console application uses a loop that looks for user input of integers to determine how the user wants to interact with the data.
  - The options are continuously printed to the console until the user chooses to exit.
  - 1: Displays all of the students
  - 2: Adds a new student to the database
  - 3: Updates one student's information in the database
    - When prompted to change the major, advisor, or phone number the user can choose to leave any or all of the prompts empty to not update any attribute or update any number of attributes of the users choosing.
  - 4: Soft deletes a student by setting their isDeleted value to 1
  - 5: Search for a student by their major, GPA, city, state, or advisor
    - In my implementation, a user enters one keyword like a GPA and students with that GPA are printed to the console.
    - Alternatively, a state could have been inputted by the user and students from that state are printed to the console.
  - 6: Exits the program

## Identifying Information

* Name: Samuel Navias
* Student ID: 2370708
* Email: navias@chapman.edu
* Course: CPSC-408-01
* Assignment: Sqlite

## References

* GeeksforGeeks

## Known Errors

* There are no known errors at the time of submission 

## Execution Instructions
* python retrieveData.py
* (To clarify this is the program that extracts the data from the csv file)
* python menuForStudentDB.py
* (This is the Python app that allows a user to interact with the database)
