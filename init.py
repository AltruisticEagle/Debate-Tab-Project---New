import os
import csv

def create_files():
    if not os.path.exists("teams.csv"):
        with open("teams.csv", "w") as file:
            fieldnames = ["team_name", "member_1", "member_1_junior_status", "member_2", "member_2_junior_status", "junior_status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.exists("adjudicators.csv"):
        with open("adjudicators.csv", "w") as file:
            fieldnames = ["adjudicator_name", "chair_status", "trainee_status", "rating"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.exists("adjudicator_feedback.csv"):
        with open("adjudicator_feedback.csv", "w") as file:
            fieldnames = ["adjudicator_name", "round", "scorer_type", "scorer_name", "score"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()    

    if not os.path.exists("speaker_standings.csv"):
        with open("speaker_standings.csv", "w") as file:
            fieldnames = ["speaker", "total_speaker_score", "junior_status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.exists("team_standings.csv"):
        with open("team_standings.csv", "w") as file:
            fieldnames = ["team", "points", "total_speaker_score", "junior_status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.exists("ballots.csv"):
        with open("ballots.csv", "w") as file:
            fieldnames = ["round", "room", "adjudicator",
            "pm_name", "pm_score",
            "dpm_name", "dpm_score",
            "lo_name", "lo_score",
            "dlo_name", "dlo_score",
            "mg_name", "mg_score",
            "gw_name", "gw_score",
            "mo_name", "mo_score",
            "ow_name", "ow_score"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.exists("team_draws.csv"):
        with open("team_draws.csv", "w") as file:
            fieldnames = ["round", "room", "OG", "OO", "CG", "CO"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
    
    if not os.path.exists("scratches.csv"):
        with open("scratches.csv", "w") as file:
            fieldnames = ["party_1", "party_1_status", "party_2", "party_2_status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.exists("open_breaks.csv"):
        with open("open_breaks.csv", "w") as file:
            fieldnames = ["team", "points", "total_speaker_score", "junior_status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.exists("junior_breaks.csv"):
        with open("junior_breaks.csv", "w") as file:
            fieldnames = ["team", "points", "total_speaker_score", "junior_status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()