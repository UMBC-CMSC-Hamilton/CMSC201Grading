import os
from pathlib import Path

COMMENT_KEY = "%%%"
SECTION_KEY = "###"
GRADER_COMMENT_KEY = "***"

def compile_rubric(rubric_path):
    if(os.path.exists(rubric_path + "/compiled_rubric.txt")):
       os.remove(rubric_path + "/compiled_rubric.txt")
    compiled_rubric = open(rubric_path + "/compiled_rubric.txt", "x")
    
    try:
        base_rubric = open(rubric_path + "/rubric.txt", "r")
    except FileNotFoundError:
        print("Student does not have a rubric! File does not exist: ", rubric_path + "/rubric.txt")
        os.remove(rubric_path + "/compiled_rubric.txt")
        return ["ERROR", -1]
    
    base_list = base_rubric.readlines()
    in_rubric_section = False
    section_score = 0.0
    section_total = 0.0

    student_score_list = []
    section_name_list = []

    student_folder_list = rubric_path.split("/")
    student_nameID = student_folder_list[len(student_folder_list) - 1]
    assignment_line = base_list[0].split(" ")
    assignment_ID = assignment_line[len(assignment_line) - 1].strip()
    print("Compiling " + assignment_ID + " rubric for " + student_nameID + "... ", end="")
    total_student_score = 0.0
    max_line = base_list[1]
    max_score_object = max_line.split(":")[1].split(" ")
    total_possible_score = float(max_score_object[1])

    rubric_length = len(base_list)

    last_chars_finder = len(base_list) - 1
    continue_searching = True
    while(continue_searching):
        currLine = base_list[last_chars_finder]
        if(currLine.strip() == ""):
            last_chars_finder -= 1
        else:
            if(currLine[0:3] == GRADER_COMMENT_KEY and currLine.strip().endswith(GRADER_COMMENT_KEY)):
                continue_searching = False
            else:
                print("ERROR")
                print("Grader comments must go *inside* the two rows of asterisks! The last line must be a row of asterisks.")
                print("The following line is not valid:")
                print(currLine + "\n")
                os.remove(rubric_path + "/compiled_rubric.txt")
                return ["ERROR", -1]
    
    for index in range(len(base_list)):
        line = base_list[index]
        if(line[0:3] != COMMENT_KEY):
            
            #Inside a rubric section, all lines must start with a grade.
            if(line[0:3] == SECTION_KEY and in_rubric_section == True):
                if(not line.strip().endswith(SECTION_KEY)):
                    print("ERROR")
                    print("The following line is not a valid section key line! (It does not start/end with ###)")
                    print(line)
                    os.remove(rubric_path + "/compiled_rubric.txt")
                    return ["ERROR", -1]
                in_rubric_section = False
                total_student_score += section_score
                section_score_line = "Section Score: {}/{}".format(section_score, section_total)
                student_score_list.append(section_score)
                if(section_total == 0 and section_score == 0):
                    compiled_rubric.write("Congratulations! You followed the overall guidelines!\n")
                if(section_total == 0 and section_score > 0):
                    print("ERROR")
                    print("The point total for overall guidelines is greater than 0.. this shouldn't happen!\n")
                    os.remove(rubric_path + "/compiled_rubric.txt")
                    return ["ERROR", -1]
                compiled_rubric.write(line)
                compiled_rubric.write(section_score_line + "\n")
                section_score = 0.0
                section_total = 0.0
            elif(line[0:3] == SECTION_KEY and in_rubric_section == False):
                if(not line.strip().endswith(SECTION_KEY)):
                    print("ERROR")
                    print("The following line is not a valid section key line! (It does not start/end with ###)")
                    print(line)
                    os.remove(rubric_path + "/compiled_rubric.txt")
                    return ["ERROR", -1]
                point_line = base_list[index-1].split("(")
                if(get_section_names == True):
                    section_name_list.append(point_line[0].strip())
                section_total = float(point_line[len(point_line) - 1].split(" ")[0]) # Extracts section max score
                in_rubric_section = True
                compiled_rubric.write(line)
            else:
                if(in_rubric_section):
                    if(line.isspace() == False):
                        
                        grade_object = line.split(" ")[0]
                        try:
                            line_object = grade_object.split("/")
                            line_item_grade = float(line_object[0])
                            line_item_total = float(line_object[1])
                            if(line_item_grade > line_item_total):
                                print("ERROR")
                                print("You gave the following line item more than the maximum points allowed!")
                                print(line)
                                os.remove(rubric_path + "/compiled_rubric.txt")
                                return ["ERROR", -1]
                            section_score += line_item_grade
                        except ValueError:
                            print("ERROR")
                            print("Uh oh! Clean up on line " + str(index) + "!")
                            print("There was an error when parsing the grade on this line:")
                            print(line)
                            os.remove(rubric_path + "/compiled_rubric.txt")
                            return ["ERROR", -1]
                if(line.isspace() and in_rubric_section == True):
                    pass
                else:
                    compiled_rubric.write(line)
                if index + 1 != rubric_length:

                    # If the TA doesn't leave the student any comments, it publicly shames them (or used to)
                    if(line[0:3] == GRADER_COMMENT_KEY and base_list[index+1][0:3] == GRADER_COMMENT_KEY):
                        compiled_rubric.write("No comments.\n")
                        
    if(total_student_score < 0):
        print("ERROR")
        print(student_nameID, "has a negative score!\n")
        os.remove(rubric_path + "/compiled_rubric.txt")
        return ["ERROR", -1]
    if(total_student_score > total_possible_score):
        print("ERROR")
        print(student_nameID, "has a score greater than the maximum possible score!\n")
        os.remove(rubric_path + "/compiled_rubric.txt")
        return ["ERROR", -1]
    compiled_rubric.write("\nTOTAL SCORE: {}/{}\n\n".format(total_student_score, total_possible_score))
    compiled_rubric.write("Grades should appear in Blackboard shortly.\n\n")
    compiled_rubric.write("Please reply to this email if you have any questions about your grade.\n")
    compiled_rubric.close()
    
    if(get_section_names == True):
        section_name_list.append("TOTAL")
        
    student_score_list.append(total_student_score)
    print("{}/{}".format(total_student_score, total_possible_score))
    return section_name_list, student_score_list


# Will be called for each student in the TA's grading directory
base_ta_folder = str(Path(os.getcwd()).parents[0])
overall_success = True
get_section_names = True
sectioning_csv_path = base_ta_folder + "/" + "sectioning.csv"

if(os.path.exists(sectioning_csv_path)):
    os.remove(sectioning_csv_path)

sectioning_csv = open(sectioning_csv_path, "a")
for student_grade_folder in os.scandir(base_ta_folder):
    if(os.path.isdir(student_grade_folder.path)):
        names, result = compile_rubric(student_grade_folder.path)
        if(get_section_names == True):
            sectioning_csv.write(",".join(names) + "\n")
            get_section_names = False
        if result == -1:
            overall_success = False
        else:
            temp_result = []
            for res in result:
                temp_result.append(str(res))
            sectioning_csv.write(",".join(temp_result) + "\n")
sectioning_csv.close()
if(overall_success == False):
    print("You are not finished grading this assignment. Get back to work.")
    os.remove(sectioning_csv_path)
    face_palm_list = \
    ["............................................________", \
     "....................................,.-'\"...................``~.,", \
     ".............................,.-\"...................................\"-.,", \
     ".........................,/...............................................\":,", \
     ".....................,?......................................................,", \
     ".................../...........................................................,}", \
     "................./......................................................,:`^`..}", \
     ".............../...................................................,:\"........./", \
     "..............?.....__.........................................:`.........../", \
     "............./__.(.....\"~-,_..............................,:`........../", \
     ".........../(_....\"~,_........\"~,_....................,:`........_/", \
     "..........{.._$;_......\"=,_.......\"-,_.......,.-~-,},.~\";/....}", \
     "...........((.....*~_.......\"=-._......\";,,./`..../\"............../", \
     "...,,,___.`~,......\"~.,....................`.....}............../", \
     "............(....`=-,,.......`........................(......;_,,-\"", \
     "............/.`~,......`-...................................../", \
     ".............`~.*-,.....................................|,./.....,__", \
     ",,_..........}.>-._...................................|..............`=~-,", \
     ".....`=~-,__......`,.................................", \
     "...................`=~-,,.,...............................", \
     "................................`:,,...........................`..............__", \
     ".....................................`=-,...................,%`>--==``", \
     "........................................_..........._,-%.......`", \
     "...................................,"]
    for line in face_palm_list:
        print(line)
else:
    print("Congratulations! You are finished! Please mark yourself off as 'DONE' on the grading spreadsheet! <3")
    thumbs_up_list = \
        ["░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░", \
        "░░░░░░░▄▄▀▀▀▀▀▀▀▀▀▀▄▄█▄░░░░▄░░░░█░░░░░░░", \
        "░░░░░░█▀░░░░░░░░░░░░░▀▀█▄░░░▀░░░░░░░░░▄░", \
        "░░░░▄▀░░░░░░░░░░░░░░░░░▀██░░░▄▀▀▀▄▄░░▀░░", \
        "░░▄█▀▄█▀▀▀▀▄░░░░░░▄▀▀█▄░▀█▄░░█▄░░░▀█░░░░", \
        "░▄█░▄▀░░▄▄▄░█░░░▄▀▄█▄░▀█░░█▄░░▀█░░░░█░░░", \
        "▄█░░█░░░▀▀▀░█░░▄█░▀▀▀░░█░░░█▄░░█░░░░█░░░", \
        "██░░░▀▄░░░▄█▀░░░▀▄▄▄▄▄█▀░░░▀█░░█▄░░░█░░░", \
        "██░░░░░▀▀▀░░░░░░░░░░░░░░░░░░█░▄█░░░░█░░░", \
        "██░░░░░░░░░░░░░░░░░░░░░█░░░░██▀░░░░█▄░░░", \
        "██░░░░░░░░░░░░░░░░░░░░░█░░░░█░░░░░░░▀▀█▄", \
        "██░░░░░░░░░░░░░░░░░░░░█░░░░░█░░░░░░░▄▄██", \
        "░██░░░░░░░░░░░░░░░░░░▄▀░░░░░█░░░░░░░▀▀█▄", \
        "░▀█░░░░░░█░░░░░░░░░▄█▀░░░░░░█░░░░░░░▄▄██", \
        "░▄██▄░░░░░▀▀▀▄▄▄▄▀▀░░░░░░░░░█░░░░░░░▀▀█▄", \
        "░░▀▀▀▀░░░░░░░░░░░░░░░░░░░░░░█▄▄▄▄▄▄▄▄▄██", \
        "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"]
    for line in thumbs_up_list:
        print(line)
