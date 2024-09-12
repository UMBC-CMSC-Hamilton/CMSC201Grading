#!/usr/bin/python3

import os
import sys
import copy
import statistics as stats
import smtplib
import csv
from email.mime.text import MIMEText
from socket import gethostname
from config import DROPPED_STUDENTS, TA_NAME_ID_DICT, GRADING_DIR, GRADES_DIR

# MAJORS INSTRUCTORS
INSTRUCTORS = [ "jturner3", "eric8",  "abalasu1", "samit1"]
# NONMAJORS INSTRUCTORS
CSEE_SERVERS = ["linuxserver1.cs.umbc.edu", "linuxserver2.cs.umbc.edu"]
total_dict = {}
section_dict = {}
title_list = []
if gethostname() not in CSEE_SERVERS:
    print("WHAT ARE YOU DOING IN MY SWAMP! This script must be run from a CSEE Department Server, not GL!")
    exit()

SMTP_SERVER = smtplib.SMTP("localhost")  # Fails if not on CSEE Department Server

def set_up_instructors():
    try:
        sectioning_file = open(GRADES_DIR + "/" + sys.argv[1] + "/" + sys.argv[1] + "_sectioning.csv")
        sectioning_lines = sectioning_file.readlines()
        sectioning_file.close()
    except IOError:
        print("There is no 'sectioning.csv' file in the grades directory! You need this!")
        exit()

    total_dict["num_students"] = len(sectioning_lines[1:])
        
    for part in sectioning_lines[0].split(","):
        title_list.append(part.strip())

    for index in range(len(title_list)):
        total_dict[title_list[index]] = {}
        part_score_list = []
        for row in sectioning_lines[1:]:
            part_score_list.append(float(row.split(",")[index]))
        total_dict[title_list[index]]["mean"] = stats.mean(part_score_list)
        total_dict[title_list[index]]["median"] = stats.median(part_score_list)
        total_dict[title_list[index]]["stdev"] = stats.stdev(part_score_list)

    
def send_instructor_emails(debug=False):
    for instructor in INSTRUCTORS:
        instructor_email = []
        instructor_email.append("Greetings, oh great and powerful course instructor for CMSC 201!\n")
        instructor_email.append("\n")
        instructor_email.append("The grades for " + sys.argv[1] + " have been processed and have been released to students!\n")
        instructor_email.append("Below, you will find statistics for specific problems as well as the total assignment.\n")
        instructor_email.append("\n")
    
        for part_index in range(len(title_list)):
            instructor_email.append(title_list[part_index] + "\n")
            instructor_email.append("\tAverage: " + str(total_dict[title_list[part_index]]["mean"]) + "\n")
            instructor_email.append("\tMedian: " + str(total_dict[title_list[part_index]]["median"]) + "\n")
            instructor_email.append("\tStandard Deviation: " + str(total_dict[title_list[part_index]]["stdev"]) + "\n")
            instructor_email.append("\n")

        instructor_email.append("\n")
        instructor_email.append("Thank you for putting your time and effort into making this course what it is right now!\n")
        instructor_email.append("\n")
        instructor_email.append("Copyright 2020 -- Sean C. Jordan Industries Incorporated.\n")
        instructor_email.append("All rights reserved.\n\n")

        final_instructor = MIMEText(''.join(instructor_email))
        final_instructor["subject"] = "CMSC 201 - Assignment Statistics - " + sys.argv[1]
        final_instructor["from"] = "Kevin Chen <kchen6@umbc.edu>"
        final_instructor["to"] = TA_NAME_ID_DICT[instructor] + " <{}@umbc.edu>".format(instructor)
        instructor_email_address = instructor + "@umbc.edu"
        sender = "kchen6@umbc.edu"
        try:
            if not debug:
                SMTP_SERVER.sendmail(sender, [instructor_email_address], final_instructor.as_string())
            else:
                print(f'Debug: Email from {sender} to {instructor_email_address} sent. ')
                
            print(final_instructor)
            print("Assignment statistics email successfully sent to", instructor_email_address)
        except Exception as ex:
            print("ERROR: Assignment Statistics email sending failed for", instructor_email_address)
            print("Exception:", ex)

            
def set_up_tas():
    for grading_folder in os.scandir(BASE_GRADING_DIR):
        ta_folder = grading_folder.path
        ta_name = ta_folder.split("/")[len(ta_folder.split("/")) - 1]
        if(ta_name != "IO_files" and ta_name != "grading_scripts" and ta_name != sys.argv[1] + "_IO"):
            section_score_list = []
            section_dict[ta_name] = {}
            sectioning_path = ta_folder + "/" + "sectioning.csv"
            try:
                sectioning_file = open(sectioning_path, "r")
                sectioning_lines = sectioning_file.readlines()
                sectioning_file.close()
                total_index = len(sectioning_lines[0].split(",")) - 1
                section_dict[ta_name]["num_students"] = len(sectioning_lines[1:])
                for row in sectioning_lines[1:]:
                    try:
                        section_score_list.append(float(row.split(",")[total_index]))
                    except IndexError:
                        print(ta_name, row)
            except IOError:
                print(ta_name, "does not have a 'sectioning.csv' file! This is not gucci gang!!")
                section_score_list.append(0.0)
                section_score_list.append(0.0)
            section_dict[ta_name]["mean"] = stats.mean(section_score_list)
            section_dict[ta_name]["median"] = stats.median(section_score_list)
            section_dict[ta_name]["stdev"] = stats.stdev(section_score_list)


def send_ta_emails(debug=False):
    for ta in section_dict:
        ta_email = []
        ta_email.append("Well how do you do, fellow Teaching Assistant?\n")
        ta_email.append("\n")
        ta_email.append("The grades for " + sys.argv[1] + " have been released to students.\n")
        ta_email.append("(You may receive emails from your students about their grades now)\n")
        ta_email.append("\n")
        ta_email.append("Here are the statistics for your section:\n")
        ta_email.append("\n")
        ta_email.append("Teaching Assistant: " + TA_NAME_ID_DICT[ta] + " ({})".format(ta) + "\n")
        ta_email.append("Assignment: " + sys.argv[1] + "\n")
        ta_email.append("Maximum Points Possible: " + str(total_dict["max_total"]) + "\n")
        ta_email.append("\n")
        ta_email.append("Number of students graded: " + str(section_dict[ta]["num_students"]) + "\n")
        ta_email.append("Section Average: " + str(section_dict[ta]["mean"]) + "\n")
        ta_email.append("Section Median: " + str(section_dict[ta]["median"]) + "\n")
        ta_email.append("Section Standard Deviation: " + str(section_dict[ta]["stdev"]) + "\n")
        ta_email.append("\n")
        ta_email.append("Class Count: " + str(total_dict["num_students"]) + "\n")
        ta_email.append("Class Average: " + str(total_dict["TOTAL"]["mean"]) + "\n")
        ta_email.append("Class Median: " + str(total_dict["TOTAL"]["median"]) + "\n")
        ta_email.append("Class Standard Deviation: " + str(total_dict["TOTAL"]["stdev"]) + "\n")
        ta_email.append("\n\n")
        ta_email.append("The CMSC 201 Empire thanks you for being a faithful servant to the cause.\n")
        ta_email.append("\n")
        ta_email.append("Copyright 2020 -- Sean C. Jordan Industries Incorporated.\n")
        ta_email.append("All rights reserved.\n\n")

        final_ta = MIMEText(''.join(ta_email))
        final_ta["subject"] = "CMSC 201 - Section Statistics - " + sys.argv[1]
        final_ta["from"] = "Kevin Chen <kchen6@umbc.edu>"
        final_ta["to"] = TA_NAME_ID_DICT[ta] + " <{}@umbc.edu>".format(ta)
        ta_email_address = ta + "@umbc.edu"

        sender = "kchen6@umbc.edu"
        try:
            if not debug:
                SMTP_SERVER.sendmail(sender, [ta_email_address], final_ta.as_string())
            else:
                print(f'Debug: Email from {sender} to {ta_email_address} sent.')
            # print(final_ta)
            print("Section statistics email successfully sent to", ta_email_address)
        except Exception as ex:
            print("ERROR: Section Statistics email sending failed for", ta_email_address)
            print("Exception:", ex)

def send_student_emails(debug=False):
    student_nameIdDict = {}
    with open('student_nameID_Dict.csv') as nameIdList:
        readList = csv.reader(nameIdList)
        student_nameIdDict = dict(readList)
    
    for grading_folder in os.scandir(BASE_GRADING_DIR):
        ta_folder = grading_folder.path
        ta_name = ta_folder.split("/")[len(ta_folder.split("/")) - 1]
        if(ta_name != "IO_files" and ta_name != "grading_scripts" and ta_name != sys.argv[1] + "_IO"):
            ta_email_address = ta_name + "@umbc.edu"
            for grade_folder in os.scandir(ta_folder):
                student_folder = grade_folder.path
                if(os.path.isdir(student_folder)):
                    student_name = student_folder.split("/")[len(student_folder.split("/")) - 1]
                    if(student_name not in DROPPED_STUDENTS):
                        comp_rubric_path = student_folder + "/" + "compiled_rubric.txt"
                        comp_rubric = open(comp_rubric_path, "r") # If a student doesn't have a compiled rubric.. uh oh
                        rubric_lines = comp_rubric.readlines()
                        if("max_total" not in total_dict.keys()):
                            total_line = rubric_lines[1]
                            point_object = total_line.split(":")[1].strip()
                            total_dict["max_total"] = float(point_object.split(" ")[0])

                        final_student = MIMEText(''.join(rubric_lines))
                        final_student["subject"] = "CMSC 201 - " + sys.argv[1] + " Grade"
                        final_student["from"] = TA_NAME_ID_DICT[ta_name] + " <{}@umbc.edu>".format(ta_name)
                        final_student["to"] = student_nameIdDict[student_name] + " <{}@umbc.edu>".format(student_name)
                        student_email = student_name + "@umbc.edu"
                        try:
                            if not debug:
                                SMTP_SERVER.sendmail(ta_email_address, [student_email], final_student.as_string())
                            else:
                                print(f'Debug: Email from {ta_email_address} to {student_email} sent.')
                            # print(final_student)
                            print("Rubric email successfully sent to", student_email)
                        except Exception as ex:
                            print("ERROR: Rubric email sending failed for", student_email)
                            print("Exception:", ex)
                    
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Wrong number of arguments! Usage: ./send_emails.py <assignment> [-debug]")
        exit()

    BASE_GRADING_DIR = GRADING_DIR + sys.argv[1]
    if not os.path.exists(BASE_GRADING_DIR):
        print("That assignment does not exist! Did you spell it correctly?")
        exit()

    debug = '-debug' in sys.argv

    send_student_emails(debug)
    set_up_instructors()
    set_up_tas()
    send_instructor_emails(debug)
    send_ta_emails(debug)

