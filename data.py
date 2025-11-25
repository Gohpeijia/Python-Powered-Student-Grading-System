"""
CSC1024 Programming Principles Final Project
Python-Powered Student Grading System (Intermediate Version)
-----------------------------------------------------------
Features:
1. Add new student
2. Add new course
3. Record student marks (auto letter grade)
4. Display student performance
5. Display course summary
6. Export simple report
7. Exit program

Files created:
- students.txt  : student_id, name, email
- courses.txt   : course_id, course_name
- grades.txt    : student_id, course_id, marks, grade

all example of student, course and grades are in sunway university format
sid=student ID (251xxxxx) only 8-digits
name=student name (no numbers or special characters)
gmail=student email (xxxxxxxx@imail.sunway.edu.my)
cid=course ID (e.g., CSC1024)
canme=course name   (e.g., Programming Principles)
marks= numeric marks (0-100)
grade= letter grade (A, B, C, D, F)

Simplified design for easier understanding and viva explanation.
"""

import os

# find the path of python file 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# let the text files to be in the same folder as data.py prevent file save in wrong folder
STUDENTS_FILE = os.path.join(BASE_DIR, 'students.txt')
COURSES_FILE = os.path.join(BASE_DIR, 'courses.txt')
GRADES_FILE = os.path.join(BASE_DIR, 'grades.txt')

def ensure_files():
    for f in [STUDENTS_FILE, COURSES_FILE, GRADES_FILE]:
        if not os.path.exists(f):
            open(f, 'w').close()


def marks_to_grade(marks):
    if marks >= 85:
        return 'A'
    elif marks >= 70:
        return 'B'
    elif marks >= 60:
        return 'C'
    elif marks >= 50:
        return 'D'
    else:
        return 'F'

def read_file(filename):
    with open(filename, 'r') as f:
        return [line.strip().split(',') for line in f if line.strip()]


def add_student():
    print('\n=== Add New Student ===')
    while True:
    #get student ID (sid)
        try:
            sid = int(input('Enter Student ID (251xxxxx) : ').strip())
            if len(str(sid)) != 8:          #must change to str because len() only works on string
                raise ValueError("Sunway student ID must be 8 digits")
            students = read_file(STUDENTS_FILE)
            for s in students:                  #prevent duplicate student ID in file
                if s[0] == str(sid):
                    raise ValueError("Student ID already exists")   
        except ValueError as reason:            # this shows what error (not number and not 8-digits)
                print(f"Invalid input: {reason}")
                again = input("Error: Invalid student ID. Do you want to continue? (y/n): ").strip().lower()
                if again != 'y':
                    return # back to main()
                continue
        #get student name 
        try:
            name = input('Enter Student Name (Name per NRIC) : ').strip().upper()
            if not name:
                raise ValueError ("Name cannot be empty")
            if any(char.isdigit() for char in name):            #check name has numbers or not
                raise ValueError("Name cannot contain numbers")
            if ',' in name or '.' in name:
                raise ValueError("Name cannot contain symbol (use space instead)")
        except ValueError as reason:
            print(f'Invalid name:{reason}')
            again = input("Error: Invalid name. Do you want to continue? (y/n): ").strip().lower()
            if again != 'y':
                return # back to main()
            continue
        #get student email 
        try:
            email = input('Enter Student Email (xxxxxxxx@imail.sunway.edu.my): ').strip().lower()
            if not email.endswith("@imail.sunway.edu.my"):          #ensure email ends with @imail.sunway.edu.my
                raise ValueError("Email must end with @imail.sunway.edu.my")
        except ValueError:          #runs only no have '@imail.sunway.edu.my' in user's input
            print("Error: No '@imail.sunway.edu.my' found in your input.")
            again = input("Error: Invalid email format. Do you want to continue? (y/n): ").strip().lower()
            if again != 'y':
                return # back to main()
            continue

        #save to file and runs when all input are correct
        try:
            with open(STUDENTS_FILE, 'a') as f:
                f.write(f'{sid}, {name}, {email}\n')
            print('Student added successfully!')
        except Exception as reason:         #exception = type of error (file missing, permission denied and more)   reason= to show why crash (shows file name) #no need raise anything about it, python will product it
            print(f"Error saving file: {reason}")
       
        #ask to continue or exit
        again = input("\nAdd another student? (y/n): ").strip().lower()
        if again != 'y':
            break # back to main()

def add_course():
    print('\n=== Add New Course ===')
    while True:
        try:
            validid = False
            #get course id
            
            for attempt in range(3):  # allow user to retype 3 times if empty input
                cid = input('Enter Course ID (CSC1024) and only three attempts : ').strip().upper()
                # check empty
                if not cid:
                    print(f"Input cannot be empty. (Attempt {attempt+1}/3)")
                    continue # ask again
                # check commas
                elif ',' in cid or '.' in cid:
                    print(f"Course ID cannot contain commas. (Attempt {attempt+1}/3)")
                    continue # ask again
                elif len(cid) != 7:
                    print(f"Course ID must be 7 characters long. (Attempt {attempt+1}/3)")
                    continue # ask again
                # check duplicates
                courses = read_file(COURSES_FILE)
                is_duplicate = False
                for c in courses:
                    if c[0] == cid:
                        is_duplicate = True
                        break
                if is_duplicate:
                    print(f"Course ID '{cid}' already exists. (Attempt {attempt+1}/3)")
                    continue # ask again
                valid_id = True
                break # exit the "3 attempts" loop
            # check if loop finished without success
            if not valid_id:
                # if failed 3 times, ask stop or not
                again = input("Too many invalid attempts. Do you want to continue? (y/n): ").strip().lower()
                if again != 'y':
                    return # go back to main menu
                else:
                    continue # restart the big while loop (start from scratch)

            # get course name
            validcname = False
            
            for attempt in range(3):  # allow user to retype 3 times if empty input
                cname = input('Enter Course Name (PROGRAMMING PRINCIPLES) : ').strip().upper()
                if not cname:
                    print(f"Course Name cannot be empty. (Attempt {attempt+1}/3)")
                    continue # ask again
                if ',' in cname:
                    print(f"Course Name cannot contain commas. (Attempt {attempt+1}/3)")
                    continue # ask again
                validcname = True
                break # exit the "3 attempts" loop
            if not validcname:
                # if failed 3 times, ask stop or not
                again = input("Too many invalid attempts. Do you want to continue? (y/n): ").strip().lower()
                if again != 'y':
                    return # go back to main menu
                else:
                    continue # restart the big while loop (retart from cid)

            #save to file
            with open(COURSES_FILE, 'a') as f:
                f.write(f'{cid}, {cname}\n')
            print('Course added successfully!')

        except ValueError as reason:
            print(f'Invalid input: {reason}')
        
        except Exception as reason:
            print(f"Error saving file: {reason}")
        
        # ask to add another course
        again = input("\nAdd another course? (y/n): ").strip().lower()
        if again != 'y':
            return #back to main()

def record_marks():
    print('\n=== Record Student Marks ===')
    while True:         # Outer Loop to add marks for multiple students
        while True:
            try:
                #get student ID
                try:
                    sid = int(input('Enter Student ID (251xxxxx) : ').strip())
                except ValueError:
                    raise ValueError("ID must be a number")
                students = read_file(STUDENTS_FILE)
                student_ids = [s[0] for s in students] #list of all student IDs in file
                if str(sid) not in student_ids:
                    raise ValueError(f"Student ID {sid} not found in records")
                break       # move to Course ID

            except ValueError as reason:   # occur when user input alphabet that cause the current id not in file
                print(f'Invalid input: {reason}')
                again = input("Student ID not found in records. Do you want to continue? (y/n): ").strip().lower()          ##check .txt file have this student or not .If not,ask to continue or exit
                if again != 'y':
                    return # back to main()
                    
                
                #get course ID
        while True:
                try:
                    cid = input('Enter Course ID (CSC1024) : ').strip().upper()
                    if not cid: 
                        raise ValueError("Empty input")
                    
                    courses = read_file(COURSES_FILE)       
                    course_ids = [c[0] for c in courses] #list of all course IDs in file
                    if cid not in course_ids:
                        raise ValueError(f"Course ID {cid} not found in records")
                    break       # move to marks

                except ValueError as reason:          #check .txt file have this course or not
                    print(f'Error:{reason}.PLease add course first.')
                    again = input("Course ID not found in records. Do you want to continue adding other course marks? (y/n): ").strip().lower()          #prevent empty input .If not,ask to continue or exit
                    if again != 'y':
                        return # back to main() 
                    
                #get marks
        while True:
            try:
                try:
                    marks = float(input('Enter marks (0-100): '))
                except ValueError:
                        raise ValueError("Marks must be a number")
                if marks < 0 or marks > 100:            # marks mut in -1<marks<101                    
                    raise ValueError("Marks must be between 0 and 100")
                break      # move to save data

            except ValueError as reason:
                print(f'Invalid input: {reason}')
                again = input("Error: Marks must be between 0 and 100. Try agian? (y/n): ").strip().lower()
                if again != 'y':
                    return # back to main()  If 'y', the inner loop repeats (asking for Marks again)
                    

                #save data
            try:
                #only run when all inputs are valid
                grade = marks_to_grade(marks)
                with open(GRADES_FILE, 'a') as f:
                    f.write(f'{sid}, {cid}, {marks}, {grade}\n')    #format to save in files
                print(f'Success! Marks recorded. Grade = {grade}')

            except Exception as reason:
                print(f"System Error saving file: {reason}")
                return
        again = input("\nRecord marks for another student? (y/n): ").strip().lower()
        if again != 'y':
            break # Exit Outer Loop (Back to Main Menu)

def display_student():
    print('\n=== Display Student Performance ===')
    try:
        sid = input('Enter Student ID (251xxxxx) : ').strip()
        sid = str(int(sid))           #convert to string for len() check
        if len(str(sid)) == 8:
            #studet's data will be read from file
            students = read_file(STUDENTS_FILE)
            grades = read_file(GRADES_FILE)
            found = False
            for s in students:
                if s[0] == sid:
                    found = True            #if found student, then display info
                    print(f'\nStudent: {s[1]} ({s[0]})')
                    print('Email:', s[2])
                    print('\nCourses and Grades:')
                    total = 0
                    count = 0
                    for g in grades:
                        #check grades file for matching student id
                        if g[0] == sid:
                            print(f'Course: {g[1]}, Marks: {g[2]}, Grade: {g[3]}')
                            total += float(g[2])
                            count += 1
            if not found:
                print('Student not found!')
        else:
            raise ValueError("Sunway student ID must be 8 numbers")
    except ValueError as reason:
        print(f'Invalid student id: {reason}')   
    except Exception as reason:
        print(f'System Error:{reason}')

def display_course():
    print('\n=== Display Course Summary ===')
    try:
        cid = input('Enter Course (CSC1024) : ').strip().upper()
        if not cid:
            raise ValueError("Course ID cannot be empty") # check if empty, if empty force the crash(type again)
        #real data from files
        courses = read_file(COURSES_FILE)
        grades = read_file(GRADES_FILE)
        found = False
        for c in courses:
                #look for course id in courses file
            if c[0] == cid:
                found = True
                print(f'\nCourse: {c[1]} ({c[0]})')
                # Note: This line will crash if grades file has text instead of numbers.
                # The 'except' block below will catch it if that happens.
                course_grades = [float(g[2]) for g in grades if g[1] == cid]
                if not course_grades:
                    print('No grades recorded yet.')
                    return      # Stop here if no grades
                print(f'Average: {sum(course_grades)/len(course_grades):.2f}')
                print(f'Highest: {max(course_grades)}')
                print(f'Lowest : {min(course_grades)}')
                break   #exit loop after finding course
        if not found:
            print('Course not found, exiting...')
    except ValueError as reason:           #occur when user error input like empty course id taht can be predicted
        # Catches empty input or corrupted numbers in file
        print(f"Invalid operation: {reason}")
        
    except Exception as reason:         #occur when file missing or other crash that cant be predicted
        # Catches file missing errors or other crashes
        print(f"An error occurred: {reason}")
    #need two except block to separate predictable and unpredictable error

def export_report():
    print('\n=== Export Student Report ===')
    try:
        sid = input('Enter Student ID to export (251xxxxx) : ').strip()
        sid = str(int(sid))           #convert to string for len() check
        if len(sid) != 8:
            raise ValueError("Sunway Student ID must be 8 digits, exiting...")
        students = read_file(STUDENTS_FILE)         #find student first then read grades file
        for s in students:
            if s[0] == sid:
                grades = read_file(GRADES_FILE)
                filename = f'report_{sid}.txt'
                with open(filename, 'w') as f:
                    f.write(f'Student: {s[1]} ({s[0]})\nEmail: {s[2]}\n\n')
                    for g in grades:
                        if g[0] == sid:
                            f.write(f'Course: {g[1]}, Marks: {g[2]}, Grade: {g[3]}\n')
                print(f'Report saved as {filename}')
                return
        raise ValueError('Student not found,exiting...')      
    except ValueError as reason:
        print(f"Invalid input: {reason}")
    except Exception as reason:
        print(f"System Error: {reason}")

def delete_student():
    print('\n=== Delete Student Record ===')
    while True:
        try:
            # 1. Get ID
            sid_input = input('Enter Student ID to DELETE (251xxxxx): ').strip()
            
            # Simple Validation
            try:
                sid = int(sid_input)
            except ValueError:
                print("Invalid input: ID must be a number.")
                if input("Try again? (y/n): ").lower() != 'y': return
                continue

            # 2. Check if student exists
            students = read_file(STUDENTS_FILE)
            student_found = False
            for s in students:
                if s[0] == str(sid):
                    student_found = True
                    print(f"Found Student: {s[1]} ({s[0]})")
                    break
            
            if not student_found:
                print("Student ID not found.")
                if input("Try again? (y/n): ").lower() != 'y': return
                continue

            # 3. Confirmation
            confirm = input(f"WARNING: This will delete Student {sid} AND all their grades.\nAre you sure? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Deletion cancelled.")
                return

            # 4. DELETE FROM STUDENTS FILE
            # We create a new list that contains EVERYONE EXCEPT the deleted student
            new_students = []
            for s in students:
                if s[0] != str(sid): # Keep this student
                    new_students.append(s)
            
            # Write the new list back to the file (Overwriting old data)
            with open(STUDENTS_FILE, 'w') as f:
                for s in new_students:
                    f.write(f'{s[0]}, {s[1]}, {s[2]}\n')

            # 5. DELETE FROM GRADES FILE
            # We must also remove their marks to avoid "Ghost Data"
            grades = read_file(GRADES_FILE)
            new_grades = []
            deleted_grades_count = 0
            
            for g in grades:
                if g[0] != str(sid): # Keep this grade
                    new_grades.append(g)
                else:
                    deleted_grades_count += 1
            
            with open(GRADES_FILE, 'w') as f:
                for g in new_grades:
                    f.write(f'{g[0]}, {g[1]}, {g[2]}, {g[3]}\n')

            print(f"Success! Student {sid} deleted.")
            print(f"Also removed {deleted_grades_count} grade record(s) for this student.")
            return

        except Exception as e:
            print(f"System Error: {e}")
            return

# menu
def main():
    ensure_files()
    while True:         #always show menu until user exit(it will break loop)
        print(f"\n\nFiles are being saved to: {os.getcwd()}")   #show current file location to help user find the .txt files 
        print('\n=== Student Grading System ===')
        print('1. Add Student')
        print('2. Add Course')
        print('3. Record Marks')
        print('4. Display Student Performance')
        print('5. Display Course Summary')
        print('6. Export Student Report')
        print('7. Delete Student')
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
        elif choice == '0':
            print('Goodbye!')
            break
        else:
            print('Invalid choice!')

if __name__ == '__main__':
    main()