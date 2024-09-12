import os
import csv
import sys
import re
import logging
import datetime
from base_dir import __BASE_SUBMIT_DIR


log_path = os.path.join(__BASE_SUBMIT_DIR, 'admin', 'events.log')
logging.basicConfig(filename=log_path, filemode='a', format='%(asctime)s:%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def close_section_extension(assignment, roster_file_name, target_section):
    print(f'Closing section {target_section} extension for {assignment}')
    logging.info(f'Closing section {target_section} extension for {assignment}')
    roster_file_path = os.path.join(__BASE_SUBMIT_DIR, 'admin', roster_file_name)

    with open(roster_file_path) as roster_file:
        roster_reader = csv.reader(roster_file)
        for person, section in roster_reader:
            if person != 'eric8':
                if target_section == section:
                    the_path = os.path.join(__BASE_SUBMIT_DIR, assignment, person)
                    print(the_path)
                    os.popen('fs sa {} {} read'.format(the_path, person))


def close_student_extension(assignment, student):
    print(f'Closing {assignment} extension for {student}')
    logging.info(f'Closing {assignment} extension for {student}')
    if student != 'eric8':
        the_path = os.path.join(__BASE_SUBMIT_DIR, assignment, student)
        os.popen('fs sa {} {} read'.format(the_path, student))


if __name__ == '__main__':
    the_match = re.match(r'(?P<assignment>\w+)\s+((student\s*=\s*(?P<student>\w+))|(section\s*=\s*(?P<section>\d+)\s+(?P<roster>.*)))', ' '.join(sys.argv[1:]))
    logging.info(' '.join(sys.argv[1:]))
    print(' '.join(sys.argv[1:]))
    print(__name__)
    if the_match:
        if the_match.group('student'):
            close_student_extension(the_match.group('assignment'), the_match.group('student'))
        else:
            close_section_extension(the_match.group('assignment'), the_match.group('roster'), the_match.group('section'))

