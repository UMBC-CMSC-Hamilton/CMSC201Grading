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
PYTEST_FILES_FOLDER = BASE_DIR + "pytest_files"
NONMAJOR_EXT = "_NONMAJORS"
MAJOR_EXT = "_MAJORS"
NONMAJOR_TAS = ["mhambre1", "shender2"]  # Allows grouping of work to separate majors/nonmajors
sections = "All"

# Load nameID >> Full Name Dictionary
student_nameIdDict = {}
with open('student_nameID_Dict.csv') as nameIdList:
    readList = csv.reader(nameIdList)
    student_nameIdDict = dict(readList)


def copy_rubric(base_rubric_path, student_grade_folder, student, TA):
    source_rubric_file = open(base_rubric_path, "r")
    rubric_lines = source_rubric_file.readlines()
    source_rubric_file.close()
    rubric_lines[2] = rubric_lines[2].replace("{}", str(TA_NAME_ID_DICT[TA] + " <" + TA + "@umbc.edu>"))
    rubric_lines[3] = rubric_lines[3].replace("{}", str(student_nameIdDict[student] + " <" + student + "@umbc.edu>"))
    dest_rubric_file = open(student_grade_folder + "/rubric.txt", "x")
    dest_rubric_file.writelines(rubric_lines)
    dest_rubric_file.close()


def copy_makefile(base_makefile_path, student_grade_folder):
    source_makefile = open(base_makefile_path, "r")
    dest_makefile = open(student_grade_folder + "/Makefile", "x")
    dest_makefile.writelines(source_makefile.readlines())
    source_makefile.close()
    dest_makefile.close()


def copy_pyfile(base_pytest_path, student_grade_folder, filename):
    source_file = open(base_pytest_path, "r")
    dest_makefile = open(student_grade_folder + "/" + filename, "x")
    dest_makefile.writelines(source_file.readlines())
    source_file.close()
    dest_makefile.close()


if len(sys.argv) != 3:
    print("Wrong number of arguments! Usage: ./setup_grading.py <assignment> <--majors | --nonmajors | --all>")
    exit()
else:
    if sys.argv[2] == "--majors":
        sections = "Majors"
    elif sys.argv[2] == "--nonmajors":
        sections = "Nonmajors"
    elif sys.argv[2] == "--all":
        sections = "All"
    else:
        print("Must select either '--majors', '--nonmajors', or '--all' to configure grouping.")
        exit()

BASE_SUBMIT_DIR = SUBMIT_DIR + sys.argv[1]
if not os.path.exists(BASE_SUBMIT_DIR):
    print("That assignment does not exist! Did you spell it correctly?")
    exit()

roster_file = open(ROSTER, "r")
roster_lines = roster_file.readlines()

# Load nameID >> Full Name Dictionary
nameIdDict = {}
with open('student_nameID_Dict.csv') as nameIdList:
    readList = csv.reader(nameIdList)
    nameIdDict = dict(readList)

if sections == "Majors":
    base_grading_dir = GRADING_DIR + sys.argv[1] + MAJOR_EXT
    if os.path.exists(base_grading_dir):
        print("Grading Directory " + sys.argv[1] + MAJOR_EXT + " already exists... would you like to overwrite?")
        if input("Enter 'yes' to confirm, anything else to quit: ").lower() == "yes":
            shutil.rmtree(base_grading_dir)
        else:
            exit()

    rubric_path = RUBRIC_FOLDER + "/" + sys.argv[1] + MAJOR_EXT + "_rubric.txt"
    if not os.path.exists(rubric_path):
        print(sys.argv[1] + MAJOR_EXT + "_rubric.txt" + " was not found in the rubrics directory! Exiting!")
        exit()

    if not os.path.exists(SCRIPT_FOLDER):
        print("There is no grading_scripts directory in the home folder! You need this!")
        exit()

    os.mkdir(base_grading_dir)
    print("Copying over grading_scripts directory...")
    shutil.copytree(SCRIPT_FOLDER, base_grading_dir + "/grading_scripts")

    base_io_dir = IO_FOLDER + "/" + sys.argv[1] + MAJOR_EXT
    try:
        shutil.copytree(base_io_dir, base_grading_dir + "/IO_files")
        print("Copying over IO_files directory...")
    except FileNotFoundError:
        print("IO Folder not found for " + sys.argv[1] + MAJOR_EXT + "! Skipping...")

    # This is horribly inefficient.. whose idea was it to do a dictionary this way?
    for TA in TA_DICT:
        if TA not in NONMAJOR_TAS:
            curr_ta_folder = base_grading_dir + "/" + TA
            print("Setting up " + sys.argv[1] + MAJOR_EXT + " grading directory for", TA)
            os.mkdir(curr_ta_folder)

            for student_section in roster_lines:
                curr_student, curr_section = student_section.split(",")
                if int(curr_section) in TA_DICT[TA] and curr_student not in DROPPED_STUDENTS:
                    student_submit_folder = BASE_SUBMIT_DIR + "/" + curr_student
                    student_grade_folder = curr_ta_folder + "/" + curr_student
                    os.mkdir(student_grade_folder)
                    copy_rubric(rubric_path, student_grade_folder, curr_student, TA)
                    makefile_path = MAKEFILE_FOLDER + "/" + sys.argv[1] + MAJOR_EXT + "_Makefile"
                    if os.path.exists(makefile_path):
                        copy_makefile(makefile_path, student_grade_folder)
                    pytest_files_path1 = PYTEST_FILES_FOLDER + "/" + "solutions.py"
                    if os.path.exists(pytest_files_path1):
                        copy_pyfile(pytest_files_path1, student_grade_folder, "solutions.py")
                    pytest_files_path1 = PYTEST_FILES_FOLDER + "/" + "hw6_tester.py"
                    if os.path.exists(pytest_files_path1):
                        copy_pyfile(pytest_files_path1, student_grade_folder, "hw6_tester.py")
                    for s_file in os.listdir(student_submit_folder):
                        shutil.copy(student_submit_folder + "/" + s_file, student_grade_folder)

elif sections == "Nonmajors":
    base_grading_dir = GRADING_DIR + sys.argv[1] + NONMAJOR_EXT
    if os.path.exists(base_grading_dir):
        print("Grading Directory " + sys.argv[1] + NONMAJOR_EXT + " already exists... would you like to overwrite?")
        if input("Enter 'yes' to confirm, anything else to quit: ").lower() == "yes":
            shutil.rmtree(base_grading_dir)
        else:
            exit()

    rubric_path = RUBRIC_FOLDER + "/" + sys.argv[1] + NONMAJOR_EXT + "_rubric.txt"
    if not os.path.exists(rubric_path):
        print(sys.argv[1] + NONMAJOR_EXT + "_rubric.txt" + " was not found in the rubrics directory! Exiting!")
        exit()

    if not os.path.exists(SCRIPT_FOLDER):
        print("There is no grading_scripts directory in the home folder! You need this!")
        exit()

    os.mkdir(base_grading_dir)
    print("Copying over grading_scripts directory...")
    shutil.copytree(SCRIPT_FOLDER, base_grading_dir + "/grading_scripts")
    base_io_dir = IO_FOLDER + "/" + sys.argv[1] + NONMAJOR_EXT
    try:
        shutil.copytree(base_io_dir, base_grading_dir + "/IO_files")
        print("Copying over IO_files directory...")
    except FileNotFoundError:
        print("IO Folder not found for " + sys.argv[1] + NONMAJOR_EXT + "! Skipping...")

    # This is horribly inefficient.. whose idea was it to do a dictionary this way?
    for TA in TA_DICT:
        if TA in NONMAJOR_TAS:
            curr_ta_folder = base_grading_dir + "/" + TA
            print("Setting up " + sys.argv[1] + NONMAJOR_EXT + " grading directory for", TA)
            os.mkdir(curr_ta_folder)

            for student_section in roster_lines:
                curr_student, curr_section = student_section.split(",")
                if int(curr_section) in TA_DICT[TA] and curr_student not in DROPPED_STUDENTS:
                    student_submit_folder = BASE_SUBMIT_DIR + "/" + curr_student
                    student_grade_folder = curr_ta_folder + "/" + curr_student
                    os.mkdir(student_grade_folder)
                    copy_rubric(rubric_path, student_grade_folder, curr_student, TA)
                    makefile_path = MAKEFILE_FOLDER + "/" + sys.argv[1] + NONMAJOR_EXT + "_Makefile"
                    if os.path.exists(makefile_path):
                        copy_makefile(makefile_path, student_grade_folder)
                    pytest_files_path1 = PYTEST_FILES_FOLDER + "/" + "solutions.py"
                    if os.path.exists(pytest_files_path1):
                        copy_pyfile(pytest_files_path1, student_grade_folder, "solutions.py")
                    pytest_files_path1 = PYTEST_FILES_FOLDER + "/" + "hw6_tester.py"
                    if os.path.exists(pytest_files_path1):
                        copy_pyfile(pytest_files_path1, student_grade_folder, "hw6_tester.py")
                    for s_file in os.listdir(student_submit_folder):
                        shutil.copy(student_submit_folder + "/" + s_file, student_grade_folder)

else:
    base_grading_dir = GRADING_DIR + sys.argv[1]
    if os.path.exists(base_grading_dir):
        print("Grading Directory " + sys.argv[1] + " already exists... would you like to overwrite?")
        if input("Enter 'yes' to confirm, anything else to quit: ").lower() == "yes":
            shutil.rmtree(base_grading_dir)
        else:
            exit()

    rubric_path = RUBRIC_FOLDER + "/" + sys.argv[1] + "_rubric.txt"
    if not os.path.exists(rubric_path):
        print(sys.argv[1] + "_rubric.txt" + " was not found in the rubrics directory! Exiting!")
        exit()

    if not os.path.exists(SCRIPT_FOLDER):
        print("There is no grading_scripts directory in the home folder! You need this!")
        exit()

    os.mkdir(base_grading_dir)
    print("Copying over grading_scripts directory...")
    shutil.copytree(SCRIPT_FOLDER, base_grading_dir + "/grading_scripts")

    base_io_dir = IO_FOLDER + "/" + sys.argv[1]
    try:
        shutil.copytree(base_io_dir, base_grading_dir + "/IO_files")
        print("Copying over IO_files directory...")
    except FileNotFoundError:
        print("IO Folder not found for " + sys.argv[1] + "! Skipping...")

    # This is horribly inefficient.. whose idea was it to do a dictionary this way?
    for TA in TA_DICT:
        curr_ta_folder = base_grading_dir + "/" + TA
        print("Setting up " + sys.argv[1] + " grading directory for", TA)
        os.mkdir(curr_ta_folder)

        for student_section in roster_lines:
            curr_student, curr_section = student_section.split(",")
            if int(curr_section) in TA_DICT[TA] and curr_student not in DROPPED_STUDENTS:
                student_submit_folder = BASE_SUBMIT_DIR + "/" + curr_student
                student_grade_folder = curr_ta_folder + "/" + curr_student
                os.mkdir(student_grade_folder)
                copy_rubric(rubric_path, student_grade_folder, curr_student, TA)
                makefile_path = MAKEFILE_FOLDER + "/" + sys.argv[1] + "_Makefile"
                if os.path.exists(makefile_path):
                    copy_makefile(makefile_path, student_grade_folder)
                for s_file in os.listdir(student_submit_folder):
                    shutil.copy(student_submit_folder + "/" + s_file, student_grade_folder)
