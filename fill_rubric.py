#!/usr/bin/python3

import sys
import os

SECTION_KEY = "###"
COMMENT_KEY = "%%%"

ID_NAME_MAP = {}

SECTION_LINE_INDICES = []

rubricPath = os.getcwd() + "/rubric.txt"

rubricFile = open(rubricPath, "r")
rubricLines = rubricFile.readlines()
rubricFile.close()

def fill_rubric_section(section_number, fillwith):
    filledSomething = False
    currLineIndex = SECTION_LINE_INDICES[section_number] + 1
    currLine = rubricLines[currLineIndex]
    while currLine[0:3] != SECTION_KEY:
        if currLine[0:3] != COMMENT_KEY:
            old_line = currLine
            if fillwith == "fill":
                grade_object = currLine.split(" ")[0].strip()
                max_grade = int(grade_object.split("/")[1])
                rubricLines[currLineIndex] = currLine.replace("&", str(max_grade), 1)
            else:
                rubricLines[currLineIndex] = currLine.replace("&", str(0), 1)
            new_line = rubricLines[currLineIndex]
            if(old_line != new_line):
                filledSomething = True
        currLineIndex += 1
        currLine = rubricLines[currLineIndex]
    if(filledSomething == True):
        if(fillwith == "fill"):
            print("Filling '" + ID_NAME_MAP[section_number] + "' with maximum points!")
        else:
            print("Filling '" + ID_NAME_MAP[section_number] + "' with zeros!")
    else:
        print(ID_NAME_MAP[section_number], "was already filled!")
if((len(sys.argv) <= 1) or (len(sys.argv) >= 4)):
    print("Wrong number of arguments!")
    print("Usage: make <fill | zero> [section #]")
    exit()

if(sys.argv[1] != "fill" and sys.argv[1] != "zero"):
    print("Argument 1 must be either 'fill' or 'zero'! Are you using the makefile?")
    exit()
    
num_sections = 0
in_section = False
is_attendance_rubric = False
attendance_section_id = -1
for index in range(len(rubricLines)):
    line = rubricLines[index]
    if line[0:3] == SECTION_KEY and in_section == False:
        section_name = rubricLines[index - 1].split("(")[0].strip()
        if(section_name.split(":")[1].strip() == "Attendance"):
            is_attendance_rubric = True
            attendance_section_id = num_sections
        ID_NAME_MAP[num_sections] = section_name
        num_sections += 1
        SECTION_LINE_INDICES.append(index)
        in_section = True
    elif line[0:3] == SECTION_KEY and in_section == True:
        in_section = False


if(len(sys.argv) == 2):
    #Fills everything except for overall guidelines
    for section in range(num_sections - 1):
        fill_rubric_section(section, sys.argv[1])
elif(len(sys.argv) == 3):
    if(sys.argv[2] == "attendance"):
        if is_attendance_rubric:
            fill_rubric_section(attendance_section_id, sys.argv[1])
        else:
            print("The current rubric does not have an attendance section!")
    else:
        #Try to cast it to a number that corresponds with the rubric section
        try:
            wanted_section = int(sys.argv[2])
            # Offset due to overall guidelines being manual
            if (wanted_section <= 0) or (wanted_section >= num_sections):
                print("Invalid section! Valid options are integers from 1 to {}!".format(num_sections - 1))
                exit()
            else:
                fill_rubric_section(wanted_section - 1, sys.argv[1])
        except ValueError:
            print("Cannot convert", sys.argv[2], "to an integer! Please try again!")
            exit()
rubricFile = open(rubricPath, "w")
rubricFile.writelines(rubricLines)
rubricFile.close()
