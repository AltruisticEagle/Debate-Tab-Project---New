import csv
import checks

def check_team(team_name): #checks for preexisting team names
    with open("teams.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if team_name == row["team_name"]:
                raise ValueError("\nThe team name is already taken or the team already exists, please try again")

def create_team_check(team_name, member_1, member_1_junior_status, member_2, member_2_junior_status):
    #these are all just checks for the parameters, they all work fine and the exception raises in UI
    matches1 = checks.checks(team_name, "team_name")
    matches2 = checks.checks(member_1, "name")
    matches3 = checks.checks(member_2, "name")
    matches4 = checks.checks(member_1_junior_status, "yes_no")
    matches5 = checks.checks(member_2_junior_status, "yes_no")
    matches = [matches1, matches2, matches3, matches4, matches5]
    for i in matches:
        if i == None:
            raise Exception
        
def modify_team_check(modify_parameter, modify_to):
    #checks, they also work fine, exceptions are raised the same way
    category = None
    if "member" in modify_parameter:
        category = "name"
    elif "team" in modify_parameter:
        category = "team_name"
    elif "junior_status" in modify_parameter:
        category = "yes_no"
    matches = checks.checks(modify_to, category)
    if matches is None:
        raise Exception

def create_teams(team_name, member_1, member_1_junior_status, member_2, member_2_junior_status):
    check_team(team_name)
    #appending a team, no need for a reader; this is to teams.csv
    with open("teams.csv", "a", newline="") as file:
        fieldnames = ["team_name", "member_1", "member_1_junior_status", "member_2", "member_2_junior_status", "junior_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if member_1_junior_status == "Y" and member_2_junior_status == "Y":
            junior_status = "Y"
        else:
            junior_status = "N"
        row = {
        "team_name": team_name, 
        "member_1": member_1, 
        "member_1_junior_status": member_1_junior_status,
        "member_2": member_2, 
        "member_2_junior_status": member_2_junior_status,
        "junior_status": junior_status}

        writer.writerow(row)

    #this appends the new team to team_standings.csv with no preexisting results
    with open("team_standings.csv", "a", newline="") as file:
        fieldnames = ["team", "points", "total_speaker_score", "junior_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        row = {"team": team_name, "points": 0, "total_speaker_score": 0, "junior_status": junior_status} 
        writer.writerow(row)

    #same as previous, but for the two debaters to the speaker_standings.csv file
    with open("speaker_standings.csv", "a", newline="") as file:
        fieldnames = ["speaker", "total_speaker_score", "junior_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        row1 = {"speaker": member_1, "total_speaker_score": 0, "junior_status": member_1_junior_status}
        row2 = {"speaker": member_2, "total_speaker_score": 0, "junior_status": member_2_junior_status}
        writer.writerows([row1, row2])

#1.2.1
def modify_teams(team_modify, modify_parameter, modify_to):
    if modify_parameter == "team_name": #this does the modification in the team standings specifically
        with open("team_standings.csv", "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        with open("team_standings.csv", "w", newline="") as file:
            fieldnames = ["team", "points", "total_speaker_score", "junior_status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                if row["team"] == team_modify: 
                    row["team"] = modify_to
                    #look at standings --> team name matches --> change name
                writer.writerow(row)
        
        #Modifying the draws
        with open("team_draws.csv", "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        with open("team_draws.csv", "w", newline="") as file:
            fieldnames = ["round","room","OG","OO","CG","CO"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                if row["OG"] == team_modify:
                    row["OG"] = modify_to
                elif row["OO"] == team_modify:
                    row["OO"] = modify_to
                elif row["CG"] == team_modify: 
                    row["CG"] = modify_to
                elif row["CO"] == team_modify:
                    row["CO"] = modify_to
                writer.writerow(row)
                

    if "member" in modify_parameter or "junior" in modify_parameter: 
        #this does modifications in the speaker standings specifically
        #speaker name and speaker junior status

        speaker = None
        #what we are doing here is looking in the teams.csv file for the speaker first
        #the one that we need to change the name/status thereof
        #This is because we don't have the name of the person we're changing from the UI
        #so ofc we need to find it first, then we can actually match and change it
        with open("teams.csv", "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            for row in rows:
                if row["team_name"] == team_modify:
                    if "member_1" in modify_parameter:
                        speaker = row["member_1"]
                    elif "member_2" in modify_parameter:
                        speaker = row["member_2"]

        if "junior" in modify_parameter:
            #this part does the junior status modification
            with open("speaker_standings.csv", "r") as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            with open("speaker_standings.csv", "w", newline="") as file:
                fieldnames = ["speaker", "total_speaker_score", "junior_status"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in rows:
                    if row["speaker"] == speaker:
                        row["junior_status"] = modify_to
                    writer.writerow(row)

        elif "member" in modify_parameter:
            #then we open up speaker standings to do the final modification
            with open("speaker_standings.csv", "r") as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            with open("speaker_standings.csv", "w", newline="") as file:
                fieldnames = ["speaker", "total_speaker_score", "junior_status"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in rows:
                    if row["speaker"] == speaker:
                        row["speaker"] = modify_to
                    writer.writerow(row)

    #This section modifies what we have to modify in the teams.csv file - completed, no need for fixes
    with open("teams.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    with open("teams.csv", "w", newline="") as file:
        fieldnames = ["team_name", "member_1", "member_1_junior_status", "member_2", "member_2_junior_status", "junior_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        found = 0
        #slightly archaic finding system but honestly it works, raise the same type of error also
        for row in rows:
            if row["team_name"] == team_modify:
                found = found + 1
                if modify_parameter == "team_name":
                    row["team_name"] = modify_to
                elif modify_parameter == "member_1":
                    row["member_1"] = modify_to
                elif modify_parameter == "member_2":
                    row["member_2"] = modify_to
                elif modify_parameter == "member_1_junior_status":
                    row["member_1_junior_status"] = modify_to
                elif modify_parameter == "member_2_junior_status":
                    row["member_2_junior_status"] = modify_to
            writer.writerow(row)
        
        if found == 0:
            raise ValueError(("\nThe team inputted for modification does not exist, please try again"))
    
    #We check the junior status here again, in the case it was changed
    if "junior_status" in modify_parameter: 
        with open("teams.csv", "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        with open("teams.csv", "w", newline="") as file:
            junior_status = None
            fieldnames = ["team_name", "member_1", "member_1_junior_status", "member_2", "member_2_junior_status", "junior_status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for row in rows:
                if row["team_name"] == team_modify:
                    if row["member_1_junior_status"] == "Y" and row["member_2_junior_status"] == "Y":
                        junior_status = "Y"
                        row["junior_status"] = junior_status
                    else: 
                        junior_status = "N"
                        row["junior_status"] = junior_status
                    writer.writerow(row)                

        with open("team_standings.csv", "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        with open("team_standings.csv", "w", newline="") as file:
            fieldnames = ["team", "points", "total_speaker_score", "junior_status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                if row["team"] == team_modify:
                    row["junior_status"] = junior_status
                writer.writerow(row)

    
def delete_teams(team_modify):
    member_1 = None
    member_2 = None
    with open("teams.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row["team_name"] == team_modify:
                member_1 = row["member_1"]
                member_2 = row["member_2"]

    with open("speaker_standings.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    with open("speaker_standings.csv", "w", newline="") as file:
        fieldnames = ["speaker", "total_speaker_score", "junior_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if row["speaker"] == member_1 or row["speaker"] == member_2:
                continue
            writer.writerow(row)

    with open("teams.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    with open("teams.csv", "w", newline="") as file:
        fieldnames = ["team_name", "member_1", "member_1_junior_status", "member_2", "member_2_junior_status", "junior_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if row["team_name"] == team_modify:
                continue
            writer.writerow(row)

    with open("team_standings.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    with open("team_standings.csv", "w", newline="") as file:
        fieldnames = ["team", "points", "total_speaker_score", "junior_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if row["team"] == team_modify:
                continue
            writer.writerow(row)