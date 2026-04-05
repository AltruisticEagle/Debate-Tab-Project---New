import re

def checks(checked, category):
    matches = None
    if category == "speaker_score": #speaker scores check for ballots.py
        if 65 <= checked <= 85:
            matches = True

    elif category == "name": #speaker/adjudicator name check (general name check)
        matches = re.fullmatch(r"[a-zA-Z ]+", checked) 
    elif category == "team_name": #team name creation/modification check (general team name check)
        matches = re.search(r".", checked)
    elif category == "yes_no": #Y/N for adjudicator status and junior status (general Y/N check)
        matches = re.fullmatch(r"[YN]", checked)
    elif category == "round": #round number check (this literally only checks for numbers and is immutable)
        matches = re.fullmatch(r"\d", checked)

    elif category == "status_check": #status check (this is for scratches.py status fields)
        if checked == "adjudicator" or checked == "team" or checked == "speaker":
            matches = True

    elif category == "adjudicator_feedback_score": #This is the judge feedback score check, 1-10 scale
        if 1 <= int(checked) <= 10:
            matches = True

    elif category == 8: #Not sure what this one is for
        if checked == "Team" or checked == "Speaker":
            matches = True
    return matches