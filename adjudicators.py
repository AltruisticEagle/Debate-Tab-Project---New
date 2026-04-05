import checks
import csv

def check_create_adjudicators(adjudicator_name, chair_status, trainee_status):
    matches1 = checks.checks(adjudicator_name, "name")
    matches2 = checks.checks(chair_status, "yes_no")
    matches3 = checks.checks(trainee_status, "yes_no")
    matches = [matches1, matches2, matches3]
    for i in matches:
        if i == None:
            raise ValueError
        
def check_modify_adjudicators(modify_parameter, modify_to):
    check = None
    if "adjudicator" in modify_parameter:
        check = "name"
    elif "status" in modify_parameter:
        check = "yes_no"
    matches = checks.checks(modify_to, check)
    if matches is None:
        raise Exception
    
def check_adjudicator_feedback(round_number, scorer_type, scorer_name, score):
    round_number = str(round_number)
    matches1 = checks.checks(round_number, "round")
    matches2 = checks.checks(scorer_type, "status_check") 
    matches3 = checks.checks(scorer_name, "name")
    matches4 = checks.checks(score, "adjudicator_feedback_score")
    matches = [matches1, matches2, matches3, matches4]
    for i in matches:
        if i == None:
            raise Exception

def check_adjudicator_already_exists(adjudicator_name):
    with open("adjudicators.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if adjudicator_name == row["adjudicator_name"]:
                raise ValueError("\nAdjudicator already exists, try again and input a new adjudicator")

def create_adjudicators(adjudicator_name, chair_status, trainee_status): 
    check_create_adjudicators(adjudicator_name, chair_status, trainee_status)
    check_adjudicator_already_exists(adjudicator_name)

    with open("adjudicators.csv", "a", newline="") as file:
        fieldnames = ["adjudicator_name", "chair_status", "trainee_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
    
        row = {"adjudicator_name": adjudicator_name, "chair_status": chair_status, "trainee_status": trainee_status}
        writer.writerow(row)

def modify_adjudicators(adjudicator_modify, modify_parameter, modify_to):
    check_modify_adjudicators(modify_parameter, modify_to)

    with open("adjudicators.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    with open("adjudicators.csv", "w", newline="") as file:
        fieldnames = ["adjudicator_name", "chair_status", "trainee_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        found = 0
        for row in rows:
            if row["adjudicator_name"] == adjudicator_modify:
                found = found + 1
                if modify_parameter == "adjudicator_name":
                    row["adjudicator_name"] = modify_to
                elif modify_parameter == "chair_status":
                    row["chair_status"] = modify_to
                elif modify_parameter == "trainee_status":
                    row["trainee_status"] = modify_to
            writer.writerow(row)
        
        if found == 0:
            raise ValueError(("\nThe adjudicator inputted for modification does not exist, please try again"))

def delete_adjudicators(adjudicator_modify):
    with open("adjudicators.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    with open("adjudicators.csv", "w", newline="") as file:
        fieldnames = ["adjudicator_name", "chair_status", "trainee_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if row["adjudicator_name"] == adjudicator_modify:
                continue
            writer.writerow(row)

#adjudicator feedback section
def create_adjudicator_feedback(adjudicator_name, round_number, scorer_type, scorer_name, score):
    check_adjudicator_feedback(round_number, scorer_type, scorer_name, score)

    with open("adjudicator_feedback.csv", "a", newline="") as file:
        fieldnames = ["adjudicator_name", "round", "scorer_type", "scorer_name", "score"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        row = {"adjudicator_name": adjudicator_name, "round": round_number, "scorer_type": scorer_type, "scorer_name": scorer_name, "score": score}
        writer.writerow(row)

def modify_adjudicator_feedback(adjudicator_feedback_modify, round_number, scorer_name, score):
    scorer_type = "adjudicator"
    check_adjudicator_feedback(round_number, scorer_type, scorer_name, score)

    with open("adjudicator_feedback.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    with open("adjudicator_feedback.csv", "w", newline="") as file:
        fieldnames = ["adjudicator_name","round","scorer_type","scorer_name","score"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if row["adjudicator_name"] == adjudicator_feedback_modify:
                if row["scorer_name"] == scorer_name:
                    if row["score"] == str(score):
                        if row["round"] == str(round_number):
                            continue

            writer.writerow(row)

def view_adjudicator_feedback(adjudicator_name):
    if checks.checks(adjudicator_name, "name") == None:
        raise ValueError("\nThis isn't a name, try again")
    
    with open("adjudicator_feedback.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

        table = []
        found = 0
        for row in rows:
            if row["adjudicator_name"].lower() == adjudicator_name.lower():
                found = found + 1
                table.append([row["round"], row["scorer_name"], row["scorer_type"], row["score"]])
            
        if found == 0:
            raise ValueError("The inputted adjudicator does not exist")
    
    return table