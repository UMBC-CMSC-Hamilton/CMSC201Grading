import argparse
import csv
import os
import shutil

section_dict = {
    11: "mhakim1",
    12: "obaker1",
    13: "natolyb1",
    14: "sjordan2",
    15: "wlazer1",
    16: "npottei1",

    21: "nproulx1",
    22: "yothman1",
    23: "kchen6",
    24: "certel1",
    25: "cvantie1",
    26: "edove1",

    31: "pcode1",
    32: "b180",
    33: "aasfaw1",
    34: "reesd1",
    35: "alasbri1",
    36: "kg98416",

    41: "smammel1",
    42: "hc11773",
    43: "diyap1",
    44: "rg66173",
    45: "jslaught",
    46: "rappleb1",

    51: "mariahq1",
    52: "minc1",
    53: "bishalr1",
    54: "faithr1",
    56: "michalm1",
    55: "zj17690",

    61: "jmartin8",
    62: "tommyn3",
}

BASE_PATH = '/afs/umbc.edu/users/e/r/eric8/pub/cmsc201/fall20'
GRADING = 'Grading'
ALL_ASSIGNMENTS = ('HW0', 'HW1', 'HW2', 'HW3', 'LAB1', 'LAB2', 'LAB3')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('assignment', choices=['all', 'HW0', 'HW1', 'HW2', 'HW3', 'LAB1', 'LAB2', 'LAB3'])
    parser.add_argument('-find', action='store_true')
    parser.add_argument('-suppress', action='store_true')
    result = parser.parse_args()

    student_sections = {}
    with open('submit_roster.csv') as course_roster_file:
        reader = csv.reader(course_roster_file)
        for line in reader:
            try:
                student_sections[line[0]] = int(line[1])
            except ValueError:
                student_sections[line[0]] = 0

    search_path = os.path.join(BASE_PATH, result.assignment)
    if result.assignment == 'all':
        assignments = ALL_ASSIGNMENTS
    else:
        assignments = [result.assignment]

    for assignment in assignments:
        print('Scanning assignment {}'.format(assignment))
        for person in student_sections:
            persons_ta = section_dict.get(student_sections[person], None)
            if persons_ta:
                try:
                    files_source = os.listdir(os.path.join(BASE_PATH, assignment, person))
                    files_destination = os.listdir(os.path.join(BASE_PATH, GRADING, assignment, persons_ta, person))
                    if any(x not in files_destination for x in files_source):
                        print(person, files_source, files_destination)
                        for file_name in files_source:
                            if not os.path.exists(os.path.join(BASE_PATH, GRADING, assignment, persons_ta, person, file_name)):
                                shutil.copyfile(os.path.join(BASE_PATH, assignment, person, file_name),
                                                os.path.join(BASE_PATH, GRADING, assignment, persons_ta, person, file_name))
                                print(file_name, "copied to", os.path.join(BASE_PATH, assignment, person, file_name))
                            else:
                                y_n = input('Do you want to overwrite? File seems to exist! (yes/no)')
                                if y_n.lower() in ['yes', 'y']:
                                    print('Overwriting...')
                                    shutil.copyfile(os.path.join(BASE_PATH, assignment, person, file_name),
                                                    os.path.join(BASE_PATH, GRADING, assignment, persons_ta, person, file_name))
                                    print(file_name, "copied to", os.path.join(BASE_PATH, assignment, person, file_name))
                                else:
                                    print('Bypassing file')
                except OSError:
                    if not result.suppress:
                        print("No {} directory for {}".format(assignment, person))

            else:
                print(person, 'does not have a section, ignoring...')

    print(result)
