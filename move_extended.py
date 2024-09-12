"""
File: move_extended.py
Author: Nicholas Marthinuss <nmarthi1@umbc.edu>
Date: 10/4/2021
Description: This program copies files from the
             submission directory to the Grading
             directory once an extension ends.
             This program is intended to be dispatched
             by the 201 bot.
"""
import os
import sys
import shutil
from base_dir import __BASE_SUBMIT_DIR

GRADING_DIR = "Grading"

# False -- no output
# True -- prints each copied file for username
LOGGING = False

if __name__ == "__main__":
    if len(sys.argv) == 4:

        student_username = sys.argv[1]
        TA_username = sys.argv[2]
        assignment_name = sys.argv[3].upper()

        # student path is BASE, assignment, student_username
        student_folder = os.path.join(
            __BASE_SUBMIT_DIR, assignment_name, student_username)

        # grading path is BASE, Grading, assignment, TA_username, student_username
        grading_folder = os.path.join(
            __BASE_SUBMIT_DIR, GRADING_DIR, assignment_name, TA_username, student_username)

        # note: copy all files, not just .py files because students will do things
        # like submit emacs recovery files, emacs autosaves, and sometimes even
        # without any file extension at all

        # walk the submit directory and get each file
        # os.walk on a non-existant directory just gives an empty list
        files = [f for _, _, f in os.walk(student_folder)]
        try:
            # we want the list inside of the one we made
            files = files[0]
        except IndexError as e:
            # if we have an IndexError, there were no files found
            print(e)
            print(f"Empty folder for: {student_username}")

        # print(f"{files = }")

        # copy each file from submit directory
        for f in files:
            try:
                shutil.copyfile(os.path.join(student_folder, f),
                                os.path.join(grading_folder, f))
                if LOGGING:
                    print(f"Copied {f} for {student_username}")
            except OSError as e:
                # OSError if the dest is not writeable or if file is character device/pipe
                # if a student has a character device in their submit folder
                # then I would have some questions
                print(e)
                print(f"Error. Skipping {f} for {student_username}")
            except shutil.SameFileError as e:
                # we should never end up copying the same file
                # since the paths are different but just in case
                print(e)
                print(
                    f"Error. Skipping copy of src to itself for file {f} with user {student_username}")
    else:
        print(
            "Usage: python3 move_extended.py <student_username> <TA_username> <assignment>")
