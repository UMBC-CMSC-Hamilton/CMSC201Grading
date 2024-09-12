import os
import csv
import sys
import subprocess
from base_dir import __BASE_SUBMIT_DIR

PUB_SUBMIT_RC_FILE = '.pubsubmitrc'
__BASE_PUB_DIR = '/afs/umbc.edu/users/e/r/eric8/pub/'
course_admin = 'eric8'


def make_directory(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        print('Directory {} already exists'.format(path))

        
def verify_student(student, assignment):
    path = os.path.join(__BASE_SUBMIT_DIR, assignment, student)
    p = subprocess.Popen(['fs', 'la', path], stdout=subprocess.PIPE)
    out, err = p.communicate()
    out_lines = out.decode('utf-8').split('\n')

    found_student = False
    for line in out_lines:

        split_lines = line.split()
        if len(split_lines) == 2:
            name, permissions = split_lines

            if name == student:
                found_student = True
                if 'w' not in permissions:
                    return False

    if not found_student:
        return False

    return True

        
def create_assignment(roster_file_name, assignment, overwrite=False):
    log_file = open(f'create_{assignment}.log', 'w')
    
    with open(roster_file_name) as roster_file:
        roster_reader = csv.reader(roster_file)
        assignment_path = os.path.join(__BASE_SUBMIT_DIR, assignment)
        make_directory(assignment_path)
        
        for person, section in roster_reader:
            the_path = os.path.join(__BASE_SUBMIT_DIR, assignment, person)
            make_directory(the_path)
            if person != course_admin:
                attempts = 0
                os.popen(f'fs sa {the_path} {course_admin}:submit_cmsc201 none')
                os.popen(f'fs sa {the_path} eric8:cmsc201staff write')
                # remove anyuser rl privileges
                os.popen(f'fs sa {the_path} system:anyuser none')
                os.popen(f'fs sa {the_path} {person} write')
                # a common issue is that the the permissions are not actually granted, ensure that they are
                # even with this permission are still not always set... 
                if verify_student(person, assignment):
                    log_file.write(f"{the_path} {person} created with correct permissions")
                else:
                    log_file.write(f"{the_path} {person} not correctly created")
                    
                while not verify_student(person, assignment) and attempts < 10:
                    attempts += 1
                    os.popen(f'fs sa {the_path} {person} write')
                
            else:
                os.popen(f'fs sa {the_path} {course_admin}:submit_cmsc201 none')
        os.popen(f'fs sa {assignment_path} system:anyuser rl')
    log_file.close()

def update_pub_submitrc(assignment_name, due_date):
    if due_date != 'no-update':
        try:
            with open(os.path.join(__BASE_PUB_DIR, PUB_SUBMIT_RC_FILE), 'a') as pub_sumbmit_rc:
                pub_sumbmit_rc.write('PROJECT ' + assignment_name + '\n')
                pub_sumbmit_rc.write('ENDDATE ' + due_date + '\n')
        except OSError:
            print('Unable to update .pubsubmitrc')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 create_assignment.py [Assignment Name] [Roster File] [Due Date MM/DD/YYYY format]")
    else:
        create_assignment(sys.argv[2], sys.argv[1])
        if len(sys.argv) == 4:
            update_pub_submitrc(sys.argv[1], sys.argv[3])
