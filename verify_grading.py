#!/usr/bin/python3

import sys
import os
import subprocess as sp
from config import GRADING_DIR

if(len(sys.argv) != 2):
    raise ValueError("Wrong number of arguments! Usage: ./verify_grading.py <assignment>")
else:
    print("Running Grade Verification for assignment", sys.argv[1])
    grade_dir = GRADING_DIR + sys.argv[1]
    try:
        os.chdir(grade_dir)
        
    except OSError:
        print("Could not find that assignment directory.. did you spell it correctly?")
        exit()
    full_path = os.getcwd()
    not_done_tas = []
    for grading_folder in os.scandir(full_path):
        ta_folder = grading_folder.path
        ta_name = ta_folder.split("/")[len(ta_folder.split("/")) - 1]
        if(ta_name != "IO_files" and ta_name != "grading_scripts" and ta_name != sys.argv[1] + "_IO"):
            os.chdir(ta_folder)
            if(os.path.exists("sectioning.csv")):
                os.remove("sectioning.csv")
            first_student_dir = next(os.scandir(os.getcwd())).path
            os.chdir(first_student_dir)
            print("Checking", ta_name, "for completion...", end=" ")
            is_ta_done = sp.run(["make", "compile"], stdout=sp.PIPE).stdout.decode("utf-8")
            if("Get back to work." in is_ta_done):
                not_done_tas.append(ta_name)
                print("NOT COMPLETE")
            else:
                print("DONE")
    print()
    if(len(not_done_tas) == 0):
        print("All the TAs have finished grading {}! Go do grade processing!".format(sys.argv[1]))
    else:
        print("The following {} TAs have not finished grading:".format(len(not_done_tas)))
        for ta in not_done_tas:
            print(ta)
