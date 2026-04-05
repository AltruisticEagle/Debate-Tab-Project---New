import csv

def speaker_tab():
    with open("speaker_standings.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        tablex = []
        for row in rows:
            tablex.append(row)

    tablex = sorted(tablex, key=lambda row: int(row["total_speaker_score"]), reverse=True)
    table = []
    for i in range(len(tablex)):
        table.append([i + 1, tablex[i]["speaker"], tablex[i]["total_speaker_score"], tablex[i]["junior_status"]])
    
    return table

def team_tab():
    with open("team_standings.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        tablex = []
        for row in rows:
            tablex.append(row)

    tablex = sorted(tablex,
    key=lambda row: (int(row["points"]), int(row["total_speaker_score"])), reverse=True)   
    table = []
    for i in range(len(tablex)):
        table.append([i + 1, tablex[i]["team"], tablex[i]["points"], tablex[i]["total_speaker_score"], tablex[i]["junior_status"]])
    
    return table