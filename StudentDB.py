import sqlite3
import csv


# Function to import students.csv into StudentDB database
def import_csv():
    conn = sqlite3.connect('./StudentDB.db')
    my_cursor = conn.cursor()

    with open('students.csv', 'r') as myFile:
        reader = csv.DictReader(myFile)
        for row in reader:
            my_cursor.execute("INSERT INTO Student(FirstName, LastName, GPA, "
                              "Major, FacultyAdvisor, Address, City, State, ZipCode, "
                              "MobilePhoneNumber, isDeleted)"
                              "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                              (row["FirstName"], row["LastName"], row["GPA"],
                               row["Major"], "Unassigned", row["Address"], row["City"],
                               row["State"], row["ZipCode"], row["MobilePhoneNumber"], 0,))

    conn.commit()
    my_cursor.close()


# function to display all students in StudentDB database
def display_all_students():
    conn = sqlite3.connect('./StudentDB.db')
    my_cursor = conn.cursor()
    my_cursor.execute("SELECT * FROM Student WHERE isDeleted = 0")

    rows = my_cursor.fetchall()
    for row in rows:
        print(row)
    my_cursor.close()
    return rows


# function to add new student to StudentDB database
def add_new_student(attribute_dict):
    conn = sqlite3.connect('./StudentDB.db')
    my_cursor = conn.cursor()
    my_cursor.execute("INSERT INTO Student(FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State,"
                      " ZipCode, MobilePhoneNumber, isDeleted) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                      (attribute_dict["FirstName"], attribute_dict["LastName"], attribute_dict["GPA"],
                       attribute_dict["Major"], attribute_dict["FacultyAdvisor"], attribute_dict["Address"],
                       attribute_dict["City"], attribute_dict["State"], attribute_dict["ZipCode"],
                       attribute_dict["MobilePhoneNumber"], 0,))

    conn.commit()
    my_cursor.close()


# function to update student info for a student in StudentDB database
def update_student(psid, p_choice, updated_value):
    conn = sqlite3.connect('./StudentDB.db')
    my_cursor = conn.cursor()
    if p_choice == 1:
        my_cursor.execute("UPDATE Student SET Major = ? WHERE StudentId = ?;",
                          (updated_value, psid))
    elif p_choice == 2:
        my_cursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?;",
                          (updated_value, psid))
    elif p_choice == 3:
        my_cursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentId = ?;",
                          (updated_value, psid))
    else:
        print("Oops! Something went wrong")

    conn.commit()
    my_cursor.close()


# function to soft-delete student in StudentDB database
def delete_student(sid):
    conn = sqlite3.connect('./StudentDB.db')
    my_cursor = conn.cursor()
    my_cursor.execute("UPDATE Student SET IsDeleted = ? WHERE StudentId = ?",
                      (1, sid))

    conn.commit()
    my_cursor.close()


# function to find students with a specific major, gpa, city, state, or Faculty Advisor
def find_student(choices, values):
    if choices == 1:
        query = "Major = ?"
    if choices == 2:
        query = "GPA = ?"
    if choices == 3:
        query = "City = ?"
    if choices == 4:
        query = "State = ?"
    if choices == 5:
        query = "FacultyAdvisor = ?"

    conn = sqlite3.connect('./StudentDB.db')
    my_cursor = conn.cursor()
    my_cursor.execute("SELECT * FROM Student WHERE " + query + "AND isDeleted = ?;", (values, 0,))
    result = my_cursor.fetchall()

    conn.commit()
    my_cursor.close()
    for row in result:
        print(row)
    return result


# used to make sure students exist in database
def find_id(psid):
    conn = sqlite3.connect('./StudentDB.db')
    my_cursor = conn.cursor()
    my_cursor.execute("SELECT * FROM Student WHERE StudentId = ? and isDeleted = ?", (psid, 0,))

    rows = my_cursor.fetchall()
    my_cursor.close()
    return rows


advisors = ["Michael Smith", "Matt Shugarte", "Diego Murillo", "Ewan Shen", "Kevin Le"]
states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
          'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
          'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
          'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
          'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
          'South Carolina ', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
          'West Virginia', 'Wisconsin', 'Wyoming']

f_choice = 0 # Operation to be performed by user
while f_choice != 7:
    print("Please select one operation you'd like to perform (Type a number 1-7):")
    print("1) Import students.csv\n2) Display all students in the database\n3) Add new student to the database\n"
          "4) Update student info\n5) Delete a student\n6) Find students based on student info\n7) Exit")
    user_in = input()
    if user_in.strip().isdigit():
        if int(user_in.strip()) > 0 and int(user_in.strip()) < 8:
            f_choice = int(user_in.strip())
            # import students.csv
            if f_choice == 1:
                import_csv()
            # display all students
            elif f_choice == 2:
                display_all_students()
            # add a new student
            elif f_choice == 3:
                attributes = {"FirstName": input("Enter the new student's First Name: ")[0:30],
                              "LastName": input("Enter the new student's Last Name: ")[0:30]}
                need_gpa = True
                gpa = "0.0"
                while need_gpa:
                    try:
                        user_in2 = input("Enter the new student's GPA: ")
                        gpa = float(user_in2)
                        need_gpa = False
                    except:
                        print("Enter in a decimal number. Do not use non-numeric characters")

                attributes["GPA"] = float(gpa)
                attributes["Major"] = input("Enter the new student's Major: ")[0:30]

                while True:
                    print("Select the new student's Faculty Advisor (Type a number 1-5): ")
                    print("1) Michael Smith\n2) Matt Shugarte\n3) Diego Murillo\n4) Ewan Shen\n5) Kevin Le")
                    advisor = input()
                    if advisor.isdigit():
                        if int(advisor) > 0 and int(advisor) < 6:
                            attributes["FacultyAdvisor"] = advisors[int(advisor) - 1]
                            break
                        else:
                            print("Enter a number between 1 and 5 to select a valid advisor.")
                    else:
                        print("Enter a number between 1 and 5 to select a valid advisor.")

                attributes["Address"] = input("Enter the new student's address: ")[0:60]
                attributes["City"] = input("Enter the new student's City: ")[0:40]

                while True:
                    state = input("Enter the new student's State: ")
                    if state in states:
                        attributes["State"] = state
                        break
                    else:
                        print("Enter a valid state")
                while True:
                    zip_c = input("Enter the new student's Zipcode: ")
                    if len(zip_c) == 5 and zip_c.isdigit():
                        attributes["ZipCode"] = zip_c
                        break
                    else:
                        print("Please enter a 5 digit zipcode")
                while True:
                    cp_number = input("Enter the new student's Mobile Phone Number as a sequence of integers only: ")
                    if cp_number.isdigit():
                        attributes["MobilePhoneNumber"] = cp_number
                        break
                    else:
                        print("Enter only integers for the phone number")

                add_new_student(attributes)
            # update student info
            elif f_choice == 4:
                while True:
                    user_in2 = input("Enter the id of the student who's info you wish to update: ")
                    if user_in2.isdigit():
                        sid = int(user_in2)
                        find = find_id(sid)
                        print(find)
                        if len(find) == 1:
                            while True:
                                print("Select what attribute you would like to change (1-3):")
                                print("1) Major\n2) Faculty Advisor\n3) Mobile Phone Number")
                                user_choice = input()
                                if user_choice.isdigit():
                                    i_choice = int(user_choice)
                                    if i_choice == 1:
                                        value = input("Enter the new student's Major: ")[0:30]
                                        break
                                    elif i_choice == 2:
                                        while True:
                                            print("Select the new student's Faculty Advisor (Type a number 1-5): ")
                                            print(
                                                "1) Michael Smith\n2) Matt Shugarte\n3) Diego Murillo\n4) Ewan Shen\n5) Kevin Le")
                                            advisor = input()
                                            if advisor.isdigit():
                                                if int(advisor) > 0 and int(advisor) < 6:
                                                    value = advisors[int(advisor) - 1]
                                                    break
                                                else:
                                                    print("Enter a number between 1 and 5 to select a valid advisor.")
                                            else:
                                                print("Enter a number between 1 and 5 to select a valid advisor.")
                                        break
                                    elif i_choice == 3:
                                        while True:
                                            cp_number = input("Enter the new student's Mobile Phone Number as a "
                                                              "sequence of integers only: ")
                                            if cp_number.isdigit():
                                                value = cp_number
                                                break
                                            else:
                                                print("Enter only integers for the phone number.")
                                        break
                                    else:
                                        print("Enter an integer between 1 and 3 to select an option.")
                                else:
                                    print("Enter an integer for your selection.")
                            break
                        else:
                            print("Student not found. Please enter a valid student ID.")
                    else:
                        print("Student ID should be an integer.")
                update_student(sid, i_choice, value)
            # delete student
            elif f_choice == 5:
                while True:
                    user_in2 = input("Enter the id of the student you wish to delete: ")
                    if user_in2.isdigit():
                        sid = int(user_in2)
                        find = find_id(sid)
                        if len(find) == 1:
                            delete_student(sid)
                            break
                        else:
                            print("Student not found. Please enter a valid student ID.")
                    else:
                        print("Student ID should be an integer.")
            # query by major, gpa, city, state, or faculty advisor
            elif f_choice == 6:
                while True:
                    print("Select what you would like to query by: ")
                    print("1) Major\n2) GPA\n3) City\n4) State\n5) Faculty Advisor")
                    choice = input()
                    if choice.isdigit():
                        i_choice = int(choice)
                        if i_choice == 1:
                            value = input("Enter the Major you would like to search by: ")[0:30]
                            break
                        elif i_choice == 2:
                            need_gpa = True
                            gpa = "0.0"
                            while need_gpa:
                                try:
                                    user_in2 = input("Enter the new student's GPA: ")
                                    gpa = float(user_in2)
                                    need_gpa = False
                                except:
                                    print("Enter in a decimal number. Do not use non-numeric characters")
                                # gpa = ""
                                # need_gpa = False
                                # for char in user_in2:
                                #     if char.isnumeric() or char == '.':
                                #         gpa += char
                                #     else:
                                #         print("Enter in a decimal number. Do not use non-numeric characters")
                                #         need_gpa = True
                                #         break
                            value = float(gpa)
                            break
                        elif i_choice == 3:
                            value = input("Enter the students' City: ")[0:40]
                            break
                        elif i_choice == 4:
                            while True:
                                state = input("Enter the students' State: ")
                                if state in states:
                                    value = state
                                    break
                                else:
                                    print("Enter a valid state.")
                            break
                        elif i_choice == 5:
                            while True:
                                print("Select the Faculty Advisor to search for (Type a number 1-5): ")
                                print("1) Michael Smith\n2) Matt Shugarte\n3) Diego Murillo\n4) Ewan Shen\n5) Kevin Le")
                                advisor = input()
                                if advisor.isdigit():
                                    if int(advisor) > 0 and int(advisor) < 6:
                                        value = advisors[int(advisor) - 1]
                                        break
                                    else:
                                        print("Enter a number between 1 and 5 to select a valid advisor.")
                                else:
                                    print("Enter a number between 1 and 5 to select a valid advisor.")
                            break
                        else:
                            print("Enter a number between 1 and 7 to select a valid option")
                    else:
                        print("Enter a number between 1 and 7 to select a valid option")
                find_student(i_choice, value)
            # exit
            elif f_choice == 7:
                print("Goodbye!")
                break
        else:
            print("Please enter a number within the range of 1 to 7 to select your operation.\n")
            continue
    else:
        print("Please enter a numerical value. Do not use words or letters.\n")
