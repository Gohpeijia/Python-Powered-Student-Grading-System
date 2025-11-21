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

Simplified design for easier understanding and viva explanation.
"""

# ------------------------ Imports ------------------------
import os

# ------------------------ File Setup ------------------------
STUDENTS_FILE = 'students.txt'
COURSES_FILE = 'courses.txt'
GRADES_FILE = 'grades.txt'

def ensure_files():
    for f in [STUDENTS_FILE, COURSES_FILE, GRADES_FILE]:
        if not os.path.exists(f):
            open(f, 'w').close()

# ------------------------ Helper Functions ------------------------

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

def write_file(filename, lines):
    with open(filename, 'w') as f:
        for line in lines:
            f.write(','.join(line) + '\n')

# ------------------------ Main Functions ------------------------

def add_student():
    try:
        sid = int(input('Enter Student ID: ').strip())
    except ValueError:
        print('Invalid input of Sunway student ID,please try again in integer only:')
        return
    try:
        name = str(input('Enter Student Name: ').strip())
    except ValueError:
        print('Invalid input of Sunway student name, please try again:')
        return
    try:
        email = input('Enter Student Email (xxxxxxxx@imail.sunway.edu.my): ').strip()
        email.index("@imail.sunway.edu.my")
    except ValueError:          #runs only no have '@imail.sunway.edu.my' in user's input
        print("Error: No '@imail.sunway.edu.my' found in your input.")

    with open(STUDENTS_FILE, 'a') as f:
        f.write(f'{sid},{name},{email}\n')
    print('Student added successfully!')

def add_course():
    try:
        #get course id
        cid = input('Enter Course ID: ').strip()
        if not cid:
            raise ValueError("Empty input") # check if empty, if empty force the crash(type again)
        cname = str(input('Enter Course Name: ').strip())
        if not cname:
            raise ValueError("Course Name cannot be empty ") # check if empty, if empty force the crash(type again)
        
        #save to file if all input are valid
        with open(COURSES_FILE, 'a') as f:
            f.write(f'{cid},{cname}\n')
        print('Course added successfully!')

    except ValueError as reason:  #occur when empty ID or empty name
        print(f'Invalid input {reason}, please try again:')
        return

def record_marks():
    #get student ID
    try:
        sid = int(input('Enter Student ID (250xxxxx): ').strip())
    except ValueError:   # occur when user type an alphabet or typo that cause the current id not in file
        print('Invalid input of Sunway student ID,please try again in numbers only:')
        return    
    #get course ID
    try:
        cid = input('Enter Course ID (CSC1024): ').strip()
        if not cid: 
            raise ValueError("Empty input") # Check if empty, if empty force the crash(type again)
    except ValueError:          #check .txt file have this course or not
        print('Invalid input of Sunway Course name, please try again:')
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
            f.write(f'{sid},{cid},{marks},{grade}\n')
        print(f'Success! Marks recorded. Grade = {grade}')
    except Exception as reason:         #'reason' will shows why error happened
        print(f"Error saving to file: {reason}")     #output : Error saving to file: [Errno 13] Permission denied: 'grades.txt'

def display_student():
    sid = input('Enter Student ID: ').strip()
    students = read_file(STUDENTS_FILE)
    grades = read_file(GRADES_FILE)
    found = False
    for s in students:
        if s[0] == sid:
            found = True
            print(f'\nStudent: {s[1]} ({s[0]})')
            print('Email:', s[2])
            print('\nCourses and Grades:')
            total = 0
            count = 0
            for g in grades:
                if g[0] == sid:
                    print(f'Course: {g[1]}, Marks: {g[2]}, Grade: {g[3]}')
                    total += float(g[2])
                    count += 1
            if count > 0:
                print(f'Average Marks: {total / count:.2f}')
            else:
                print('No grades recorded yet.')
    if not found:
        print('Student not found!')

def display_course():
    cid = input('Enter Course ID: ').strip()
    courses = read_file(COURSES_FILE)
    grades = read_file(GRADES_FILE)
    found = False
    for c in courses:
        if c[0] == cid:
            found = True
            print(f'\nCourse: {c[1]} ({c[0]})')
            course_grades = [float(g[2]) for g in grades if g[1] == cid]
            if not course_grades:
                print('No grades recorded yet.')
                return
            print(f'Average: {sum(course_grades)/len(course_grades):.2f}')
            print(f'Highest: {max(course_grades)}')
            print(f'Lowest : {min(course_grades)}')
    if not found:
        print('Course not found!')

def export_report():
    sid = input('Enter Student ID to export: ').strip()
    students = read_file(STUDENTS_FILE)
    grades = read_file(GRADES_FILE)
    for s in students:
        if s[0] == sid:
            filename = f'report_{sid}.txt'
            with open(filename, 'w') as f:
                f.write(f'Student: {s[1]} ({s[0]})\nEmail: {s[2]}\n\n')
                for g in grades:
                    if g[0] == sid:
                        f.write(f'Course: {g[1]}, Marks: {g[2]}, Grade: {g[3]}\n')
            print(f'Report saved as {filename}')
            return
    print('Student not found!')

# ------------------------ Menu ------------------------

def main():
    ensure_files()
    while True:
        print('\n=== Student Grading System ===')
        print('1. Add Student')
        print('2. Add Course')
        print('3. Record Marks')
        print('4. Display Student Performance')
        print('5. Display Course Summary')
        print('6. Export Student Report')
        print('0. Exit')
        choice = input('Enter choice: ').strip()
        if choice == '1': add_student()
        elif choice == '2': add_course()
        elif choice == '3': record_marks()
        elif choice == '4': display_student()
        elif choice == '5': display_course()
        elif choice == '6': export_report()
        elif choice == '0':
            print('Goodbye!')
            break
        else:
            print('Invalid choice!')

if __name__ == '__main__':
    main()