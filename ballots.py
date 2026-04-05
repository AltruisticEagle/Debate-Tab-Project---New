import csv
from checks import checks
from reader import read_csv

ballot_fieldnames = [
"round",
"room",
"adjudicator",
"pm_name",
"pm_score",
"dpm_name",
"dpm_score",
"lo_name",
"lo_score",
"dlo_name",
"dlo_score",
"mg_name",
"mg_score",
"gw_name",
"gw_score",
"mo_name",
"mo_score",
"ow_name",
"ow_score",
"og_team_name",
"oo_team_name",
"cg_team_name",
"co_team_name"]

def check_create_ballot(round_number, room_number, adjudicator, pm, dpm, lo, dlo, mg, gw, mo, ow):
    matches1 = checks(str(round_number), "round")
    matches1_1 = checks(str(room_number), "round")
    matches2 = checks(adjudicator, "name")
    matches3 = checks(pm["name"], "name")
    matches4 = checks(dpm["name"], "name")
    matches5 = checks(lo["name"], "name")
    matches6 = checks(dlo["name"], "name")
    matches7 = checks(mg["name"], "name")
    matches8 = checks(gw["name"], "name")
    matches9 = checks(mo["name"], "name")
    matches10 = checks(ow["name"], "name")

    matches11 = checks(pm["speaker_score"], "speaker_score")
    matches12 = checks(dpm["speaker_score"], "speaker_score")
    matches13 = checks(lo["speaker_score"], "speaker_score")
    matches14 = checks(dlo["speaker_score"], "speaker_score")
    matches15 = checks(mg["speaker_score"], "speaker_score")
    matches16 = checks(gw["speaker_score"], "speaker_score")
    matches17 = checks(mo["speaker_score"], "speaker_score")
    matches18 = checks(ow["speaker_score"], "speaker_score")

    matches = [
        matches1,
        matches1_1, 
        matches2, 
        matches3, 
        matches4, 
        matches5, 
        matches6, 
        matches7, 
        matches8, 
        matches9, 
        matches10, 
        matches11,
        matches12,
        matches13,
        matches14,
        matches15,
        matches16,
        matches17,
        matches18]
    
    for i in matches:
        if i is None:
            raise Exception

def check_view_ballot(round_number, room_number):
    matches == None
    matches1 = checks(round_number, "round")
    matches2 = checks(room_number, "round")
    matches = [matches1, matches2]
    for i in matches:
        if i == None:
            raise Exception

def write_to_standings(og_team_name, pm, dpm, oo_team_name, lo, dlo, cg_team_name, mg, gw, co_team_name, mo, ow):
    #Mirroring logic on the teams
    team_names = [og_team_name, oo_team_name, cg_team_name, co_team_name]

    ranking = make_ranking({
        "pm_score": pm["speaker_score"],
        "dpm_score": dpm["speaker_score"],
        "lo_score": lo["speaker_score"],
        "dlo_score": dlo["speaker_score"],
        "mg_score": mg["speaker_score"],
        "gw_score": gw["speaker_score"],
        "mo_score": mo["speaker_score"],
        "ow_score": ow["speaker_score"],
    })

    position_to_team = {
        "OG": og_team_name,
        "OO": oo_team_name,
        "CG": cg_team_name,
        "CO": co_team_name,
    }

    position_to_total = {
        "OG": int(pm["speaker_score"]) + int(dpm["speaker_score"]),
        "OO": int(lo["speaker_score"]) + int(dlo["speaker_score"]),
        "CG": int(mg["speaker_score"]) + int(gw["speaker_score"]),
        "CO": int(mo["speaker_score"]) + int(ow["speaker_score"]),
    }

    rows = read_csv("team_standings.csv")
    for i in range(4):
        found = False
        for row in rows:
            if row["team"] == team_names[i]:
                found = True
                break
        if not found:
            raise ValueError(f"Team #{i + 1} in the ballot doesn't exist, please try again")

    points_by_rank = [3, 2, 1, 0]
    team_updates = {}

    for i in range(4):
        position = ranking[i][0]
        team_name = position_to_team[position]
        speaker_total = position_to_total[position]
        points = points_by_rank[i]

        team_updates[team_name] = {
            "points": points,
            "total_speaker_score": speaker_total
        }

    with open("team_standings.csv", "w", newline="") as file:
        fieldnames = ["team", "points", "total_speaker_score", "junior_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            if row["team"] in team_updates:
                row["points"] = int(row["points"]) + int(team_updates[row["team"]]["points"])
                row["total_speaker_score"] = int(row["total_speaker_score"]) + int(team_updates[row["team"]]["total_speaker_score"])
            writer.writerow(row)

    speakers = [
            pm["name"],
            dpm["name"],
            lo["name"],
            dlo["name"],
            mg["name"],
            gw["name"],
            mo["name"],
            ow["name"],]
    
    speaker_scores = [
            pm["speaker_score"],
            dpm["speaker_score"],
            lo["speaker_score"],
            dlo["speaker_score"],
            mg["speaker_score"],
            gw["speaker_score"],
            mo["speaker_score"],
            ow["speaker_score"],]
    
    rows = read_csv("speaker_standings.csv")
    for i in range(8):
        found = False
        for row in rows:
            if row["speaker"] == speakers[i]:
                found = True
                break
        if not found:
            raise ValueError(f"Speaker #{i + 1} in the ballot doesn't exist, please try again")
        
    speaker_updates = {
        speakers[0]: speaker_scores[0],
        speakers[1]: speaker_scores[1],
        speakers[2]: speaker_scores[2],
        speakers[3]: speaker_scores[3],
        speakers[4]: speaker_scores[4],
        speakers[5]: speaker_scores[5],
        speakers[6]: speaker_scores[6],
        speakers[7]: speaker_scores[7],
    }

    with open("speaker_standings.csv", "w", newline="") as file:
        fieldnames = ["speaker", "total_speaker_score", "junior_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            if row["speaker"] in speaker_updates:
                row["total_speaker_score"] = int(row["total_speaker_score"]) + int(speaker_updates[row["speaker"]])
            writer.writerow(row)
        
def make_ranking(row):
    og_total = int(row["pm_score"]) + int(row["dpm_score"])
    oo_total = int(row["lo_score"]) + int(row["dlo_score"])
    cg_total = int(row["mg_score"]) + int(row["gw_score"])
    co_total = int(row["mo_score"]) + int(row["ow_score"])
    ranking = [
        ("OG", og_total),
        ("OO", oo_total),
        ("CG", cg_total),
        ("CO", co_total),
    ]
    if og_total == oo_total or og_total == cg_total or og_total == co_total or oo_total == cg_total or oo_total == co_total or cg_total == co_total:
        raise ValueError("\nThere are two teams with the same total speaker score, please resolve")

    ranking = sorted(ranking, key=lambda x: x[1], reverse=True)
    return ranking

def create_ballot(round_number, room_number, adjudicator, og_team_name, pm, dpm, oo_team_name, lo, dlo, cg_team_name, mg, gw, co_team_name, mo, ow):
    check_create_ballot(round_number, room_number, adjudicator, pm, dpm, lo, dlo, mg, gw, mo, ow)

    with open("ballots.csv", "a", newline="") as file:
        fieldnames = ballot_fieldnames
        writer = csv.DictWriter(file, fieldnames)

        row = {
            fieldnames[0]: round_number,
            fieldnames[1]: room_number,
            fieldnames[2]: adjudicator,
            fieldnames[3]: pm["name"],
            fieldnames[4]: pm["speaker_score"], 
            fieldnames[5]: dpm["name"],
            fieldnames[6]: dpm["speaker_score"],
            fieldnames[7]: lo["name"],
            fieldnames[8]: lo["speaker_score"], 
            fieldnames[9]: dlo["name"],
            fieldnames[10]: dlo["speaker_score"],
            fieldnames[11]: mg["name"],
            fieldnames[12]: mg["speaker_score"],
            fieldnames[13]: gw["name"],
            fieldnames[14]: gw["speaker_score"],
            fieldnames[15]: mo["name"],
            fieldnames[16]: mo["speaker_score"],
            fieldnames[17]: ow["name"],
            fieldnames[18]: ow["speaker_score"],
            fieldnames[19]: og_team_name,
            fieldnames[20]: oo_team_name,
            fieldnames[21]: cg_team_name,
            fieldnames[22]: co_team_name
        }
            
        write_to_standings(og_team_name, pm, dpm, oo_team_name, lo, dlo, cg_team_name, mg, gw, co_team_name, mo, ow)    
        writer.writerow(row)

def modify_ballot(round_number, room_number):
    rows = read_csv("ballots.csv")

    with open("ballots.csv", "w", newline = "") as file:
        writer = csv.DictWriter(file, fieldnames=ballot_fieldnames)
        writer.writeheader()
        found = 0
        for row in rows: 
            if row["round"] == str(round_number) and row["room"] == str(room_number):
                found += 1
                continue
            writer.writerow(row)
        
        if found == 0:
            raise ValueError("\nThe inputted ballot does not exist, please try again")

    reset_speaker_standings()
    reset_team_standings()

    rows = read_csv("ballots.csv")

    for row in rows:
        og_team_name = row["og_team_name"]
        oo_team_name = row["oo_team_name"]
        cg_team_name = row["cg_team_name"]
        co_team_name = row["co_team_name"] 
        pm  = {"name": row["pm_name"],  "speaker_score": int(row["pm_score"])}
        dpm = {"name": row["dpm_name"], "speaker_score": int(row["dpm_score"])}
        lo  = {"name": row["lo_name"],  "speaker_score": int(row["lo_score"])}
        dlo = {"name": row["dlo_name"], "speaker_score": int(row["dlo_score"])}
        mg  = {"name": row["mg_name"],  "speaker_score": int(row["mg_score"])}
        gw  = {"name": row["gw_name"],  "speaker_score": int(row["gw_score"])}
        mo  = {"name": row["mo_name"],  "speaker_score": int(row["mo_score"])}
        ow  = {"name": row["ow_name"],  "speaker_score": int(row["ow_score"])}
        write_to_standings(og_team_name, pm, dpm, oo_team_name, lo, dlo, cg_team_name, mg, gw, co_team_name, mo, ow)       

def display_ballot(round_number, room_number):
    ballot = []
    rows = read_csv("ballots.csv")
    for row in rows:
        if row["round"] == str(round_number) and row["room"] == str(room_number):
            ballot.append(f"OG team: {row["og_team_name"]}, {int(row["pm_score"]) + int(row["dpm_score"])} points")
            ballot.append(f"OO team: {row["oo_team_name"]}, {int(row["lo_score"]) + int(row["dlo_score"])} points")
            ballot.append(f"CG team: {row["cg_team_name"]}, {int(row["mg_score"]) + int(row["gw_score"])} points")
            ballot.append(f"CO team: {row["og_team_name"]}, {int(row["mo_score"]) + int(row["ow_score"])} points")
    
    return ballot

def reset_speaker_standings():
    rows = read_csv("speaker_standings.csv")

    with open("speaker_standings.csv", "w", newline="") as file:
        fieldnames = ["speaker", "total_speaker_score", "junior_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            row["total_speaker_score"] = 0
            writer.writerow(row)

def reset_team_standings():
    rows = read_csv("team_standings.csv")

    with open("team_standings.csv", "w", newline="") as file:
        fieldnames = ["team", "points", "total_speaker_score", "junior_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            row["points"] = 0
            row["total_speaker_score"] = 0
            writer.writerow(row)