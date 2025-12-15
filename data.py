"""
to develop a Student Grading System that manages student records and assessment results
to calculate overall grades, assign letter grades, and display class performance summaries
to prevent abrupt crashing of program, we use a lot of try-except block, making our porgram user-friendly
"""
import os       #for file operations 
import sys      #to exit gracefully
import time    #for time delay 

STUDENTS_FILE = 'students.txt'
COURSES_FILE = 'courses.txt'
GRADES_FILE = 'grades.txt'

def read_file(filename):
    #Important fundamental function for all declare functions later, to only store primitive data so no error will be presented in case of empty line or spaces in user input
    with open(filename, 'r', encoding="utf-8") as f:        #prevemt error when file not found and contains special name in student name
        return [line.strip().split(',') for line in f if line.strip()]

def add_student():
    #get student personal information such as student ID specifically only in 8 digits format, name, email 
    try:
        student_id = int(input('Enter Student ID (251xxxxx) : ').strip())
        if len(str(student_id)) != 8:          #must change to str because len() only works on string
            raise ValueError("Sunway student ID must be 8 digits")
        students = read_file(STUDENTS_FILE)
        for s in students:                  #prevent duplicate student ID in file
            if s[0] == str(student_id):
                raise ValueError("Student ID already exists")   
    #get student name 
        name = input('Enter Student Name (Name per NRIC) : ').strip().upper()
        if not name:
            raise ValueError ("Name cannot be empty")
        elif any(char.isdigit() for char in name):            #check name has numbers or not
            raise ValueError("Name cannot contain numbers")
        elif ',' in name or '.' in name:
            raise ValueError("Name cannot contain symbol (use space instead)")
    #get student email 
        email = input('Enter Student Email (xxxxxxxx@imail.sunway.edu.my): ').strip().lower()
        if not email.endswith("@imail.sunway.edu.my"):          #ensure email ends with @imail.sunway.edu.my
            raise ValueError("Email must end with @imail.sunway.edu.my")
    #save to file and runs when all input are correct
        with open(STUDENTS_FILE, 'a', encoding = "utf-8") as f:
            f.write(f'{student_id},{name},{email}\n')
        print('Student added successfully!')

    #robust error-handling
    except ValueError as problem:          
        print(f"Invalid input: {problem}")
        return
    except FileNotFoundError: 
        print("Error: The database file is missing.")
        return
    except Exception as problem:         #exception = type of error (file missing, permission denied and more)   problem= to show why crash (shows file name) #no need raise anything about it, python will product it
        print(f"Unexpected error occured: {problem}")
        return

def add_course():
    #to get course id, course name
    try:
        course_id = input('Enter Course ID (CSC1024) : ').strip().upper()
        if not course_id:
            raise ValueError("Empty input") # check if empty, if empty force the crash(type again)
        elif ',' in course_id: 
            raise ValueError("Course ID cannot contain commas")
        courses = read_file(COURSES_FILE)
        for c in courses:
            if c[0] == course_id:
                raise ValueError(f"Course ID '{course_id}' already exists")  #prevent duplicate course ID in file
        course_name = input('Enter Course Name (PROGRAMMING PRINCIPLES) : ').strip().upper()
        if not course_name:
            raise ValueError("Course Name cannot be empty ") # check if empty, if empty force the crash(type again)
        elif ',' in course_name or '.' in course_name:
            raise ValueError("Course Name cannot contain commas (use space instead)")
        #save to file if all input are valid
        with open(COURSES_FILE, 'a', encoding = "utf-8") as f:
            f.write(f'{course_id},{course_name}\n')
        print('Course added successfully!')

    #robust error-handling
    except ValueError as problem:  #occur when empty ID or empty name
        print(f'Invalid input {problem}, please try again:')
        return
    except FileNotFoundError: 
        print("Error: The database file is missing.")
        return
    except Exception as problem:
        print(f"Unexpected error occured: {problem}")
        return

def marks_to_grade(marks):
    #Assign letter grades based on the Sunway University grading scale
    if marks >= 90: 
        return 'A+'
    elif marks >= 80: 
        return 'A'
    elif marks >= 75: 
        return 'A-'
    elif marks >= 70: 
        return 'B+'
    elif marks >= 65: 
        return 'B'
    elif marks >= 60: 
        return 'B-'
    elif marks >= 55: 
        return 'C+'
    elif marks >= 50: 
        return 'C'
    # Fail
    elif marks >= 45: 
        return 'C-'
    elif marks >= 40: 
        return 'D+'
    elif marks >= 35: 
        return 'D'
    else:
    # If none of the above (0-34)
        return 'F'

def record_marks():
    #allow users to enter marks for a student in a specific course, automatically calculating and assigning a letter grade
    try:
        student_id = int(input('Enter Student ID (251xxxxx) : ').strip())
        students = read_file(STUDENTS_FILE)
        student_ids = [s[0] for s in students] #list of all student IDs in file
        if str(student_id) not in student_ids:
            raise ValueError("Student ID not found in records") #check .txt file have this student or not
     #get course ID
        course_id = input('Enter Course ID (CSC1024) : ').strip().upper()
        courses = read_file(COURSES_FILE)
        course_ids = [c[0] for c in courses] #list of all course IDs in file
        if course_id not in course_ids:
            raise ValueError("Course ID not found in records")  #raise error if course id not found in file
    #get marks
        marks = float(input('Enter marks (0-100): '))
        if marks < 0 or marks > 100:            # marks mut in -1<marks<101
            raise ValueError("Error: Marks must be between 0 and 100.")
    #save data
    #only run when all inputs are valid
        grade = marks_to_grade(marks)
        with open(GRADES_FILE, 'a', encoding = "utf-8") as f:
            f.write(f'{student_id},{course_id},{marks},{grade}\n')    #format to save in files
        print(f'Success! Marks recorded. Grade = {grade}')

    #robust error-handling
    except ValueError as problem:   # occur when user typo that cause the current id not in file
        print(f'Invalid input: {problem}')
        return  
    except FileNotFoundError:  
        print("Error: The database file is missing.")
        return
    except Exception as problem:         #'problem' will shows why error happened
        print(f"Unexpected error occured : {problem}")     #output : Error saving to file: [Errno 13] Permission denied: 'grades.txt'
        return

def display_student():
    #display individual student performance including all enrolled courses and grades
    try:
        student_id = input('Enter Student ID (251xxxxx) : ').strip()
        student_id = str(int(student_id))           #convert to string for len() check
        if len(str(student_id)) == 8:
            #studet's data will be read from file
            students = read_file(STUDENTS_FILE)
            grades = read_file(GRADES_FILE)
            found = False
            for s in students:
                if s[0] == student_id:
                    found = True            #if found student, then display info
                    print(f'\nStudent: {s[1]} ({s[0]})')
                    print('Email:', s[2])
                    print('\nCourses and Grades:')
                    total = 0
                    count = 0
                    for g in grades:
                        #check grades file for matching student id
                        if g[0] == student_id:
                            print(f'Course: {g[1]}, Marks: {g[2]}, Grade: {g[3]}')
                            total += float(g[2])
                            count += 1

                    if count ==0:
                        print('No grades recorded yet.')
                    break   #exit loop after finding student

            #robust error-handling        
            if not found:
                print('Student not found!')
        else:
            raise ValueError("Sunway student ID must be 8 numbers")
    except ValueError as reason:
        print(f'Invalid student id:{reason}')   
    except FileNotFoundError:  
        print("Error: The database file is missing.")
        return
    except Exception as problem:
        print(f'Unexpected error occured:{problem}')

def display_course():
    #display course performance summary by listing all students enrolled in a particular course, along with average, highest, and lowest marks
    try:
        course_id = input('Enter Course (CSC1024) : ').strip().upper()
        if not course_id:
            raise ValueError("Course ID cannot be empty") # check if empty, if empty force the crash(type again)
        #real data from files
        courses = read_file(COURSES_FILE)
        grades = read_file(GRADES_FILE)
        students = read_file(STUDENTS_FILE)
        
        found = False
        for c in courses:
                #look for course id in courses file
            if c[0] == course_id:
                found = True
                print(f'\nCourse: {c[1]} ({c[0]})')
                # Note: line will crash if grades file has text instead of numbers.
                # except block below catch it if that happens.
                course_grades = [g for g in grades if g[1] == course_id]
                if not course_grades:
                    print('No grades recorded yet.')
                    return      # Stop here if no grades
                #Display enrolled students with marks
                print("\nEnrolled Students:")
                marks_list = []         
                for record in course_grades:
                    student_id = record[0]
                    student_name = next((s[1] for s in students if s[0] ==student_id), "Unknown")
                    try: 
                        marks = float(record[2])

                    except ValueError:
                        print(f"Invalid marks for student {record[2]}, skipping.")
                        continue
                    grade = record[3]
                    marks_list.append(marks)
                    print(f"{student_name} ({student_id}): Marks = {marks}, Grade = {grade}")

                #Summary output
                if marks_list: # Check if list is not empty to avoid division by zero
                    total = sum (marks_list)
                    average = total / len (marks_list)

                    print("\nCourse Summary:")
                    print ('Average:', average)
                    print('Highest: ', max(marks_list))
                    print('Lowest : ', min(marks_list))
                    break   #exit loop after finding course

        #robust error-handling
        if not found:
            print('Course not found!')
    except ValueError as problem:           #occur when user error input like empty course id taht can be predicted
        # Catches empty input or corrupted numbers in file
        print(f"Invalid operation: {problem}")
        return
    except FileNotFoundError:  
        print("Error: The database file is missing.")
        return
    except Exception as problem:         #occur when file missing or other crash that cant be predicted
        # Catches file missing errors or other crashes
        print(f"Unexpected error occured: {problem}")
    #need two except block to separate predictable and unpredictable error
        return

def export_report():
    #export course summary or individual performance report to text file for record keeping
    try:
        student_id = input('Enter Student ID to export (251xxxxx) : ').strip()
        student_id = str(int(student_id))           #convert to string for len() check
        if len(student_id) != 8:
            raise ValueError("Sunway Student ID must be 8 digits")
        students = read_file(STUDENTS_FILE)         #find student first then read grades file
        for s in students:
            if s[0] == student_id:
                grades = read_file(GRADES_FILE)
                filename = f'report_{student_id}.txt'
                with open(filename, 'w', encoding="utf-8") as f:
                    f.write(f'Student: {s[1]} ({s[0]})\nEmail: {s[2]}\n\n')
                    for g in grades:
                        if g[0] == student_id:
                            f.write(f'Course: {g[1]}, Marks: {g[2]}, Grade: {g[3]}\n')
                print(f'Report saved as {filename}')
                return

        #robust error-handling    
        raise ValueError('Student not found!')      
    except ValueError as problem:
        print(f"Invalid input: {problem}")
        return
    except FileNotFoundError:  
        print("Error: The database file is missing.")
        return
    except Exception as problem:
        print(f"Unexpected error occured: {problem}")
        return

#set for delete functions to overwrite files
def save_file(filename, data_list): 
    #takes the data from memory and permanently writes it back to the text file, this function is used in delete functions
    # WARNING: This wipes the old file clean immediately!
    with open(filename, 'w', encoding="utf-8") as f: 
        for line in data_list:
            # It writes the updated list back into the file
            f.write(','.join(map(str, line)) + '\n')

def delete_student():
    #Delete a student and their associated grades based on Student ID
    try:
        student_id = input('Enter Student ID to DELETE (251xxxxx): ').strip()
        # 1. Read existing data
        students = read_file(STUDENTS_FILE)
        grades = read_file(GRADES_FILE)
        # 2. Check if student exists
        student_found = False
        new_students = []
        for s in students:
            if s[0] == student_id:
                student_found = True
                print(f"Deleting Student: {s[1]} ({s[0]})...")  # Show which student is being deleted
            else:
                new_students.append(s) # Keep students that don't match in list because the list will loop one by one, will pass all students except the one to delete
        if not student_found:
            print("Student ID not found.")  # if the student id not found in file
            return
        # 3. Remove associated grades for this student (Clean up)
        new_grades = [g for g in grades if g[0] != student_id]  
        # 4. Save changes
        confirm = input("Are you sure? This cannot be undone (Y/N): ").strip().upper()
        if confirm == 'Y':
            save_file(STUDENTS_FILE, new_students)
            save_file(GRADES_FILE, new_grades)
            print("Student and their marks deleted successfully.")
        
        #robust error-handling
        else:
            print("Deletion cancelled.")
    except FileNotFoundError:  
        print("Error: The database file is missing.")
        return
    except Exception as reason:
        print(f"Unexpected error occuredr: {reason}")
        return

def delete_mark():
    #Delete a specific grade entry for a student in a specific course
    try:
        student_id = input('Enter Student ID (251xxxxx): ').strip()
        course_id = input('Enter Course ID to remove marks (CSC1024): ').strip().upper()
        grades = read_file(GRADES_FILE)
        new_grades = []
        found = False
        for g in grades:
            # Check if BOTH student ID and Course ID match
            if g[0] == student_id and g[1] == course_id:
                found = True
                print(f"Removing mark: {g[2]} (Grade {g[3]}) for {g[1]}")
                # Do NOT append this to new_grades (effectively deleting it)
            else:
                new_grades.append(g)            # Keep all other records
        if found:
            save_file(GRADES_FILE, new_grades)
            print("Mark deleted successfully.")

        #robust error-handling    
        else:
            print("No matching mark record found.") 
    except FileNotFoundError:  
        print("Error: The database file is missing.")
        return 
    except Exception as reason:
        print(f"Unexpected error occured: {reason}")       #general exception to catch all unexpected errors
        return

def edit_course():
    #Edit course details. If ID is changed, update it in grades file too
    try:
        old_id = input('Enter Course ID to EDIT (CSC1024): ').strip().upper()
        courses = read_file(COURSES_FILE)
        course_index = -1
        # Find the course
        for i, c in enumerate(courses):     # enumerate to get index and course data (i=index and c=course data)
            if c[0] == old_id:
                course_index = i
                print(f"Editing Course: {c[1]} ({c[0]})")
                break
        if course_index == -1:
            print("Course ID not found.")
            return
        # Get new details
        print("Press Enter to keep current value.")
        new_id = input(f"Enter New Course ID (Current: {courses[course_index][0]}): ").strip().upper()
        new_name = input(f"Enter New Course Name (Current: {courses[course_index][1]}): ").strip().upper()
        # Update values if user typed something
        final_id = new_id if new_id else courses[course_index][0]
        final_name = new_name if new_name else courses[course_index][1]
        # Validation: Check if new ID already exists (only if ID changed)
        if final_id != old_id:
            for c in courses:
                if c[0] == final_id:
                    print(f"Error: Course ID {final_id} already exists!")
                    return
        # Update the course list
        courses[course_index] = [final_id, final_name]   
        # If ID changed, we MUST update grades.txt so marks aren't lost
        if final_id != old_id:
            grades = read_file(GRADES_FILE)
            updates_count = 0
            for g in grades:
                if g[1] == old_id:
                    g[1] = final_id
                    updates_count += 1
            save_file(GRADES_FILE, grades)
            print(f"Updated {updates_count} student grade records to new Course ID.")
        save_file(COURSES_FILE, courses)
        print("Course updated successfully!")
    
    #robust error-handling
    except FileNotFoundError:  
        print("Error: The database file is missing.")
        return
    except Exception as reason:
        print(f"Unexpected error occured: {reason}")
        return

#set for main function    
def all_files():
    #Ensure that required data files exist by creating empty files for students, courses, and grades if missing
    for f in [STUDENTS_FILE, COURSES_FILE, GRADES_FILE]:
        if not os.path.exists(f):
            with open(f, 'w', encoding="utf-8"): #all of our codes uses with open() syntax for auto closing of files
                pass

def main():
    #program's entry point and central controller by displaying menu and receiving user input, calling functions 
    all_files()
    while True:         #always show menu until user exit(it will break loop)
        print(f"\n\nFiles are being saved to: {os.getcwd()}")   #show current file location to help user find the .txt files 
        print('\n=== Student Grading System ===')
        print('1. Add Student')
        print('2. Add Course')
        print('3. Record Marks')
        print('4. Display Student Performance')
        print('5. Display Course Summary')
        print('6. Export Student Report')
        print('--- EDIT / DELETE ---')
        print('7. Delete Student (Fix Typo/Remove)')
        print('8. Delete Specific Mark (Fix Wrong Entry)')
        print('9. Edit Course (Rename/Fix Typo)')
        print('0. Exit')
        choice = input('Enter choice: ').strip()
        if choice == '1': 
            add_student()
        elif choice == '2': 
            add_course()
        elif choice == '3': 
            record_marks()
        elif choice == '4': 
            display_student()
        elif choice == '5': 
            display_course()
        elif choice == '6': 
            export_report()
        elif choice == '7': 
            delete_student()
        elif choice == '8': 
            delete_mark()
        elif choice == '9': 
            edit_course()
        elif choice == '0':     #to exit cutely and gracefully by adding more fun rather than just plain exit
            message = "Thank you for using Student Grading System powered by Arthur Tsen Khiam Tseng, Ding JunChen, Goh Pei Jia, Jiang ShengJi and Ow Qian Yie 👋🏻"
            for char in message:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.05)
            print()
            sys.exit(0)
        else:
            print('Invalid choice!')
        
        #to clear screen after each operation for better user experience
        time.sleep(2)  #pause for 2 seconds before clearing screen
        if os.name == "posix":
            os.system('clear')  #for linux and macOS
        elif os.name == "nt":
            os.system('cls')    #for windows

if __name__ == '__main__':
    main()

