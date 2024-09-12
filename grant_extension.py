import os
import csv
import sys
import json
from datetime import datetime
from base_dir import __BASE_SUBMIT_DIR



def grant_extensions(roster_file_name, extensions):
    section_dict = {}
    with open(roster_file_name) as roster_file:
        roster_reader = csv.reader(roster_file)
        for person, section in roster_reader:
            if section not in section_dict:
                section_dict[section] = []
            section_dict[section].append(person)

    for assignment in extensions:
        for section_num in extensions[assignment]['section-extensions']:
            for person in section_dict[section_num]:
                the_path = os.path.join(__BASE_SUBMIT_DIR, assignment, person)
                due_time = datetime.strptime(extensions[assignment]['section-extensions'][str(section_num)], '%Y.%m.%d.%H.%M.%S')
                if due_time > datetime.now():
                    os.popen('fs sa {} {} write'.format(the_path, person))
                    
        for student_id in extensions[assignment]['student-extensions']:
                the_path = os.path.join(__BASE_SUBMIT_DIR, assignment, student_id)
                due_time = datetime.strptime(extensions[assignment]['student-extensions'][student_id], '%Y.%m.%d.%H.%M.%S')
                if due_time > datetime.now():
                    os.popen('fs sa {} {} write'.format(the_path, student_id))
                    print(f'Granted extension to {student_id}') 


if __name__ == '__main__':
    extensions = {}
    try:
        extensions_file = open(sys.argv[2])
        file_data = extensions_file.read()
        print(file_data)
        extensions = json.loads(file_data)
    except OSError:
        print('No extensions file found. ')

    grant_extensions(sys.argv[1], extensions)
