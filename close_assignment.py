import os
import csv
import sys
import json
from datetime import datetime
from base_dir import __BASE_SUBMIT_DIR

def close_assignment(assignment, roster_file_name, extensions):
    with open(roster_file_name) as roster_file:
        roster_reader = csv.reader(roster_file)
        for person, section in roster_reader:
            if person != 'eric8':
                if person not in extensions[assignment] and section not in extensions[assignment]:
                    the_path = os.path.join(__BASE_SUBMIT_DIR, assignment, person)
                    os.popen('fs sa {} {} read'.format(the_path, person))
                elif section in extensions[assignment]:
                    due_time = datetime.strptime(extensions[assignment][str(section)], '%Y.%m.%d.%H.%M.%S')
                    if due_time <= datetime.now():
                        os.popen('fs sa {} {} read'.format(the_path, person))
                elif person in extensions[assignment]:
                    due_time = datetime.strptime(extensions[assignment][person], '%Y.%m.%d.%H.%M.%S')
                    if due_time <= datetime.now():
                        os.popen('fs sa {} {} read'.format(the_path, person))
                    

if __name__ == '__main__':
    print('Expected: close_assignment.py assignment roster_file_name extensions.json')
    extensions = {}
    try:
        extensions_file = open(sys.argv[3])
        extensions = json.loads(extensions_file.read())
    except OSError:
        print('No extensions file found. ')
        
    close_assignment(sys.argv[1], sys.argv[2], extensions)
