#!/usr/bin/python3

from config import GRADING_DIR, SUBMIT_DIR, TA_DICT, ROSTER, BASE_DIR, TA_NAME_ID_DICT, DROPPED_STUDENTS
import os
import sys
import shutil
import csv

IO_FOLDER = BASE_DIR + "IO_files"
RUBRIC_FOLDER = BASE_DIR + "rubrics"
MAKEFILE_FOLDER = BASE_DIR + "makefiles"
SCRIPT_FOLDER = BASE_DIR + "grading_scripts"
NONMAJOR_EXT = "_NONMAJORS"
MAJOR_EXT = "_MAJORS"
NONMAJOR_TAS = ["mhambre1", "shender2"] # Allows grouping of work to separate majors/nonmajors
sections = "All"

# Load nameID >> Full Name Dictionary
student_nameIdDict = {}
with open('student_nameID_Dict.csv') as nameIdList:
    readList = csv.reader(nameIdList)
    student_nameIdDict = dict(readList)

def copy_makefile(base_makefile_path, student_grade_folder):
    source_makefile = open(base_makefile_path, "r")
    if(os.path.exists(student_grade_folder + "/Makefile")):
        os.remove(student_grade_folder + "/Makefile")
    dest_makefile = open(student_grade_folder + "/Makefile", "x")
    dest_makefile.writelines(source_makefile.readlines())
    source_makefile.close()
    dest_makefile.close()

if(len(sys.argv) != 3):
    print("Wrong number of arguments! Usage: ./setup_grading.py <assignment> <--majors | --nonmajors | --all>")
    exit()
else:
    if(sys.argv[2] == "--majors"):
        sections = "Majors"
    elif(sys.argv[2] == "--nonmajors"):
        sections = "Nonmajors"
    elif(sys.argv[2] == "--all"):
        sections = "All"
    else:
        print("Must select either '--majors', '--nonmajors', or '--all' to configure grouping.")
        exit()
    
BASE_SUBMIT_DIR = SUBMIT_DIR + sys.argv[1]
if(not os.path.exists(BASE_SUBMIT_DIR)):
    print("That assignment does not exist! Did you spell it correctly?")
    exit()

roster_file = open(ROSTER, "r")
roster_lines = roster_file.readlines()

# Load nameID >> Full Name Dictionary
nameIdDict = {}
with open('student_nameID_Dict.csv') as nameIdList:
    readList = csv.reader(nameIdList)
    nameIdDict = dict(readList)

if(sections == "Majors"):
    base_grading_dir = GRADING_DIR + sys.argv[1] + MAJOR_EXT

    print("Copying over grading_scripts directory...")
    shutil.rmtree(base_grading_dir + "/grading_scripts") 
    shutil.copytree(SCRIPT_FOLDER, base_grading_dir + "/grading_scripts") 

    if(os.path.exists(base_grading_dir)):
        print("Grading Directory " + sys.argv[1] + MAJOR_EXT + " already exists... would you like to overwrite?")
        if(input("Enter 'yes' to confirm, anything else to quit: ").lower() != "yes"):
            exit()
    
    # This is horribly inefficient.. whose idea was it to do a dictionary this way?
    for TA in TA_DICT:
        if TA not in NONMAJOR_TAS:
            curr_ta_folder = base_grading_dir + "/" + TA
            print("Replacing makefile for " + sys.argv[1] + MAJOR_EXT + " in grading directory for", TA)
            for student_section in roster_lines:
                curr_student, curr_section = student_section.split(",")
                if int(curr_section) in TA_DICT[TA] and curr_student not in DROPPED_STUDENTS:
                    student_grade_folder = curr_ta_folder + "/" + curr_student 
                    makefile_path = MAKEFILE_FOLDER + "/" + sys.argv[1] + MAJOR_EXT + "_Makefile"
                    if(os.path.exists(makefile_path)):
                        copy_makefile(makefile_path, student_grade_folder)


elif(sections == "Nonmajors"):
    base_grading_dir = GRADING_DIR + sys.argv[1] + NONMAJOR_EXT
    
    print("Copying over grading_scripts directory...")
    shutil.rmtree(base_grading_dir + "/grading_scripts") 
    shutil.copytree(SCRIPT_FOLDER, base_grading_dir + "/grading_scripts") 

    if(os.path.exists(base_grading_dir)):
        print("Grading Directory " + sys.argv[1] + NONMAJOR_EXT + " already exists... would you like to overwrite?")
        if(input("Enter 'yes' to confirm, anything else to quit: ").lower() != "yes"):
            exit()

    # This is horribly inefficient.. whose idea was it to do a dictionary this way?
    for TA in TA_DICT:
        if TA in NONMAJOR_TAS:
            curr_ta_folder = base_grading_dir + "/" + TA
            print("Replacing makefile for " + sys.argv[1] + MAJOR_EXT + " in grading directory for", TA)
            for student_section in roster_lines:
                curr_student, curr_section = student_section.split(",")
                if int(curr_section) in TA_DICT[TA] and curr_student not in DROPPED_STUDENTS:
                    student_grade_folder = curr_ta_folder + "/" + curr_student 
                    makefile_path = MAKEFILE_FOLDER + "/" + sys.argv[1] + MAJOR_EXT + "_Makefile"
                    if(os.path.exists(makefile_path)):
                        copy_makefile(makefile_path, student_grade_folder)
