import os
import sys
import subprocess
from base_dir import __BASE_SUBMIT_DIR


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


def extend_assignment(assignment_name):
    the_path = os.path.join(__BASE_SUBMIT_DIR, assignment_name)
    _, directories, _ = next(os.walk(os.path.join(the_path)))
    for the_directory in directories:
        the_student_path = os.path.join(the_path, the_directory)
        attempts = 0
        while not verify_student(the_directory, assignment_name) and attempts < 10:
            attempts += 1
            os.popen('fs sa {} {} write'.format(the_student_path, the_directory))
        print(the_directory, attempts)

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        print('Extending assignment', sys.argv[1])
        extend_assignment(sys.argv[1])
    else:
        print('format: python3 extend_assignment.py <assignment name>')
