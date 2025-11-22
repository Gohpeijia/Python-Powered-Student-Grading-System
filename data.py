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

import os       #for file operations 

STUDENTS_FILE = 'students.txt'
COURSES_FILE = 'courses.txt'
GRADES_FILE = 'grades.txt'

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
            return
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
        return
    #get student email 
    try:
        email = input('Enter Student Email (xxxxxxxx@imail.sunway.edu.my): ').strip().lower()
        if not email.endswith("@imail.sunway.edu.my"):          #ensure email ends with @imail.sunway.edu.my
            raise ValueError("Email must end with @imail.sunway.edu.my")
    except ValueError:          #runs only no have '@imail.sunway.edu.my' in user's input
        print("Error: No '@imail.sunway.edu.my' found in your input.")
        return

    #save to file and runs when all input are correct
    try:
        with open(STUDENTS_FILE, 'a') as f:
            f.write(f'{sid},{name},{email}\n')
        print('Student added successfully!')
    except Exception as reason:         #exception = type of error (file missing, permission denied and more)   reason= to show why crash (shows file name) #no need raise anything about it, python will product it
        print(f"Error saving file: {reason}")

def add_course():
    try:
        #get course id
        cid = input('Enter Course ID (CSC1024) : ').strip().upper()
        if not cid:
            raise ValueError("Empty input") # check if empty, if empty force the crash(type again)
        if ',' in cid:
            raise ValueError("Course ID cannot contain commas")
        courses = read_file(COURSES_FILE)
        for c in courses:
            if c[0] == cid:
                raise ValueError(f"Course ID '{cid}' already exists")  #prevent duplicate course ID in file
        cname = input('Enter Course Name (PROGRAMMING PRINCIPLES) : ').strip().upper()
        if not cname:
            raise ValueError("Course Name cannot be empty ") # check if empty, if empty force the crash(type again)
        if ',' in cname or '.' in cname:
            raise ValueError("Course Name cannot contain commas (use space instead)")
        #save to file if all input are valid
        with open(COURSES_FILE, 'a') as f:
            f.write(f'{cid},{cname}\n')
        print('Course added successfully!')

    except ValueError as reason:  #occur when empty ID or empty name
        print(f'Invalid input {reason}, please try again:')
        return
    except Exception as reason:
        print(f"Error saving file: {reason}")
        return

def record_marks():
    #get student ID
    try:
        sid = int(input('Enter Student ID (251xxxxx) : ').strip())
        students = read_file(STUDENTS_FILE)
        student_ids = [s[0] for s in students] #list of all student IDs in file
        if str(sid) not in student_ids:
            raise ValueError("Student ID not found in records") #check .txt file have this student or not
    except ValueError as reason:   # occur when user typo that cause the current id not in file
        print(f'Invalid input: {reason}')
        return    
    #get course ID
    try:
        cid = input('Enter Course ID (CSC1024) : ').strip().upper()
        if not cid: 
            raise ValueError("Empty input") # Check if empty, if empty force the crash(type again)
        courses = read_file(COURSES_FILE)
        course_ids = [c[0] for c in courses] #list of all course IDs in file
        if cid not in course_ids:
            raise ValueError("Course ID not found in records")  #raise error if course id not found in file
    except ValueError as reason:          #check .txt file have this course or not
        print(f'Error:{reason}.PLease add course first.')
        return
    #get marks
    try:
        marks = float(input('Enter marks (0-100): '))
        if marks < 0 or marks > 100:            # marks mut in -1<marks<101
            print("Error: Marks must be between 0 and 100.")
            return # STOP here
    except ValueError:
        print('Error: Marks must be a number (80.5)')
        return
    #save data
    #only run when all inputs are valid
    grade = marks_to_grade(marks)
    try:
        with open(GRADES_FILE, 'a') as f:
            f.write(f'{sid},{cid},{marks},{grade}\n')    #format to save in files
        print(f'Success! Marks recorded. Grade = {grade}')
    except Exception as reason:         #'reason' will shows why error happened
        print(f"Error saving to file: {reason}")     #output : Error saving to file: [Errno 13] Permission denied: 'grades.txt'

def display_student():
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
                    if count > 0:
                        print(f'Average Marks: {total / count:.2f}')
                    else:
                        print('No grades recorded yet.')
                    break   #exit loop after finding student
            if not found:
                print('Student not found!')
        else:
            raise ValueError("Sunway student ID must be 8 numbers")
    except ValueError as reson:
        print(f'Invalid student id: {reason}')   
    except Exception as reason:
        print(f'System Error:{reason}')

def display_course():
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
            print('Course not found!')
    except ValueError as reason:           #occur when user error input like empty course id taht can be predicted
        # Catches empty input or corrupted numbers in file
        print(f"Invalid operation: {reason}")
        
    except Exception as reason:         #occur when file missing or other crash that cant be predicted
        # Catches file missing errors or other crashes
        print(f"An error occurred: {reason}")
    #need two except block to separate predictable and unpredictable error

def export_report():
    try:
        sid = input('Enter Student ID to export (251xxxxx) : ').strip()
        sid = str(int(sid))           #convert to string for len() check
        if len(sid) != 8:
            raise ValueError("Sunway Student ID must be 8 digits")
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
        raise ValueError('Student not found!')      
    except ValueError as reason:
        print(f"Invalid input: {reason}")
    except Exception as reason:
        print(f"System Error: {reason}")


# menu
def main():
    ensure_files()
    while True:         #always show menu until user exit(it will break loop)
        print('\n=== Student Grading System ===')
        print('1. Add Student')
        print('2. Add Course')
        print('3. Record Marks')
        print('4. Display Student Performance')
        print('5. Display Course Summary')
        print('6. Export Student Report')
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
        elif choice == '0':
            print('Goodbye!')
            break
        else:
            print('Invalid choice!')

if __name__ == '__main__':
    main()