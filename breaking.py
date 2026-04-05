import csv

def breaking(open_breaking, junior_breaking):
    with open("team_standings.csv", "r") as file:
        reader = csv.DictReader(file)
        teams = list(reader)
        ranked_teams = sorted(teams,
        key=lambda row: (int(row["points"]), int(row["total_speaker_score"])), reverse=True)

    with open("open_breaks.csv", "w", newline="") as file:
        fieldnames = ["team", "points", "total_speaker_score", "junior_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(min(open_breaking, len(ranked_teams))):
            writer.writerow(ranked_teams[0])
            ranked_teams.pop(0)

    with open("junior_breaks.csv", "w", newline="") as file:
        fieldnames = ["team", "points", "total_speaker_score", "junior_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        junior_breaking_teams = []
        for team in ranked_teams:
            if team["junior_status"] == "Y":
                junior_breaking_teams.append(team)
        for _ in range(min(junior_breaking, len(junior_breaking_teams))):
            writer.writerow(junior_breaking_teams[0])
            junior_breaking_teams.pop(0)

    with open("open_breaks.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        open_breaks = []
        for i in range(len(rows)):
            open_breaks.append([i + 1, rows[i]["team"], rows[i]["points"], rows[i]["total_speaker_score"], rows[i]["junior_status"]])

    with open("junior_breaks.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        junior_breaks = []
        for i in range(len(rows)):
            junior_breaks.append([i + 1, rows[i]["team"], rows[i]["points"], rows[i]["total_speaker_score"], rows[i]["junior_status"]])
    
    return open_breaks, junior_breaks