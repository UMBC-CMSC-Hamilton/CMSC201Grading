#!/bin/python3
import sys
import os
import subprocess
import csv
from base_dir import __BASE_SUBMIT_DIR


# def modify_student(student, assignment, r_w='read'):
def verify_student(student, assignment, r_w='read'):
    path = os.path.join(__BASE_SUBMIT_DIR, assignment, student)
    p = subprocess.Popen(['fs', 'la', path], stdout=subprocess.PIPE)
    out, err = p.communicate()
    out_lines = out.decode('utf-8').split('\n')

    found_student = False
    for line in out_lines:

        split_lines = line.split()
        if len(split_lines) == 2:
            name, permissions = split_lines
            if name == student and r_w == 'read':
                found_student = True
                if 'w' in permissions:
                    subprocess.Popen(['fs', 'sa', path, student, 'read'])
                    print('Changing {} permissions to read'.format(student))
            elif name == student and r_w == 'write':
                found_student = True
                if 'w' not in permissions:
                    subprocess.Popen(['fs', 'sa', path, student, 'write'])
                    print('Changing {} permissions to write'.format(student))

    if not found_student:
        print('Student permissions not found, giving student write access')
        print(student)
        subprocess.Popen(['fs', 'sa', path, student, 'write'])


def verify_assignment(roster_file_name, assignment, r_w='read'):
    with open(roster_file_name) as roster_file:
        roster_reader = csv.reader(roster_file)
        for person, section in roster_reader:
            print('Verifying {} from section {}'.format(person, section))
            verify_student(person, assignment, r_w)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: verify_permissions.py submit_roster assignment read/or/write")
    else:
        verify_assignment(sys.argv[1], sys.argv[2], sys.argv[3])
