#!/usr/bin/python3

from config import GRADING_DIR, BASE_DIR, GRADES_DIR, DROPPED_STUDENTS
import os
import sys
import shutil
import csv

TOTAL_LINE_OFFSET = 5

if(len(sys.argv) != 3):
    print("Wrong number of arguments! Usage: ./finalize_grading.py <assignment> <blackboardID>")
    exit()
    
BASE_GRADING_DIR = GRADING_DIR + sys.argv[1]
if(not os.path.exists(BASE_GRADING_DIR)):
    print(BASE_GRADING_DIR, 'must be set to the grading directory')
    print("That assignment does not exist! Did you spell it correctly?")
    exit()

BASE_GRADE_FILE_DIR = GRADES_DIR + sys.argv[1]
if(os.path.exists(BASE_GRADE_FILE_DIR)):
    print("Grade File Directory " + sys.argv[1] + " already exists... would you like to overwrite?")
    if(input("Enter 'yes' to confirm, anything else to quit: ").lower() == "yes"):
        shutil.rmtree(BASE_GRADE_FILE_DIR)
    else:
        exit()

try:
    blackboardID = int(sys.argv[2])
except ValueError:
    print(sys.argv[2], "is not a valid integer for the Blackboard Column ID!")
        
os.mkdir(BASE_GRADE_FILE_DIR)

main_sectioning_file = open(BASE_GRADE_FILE_DIR + "/" + sys.argv[1] + "_sectioning.csv", "w")
main_grade_file = open(BASE_GRADE_FILE_DIR + "/" + sys.argv[1] + "_grades.csv", "w")

main_grade_file.write("Username," + sys.argv[1] + "|" + str(sys.argv[2]) + "\n")

copy_header = True
for grading_folder in os.scandir(BASE_GRADING_DIR):
    ta_folder = grading_folder.path
    ta_name = ta_folder.split("/")[len(ta_folder.split("/")) - 1]
    if(ta_name != "IO_files" and ta_name != "grading_scripts" and ta_name != sys.argv[1] + "_IO"):
        sectioning_path = ta_folder + "/" + "sectioning.csv"
        try:
            ta_sectioning_file = open(sectioning_path, "r")
            sectioning_lines = ta_sectioning_file.readlines()
            ta_sectioning_file.close()
            if(copy_header == True):
                for line in sectioning_lines:
                    main_sectioning_file.write(line)
                    copy_header = False
            else:
                for line in sectioning_lines[1:]:
                    main_sectioning_file.write(line)
        except IOError:
            print(ta_name, "does not have a 'sectioning.csv' file in their grading directory! Did they finish grading the assignment?")

        for student_folder in os.scandir(ta_folder):
            if(os.path.isdir(student_folder.path)):
                student_name = student_folder.path.split("/")[len(student_folder.path.split("/")) - 1]
                if student_name not in DROPPED_STUDENTS:
                    compiled_rubric_path = student_folder.path + "/" + "compiled_rubric.txt"
                    try:
                        compiled_file = open(compiled_rubric_path, "r")
                        compiled_lines = compiled_file.readlines()
                        compiled_file.close()
                        total_line = compiled_lines[len(compiled_lines) - TOTAL_LINE_OFFSET]
                        total_line_list = total_line.split(":")
                        grade_object = total_line_list[1]
                        grade_list = grade_object.split("/")
                        student_grade = float(grade_list[0].strip()) # If this throws a ValueError, good luck
                        main_grade_file.write(student_name + "," + str(student_grade) + "\n")
                    except IOError:
                        print(student_name, "does not have a 'compiled_rubric.txt'! The TA is", ta_name + "!")
main_sectioning_file.close()
main_grade_file.close()
