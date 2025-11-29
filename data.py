"""
to develop a Student Grading System that manages student records and assessment results
to calculate overall grades, assign letter grades, and display class performance summaries
to prevent abrupt crashing of program, we use a lot of try-except block, making our porgram user-friendly
"""
import os       #for file operations 

STUDENTS_FILE = 'students.txt'
COURSES_FILE = 'courses.txt'
GRADES_FILE = 'grades.txt'

def all_files():
    """Ensure that required data files exist by creating empty files for students, courses, and grades if missing"""
    for f in [STUDENTS_FILE, COURSES_FILE, GRADES_FILE]:
        if not os.path.exists(f):
            with open(f, 'w', encoding="utf-8"): #all of our codes uses with open() syntax for auto closing of files
                pass

def read_file(filename):
    """Important fundamental function for all declare functions later, to only store primitive data so no error will be presented in case of empty line or spaces in user input"""
    with open(filename, 'r', encoding="-8") as f:
        return [line.strip().split(',') for line in f if line.strip()]

def add_student():
    """get student personal information such as student ID specifically only in 8 digits format, name, email """
    try:
        student_id = int(input('Enter Student ID (251xxxxx) : ').strip())
        if len(str(student_id)) != 8:          #must change to str because len() only works on string
            raise ValueError("Sunway student ID must be 8 digits")
        students = read_file(STUDENTS_FILE)
        for s in students:                  #prevent duplicate student ID in file
            if s[0] == str(student_id):
                raise ValueError("Student ID already exists")   
    except ValueError as problem:            # this shows what error (not number and not 8-digits)
            print(f"Invalid input: {problem}")
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
    except ValueError as problem:
        print(f'Invalid name:{problem}')
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
        with open(STUDENTS_FILE, 'a', encoding = "utf-8") as f:
            f.write(f'{student_id},{name},{email}\n')
        print('Student added successfully!')
    except Exception as problem:         #exception = type of error (file missing, permission denied and more)   problem= to show why crash (shows file name) #no need raise anything about it, python will product it
        print(f"Error saving file: {problem}")

def add_course():
    """to get course id, course name"""
    try:
        course_id = input('Enter Course ID (CSC1024) : ').strip().upper()
        if not course_id:
            raise ValueError("Empty input") # check if empty, if empty force the crash(type again)
        if ',' in course_id: 
            raise ValueError("Course ID cannot contain commas")
        courses = read_file(COURSES_FILE)
        for c in courses:
            if c[0] == course_id:
                raise ValueError(f"Course ID '{course_id}' already exists")  #prevent duplicate course ID in file
        course_name = input('Enter Course Name (PROGRAMMING PRINCIPLES) : ').strip().upper()
        if not course_name:
            raise ValueError("Course Name cannot be empty ") # check if empty, if empty force the crash(type again)
        if ',' in course_name or '.' in course_name:
            raise ValueError("Course Name cannot contain commas (use space instead)")
        #save to file if all input are valid
        with open(COURSES_FILE, 'a', encoding = "utf-8") as f:
            f.write(f'{course_id},{course_name}\n')
        print('Course added successfully!')

    except ValueError as problem:  #occur when empty ID or empty name
        print(f'Invalid input {problem}, please try again:')
        return
    except Exception as problem:
        print(f"Error saving file: {problem}")
        return

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

def record_marks():
    #get student ID
    try:
        student_id = int(input('Enter Student ID (251xxxxx) : ').strip())
        students = read_file(STUDENTS_FILE)
        student_ids = [s[0] for s in students] #list of all student IDs in file
        if str(student_id) not in student_ids:
            raise ValueError("Student ID not found in records") #check .txt file have this student or not
    except ValueError as problem:   # occur when user typo that cause the current id not in file
        print(f'Invalid input: {problem}')
        return    
    #get course ID
    try:
        course_id = input('Enter Course ID (CSC1024) : ').strip().upper()
        if not course_id: 
            raise ValueError("Empty input") # Check if empty, if empty force the crash(type again)
        courses = read_file(COURSES_FILE)
        course_ids = [c[0] for c in courses] #list of all course IDs in file
        if course_id not in course_ids:
            raise ValueError("Course ID not found in records")  #raise error if course id not found in file
    except ValueError as problem:          #check .txt file have this course or not
        print(f'Error:{problem}.Please add course first.')
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
        with open(GRADES_FILE, 'a', encoding = "utf-8") as f:
            f.write(f'{student_id},{course_id},{marks},{grade}\n')    #format to save in files
        print(f'Success! Marks recorded. Grade = {grade}')
    except Exception as problem:         #'problem' will shows why error happened
        print(f"Error saving to file: {problem}")     #output : Error saving to file: [Errno 13] Permission denied: 'grades.txt'

def display_student():
    """display individual student performance including all enrolled courses and grades"""
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
            if not found:
                print('Student not found!')
        else:
            raise ValueError("Sunway student ID must be 8 numbers")
    except ValueError as reason:
        print(f'Invalid student id:{reason}')   
    except Exception as problem:
        print(f'System Error:{problem}')

def display_course():
    """display course performance summary by listing all students enrolled in a particular course, along with average, highest, and lowest marks"""
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
                    marks = float(record[2])
                    grade = record[3]
                    marks_list.append(marks)
                    print(f"{student_name} ({student_id}): Marks = {marks}, Grade = {grade}")
                total = sum (course_grades)
                average = total / len (course_grades)
                print ('Average:',average)
                max_num = max(course_grades)
                print('Highest: ',max_num)
                min_num = min(course_grades)
                print('Lowest : ',min_num)
                break   #exit loop after finding course
        if not found:
            print('Course not found!')
    except ValueError as problem:           #occur when user error input like empty course id taht can be predicted
        # Catches empty input or corrupted numbers in file
        print(f"Invalid operation: {problem}")
    except Exception as problem:         #occur when file missing or other crash that cant be predicted
        # Catches file missing errors or other crashes
        print(f"An error occurred: {problem}")
    #need two except block to separate predictable and unpredictable error

def export_report():
    """export course summary or individual performance report to text file for record keeping"""
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
                with open(filename, 'w') as f:
                    f.write(f'Student: {s[1]} ({s[0]})\nEmail: {s[2]}\n\n')
                    for g in grades:
                        if g[0] == student_id:
                            f.write(f'Course: {g[1]}, Marks: {g[2]}, Grade: {g[3]}\n')
                print(f'Report saved as {filename}')
                return
        raise ValueError('Student not found!')      
    except ValueError as problem:
        print(f"Invalid input: {problem}")
    except Exception as problem:
        print(f"System Error: {problem}")
        raise ValueError('Student not found,exiting...')      
    except ValueError as reason:
        print(f"Invalid input: {reason}")
    except Exception as reason:
        print(f"System Error: {reason}")


def main():
    """program's entry point and central controller by displaying menu and receiving user input, calling functions """
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
        print('7. Exit')
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
            print('Goodbye!')
            break
        else:
            print('Invalid choice!')

if __name__ == '__main__':
    main()