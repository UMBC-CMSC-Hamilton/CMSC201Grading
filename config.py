'''
File:    config.py
Author:  Kevin Chen <kchen6@umbc.edu>, Michael Neary <mneary1@umbc.edu>, Matt Manzi <mmanzi1@umbc.edu>
Date:    Updated:2022-09-05, 2019-01-07
Description:
File holding important repository-wide constants used by multiple scripts in
order to run properly and consistently. There are a few constants that need to
be reset as frequently as the beginning of each semester. They are identified
below.
NOTE: Directory names MUST have the trailing slash, or you will break things.

To use this configuration in your code, write your script in the same directory
as this file and use the following import statement to import everything:

    from config import *

You can also import specific values:

    from config import RUBRIC_DIR, GRADING_DIR

'''

###########################################################

import csv
from base_dir import __BASE_SUBMIT_DIR

# submit system course name
# ex: "cs201" or "cmsc201"
COURSE_NAME = "cmsc201"

# base 201 directory for the person that manages the system
# ex: "/afs/umbc.edu/users/m/m/mmanzi1/home/201_TA/fa18/"
BASE_DIR = __BASE_SUBMIT_DIR
# base directory to which students will submit their assignments
# should be set to __BASE_SUBMIT_DIR
SUBMIT_DIR = __BASE_SUBMIT_DIR


'''
This function loads the ta-roster from a file called "admin_roster.csv"

The format should be each line has a [ username like eric8, ta name like Eric Hamilton, sections separated by commas eg 41, 42 or just 53 ]
'''
def load_ta_roster(filename = 'admin_roster.csv'):
    ta_dict = {}
    ta_name_id = {}
    with open(filename) as ta_roster_file:
        ta_reader = csv.reader(ta_roster_file)
        for line in ta_reader:
            ta_dict[line[0]] = [int(x) for x in line[2].split(',')]
            ta_name_id[line[0]] = line[1]
            
    return ta_dict, ta_name_id

TA_DICT, TA_NAME_ID_DICT = load_ta_roster()

# dictionary of instructors and their lecture section(s)
# ex: {"benj1":[1,9], "k38":[15]}
"""
This must still be filled in manually.

TODO: make this automatic.  
"""
PROF_DICT = {"eric8": [11, 12, 13, 14, 15, 16, 42, 43, 44, 45, 46],
             "samit1": [21, 22, 23, 24, 25, 26, 27],
             "sdonahue": [31, 32, 33, 34, 35, 36, 51, 52, 53, 54, 55, 56, 58, 71, 72, 73, 74],
             "arsenaul": [61, 62]
             }

# dictionary of course assignments and due dates
# NOTE: dates here *must* have the format of: MM/DD/YYYY
# NOTE: a 'False' assignment will be commented out in the .submitrc file
# ex: {"HW1":("09/04/2018",True), "HW2":("09/11/2018",False)}
ASSIGNMENTS = {}

# UMBC (GL) account username of the person managing the submit system
# ex: "mmanzi1"
SUBMIT_MNGR = "eric8"

# list of usernames of students who have dropped the course, add students here
# instead of going through the hassle of removing them from submit
# ex: ["mmanzi1"]
DROPPED_STUDENTS = []

###########################################################
'''
These constants do not need to be updated.
'''

# directory where rubrics and zeroed rubrics will be stored for distribution
RUBRIC_DIR = BASE_DIR + "admin/grading_scripts/rubrics/"

# directory where makefiles and I/O directories will be stored for distribution
MAKEFILE_DIR = BASE_DIR + "admin/grading_scripts/makefiles/"

# directory where exported grade files will be saved
GRADES_DIR = BASE_DIR + "grades/"

# full path to course roster, comma-separated list of students and sections
# the course roster cannot have a header row and each entry must be formatted
# like: <username>,<discussion_section> (ex: mmanzi1,2)
# Received FileNotFoundError: [Errno 2] No such file or directory: '/afs/umbc.edu/users/e/r/eric8/pub/cmsc201/fall23/submit_roster.csv'
# ROSTER = BASE_DIR + "submit_roster.csv"
ROSTER = BASE_DIR + "admin/submit_roster.csv"
# AFS group that owns the submit system
STAFF_GROUP = SUBMIT_MNGR + ":" + COURSE_NAME + "staff"

# email address from which student rubrics are sent
SENDER_EMAIL = f"{SUBMIT_MNGR}@umbc.edu"
# ###SENDER_EMAIL = "cs201reflector@gmail.com"

# bas####e directory for TAs to grade assignments in
GRADING_DIR = SUBMIT_DIR + "Grading/"

# base directory for testing scripts and other misc. things
TEST_DIR = SUBMIT_DIR + "Test/"

# configuration values for script logging
LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(filename)s(%(lineno)d): %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler"
        },
        "file": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": BASE_DIR + "201-scripts.log"
        }
    },
    "loggers": {
        "": {
            "handlers": ["file", "console"],
            "level": "DEBUG"
        }
    }
}
