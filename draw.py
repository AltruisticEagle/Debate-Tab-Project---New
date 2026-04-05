import csv
import itertools


#This is vibe coding the draw. This is not perfect and a compromise solution.
#If you have a better way of making power-based BP draws that allows teams to be on every position, please let me know.

POSITIONS = ["OG", "OO", "CG", "CO"]


def load_ranked_teams():
    with open("team_standings.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Sort by points only, descending
    ranked = sorted(rows, key=lambda row: int(row["points"]), reverse=True)

    # Return just team names
    return [row["team"] for row in ranked]


def load_position_history():
    """
    Reads existing team_draws.csv and returns:
    history[team_name][position] = count
    """
    history = {}

    with open("team_draws.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    for row in rows:
        for position in POSITIONS:
            team = row[position]
            if team == "PLACEHOLDER":
                continue

            if team not in history:
                history[team] = {"OG": 0, "OO": 0, "CG": 0, "CO": 0}

            history[team][position] += 1

    return history


def score_assignment(permutation, history):
    """
    room: list of team names length 4
    permutation: tuple of team names length 4, mapped to OG/OO/CG/CO
    Lower score is better.
    """
    score = 0
    for position, team in zip(POSITIONS, permutation):
        if team == "PLACEHOLDER":
            continue
        if team not in history:
            score += 0
        else:
            score += history[team][position]
    return score


def best_room_assignment(room, history):
    """
    Returns best assignment dict:
    {"OG": ..., "OO": ..., "CG": ..., "CO": ...}
    plus its score.
    """
    best_score = None
    best_assignment = None

    for permutation in itertools.permutations(room):
        score = score_assignment(permutation, history)

        if best_score is None or score < best_score:
            best_score = score
            best_assignment = {
                "OG": permutation[0],
                "OO": permutation[1],
                "CG": permutation[2],
                "CO": permutation[3],
            }

    return best_assignment, best_score

def make_blocks(ranked_teams):
    """
    Splits ranked teams into blocks of 8.
    Pads the final block with PLACEHOLDER if needed.
    """
    blocks = []

    for i in range(0, len(ranked_teams), 8):
        block = ranked_teams[i:i+8]

        while len(block) < 8:
            block.append("PLACEHOLDER")

        blocks.append(block)

    return blocks


def generate_two_room_splits(block):
    """
    block: list of 8 team names
    Returns unique splits into 2 rooms of 4.
    To avoid duplicate mirrored splits, force block[0] into room1.
    """
    splits = []
    first = block[0]
    remaining = block[1:]

    for combo in itertools.combinations(remaining, 3):
        room1 = [first] + list(combo)
        room2 = block.copy()
        for team in room1:
            room2.remove(team)
        splits.append((room1, room2))

    return splits


def best_two_room_split(block, history):
    """
    block: list of 8 team names
    Returns:
    (best_room1_assignment, best_room2_assignment)
    """
    best_total_score = None
    best_pair = None

    for room1, room2 in generate_two_room_splits(block):
        assignment1, score1 = best_room_assignment(room1, history)
        assignment2, score2 = best_room_assignment(room2, history)

        total_score = score1 + score2

        if best_total_score is None or total_score < best_total_score:
            best_total_score = total_score
            best_pair = (assignment1, assignment2)

    return best_pair


def update_history_with_assignment(history, assignment):
    for position in POSITIONS:
        team = assignment[position]
        if team == "PLACEHOLDER":
            continue

        if team not in history:
            history[team] = {"OG": 0, "OO": 0, "CG": 0, "CO": 0}

        history[team][position] += 1


def make_team_draw(round_number):
    round_number = str(round_number)

    teams = load_ranked_teams()
    history = load_position_history()

    # Prevent duplicate round generation
    with open("team_draws.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["round"] == round_number:
                raise ValueError(f"Round {round_number} already exists in team_draws.csv")

    # Pad with placeholders so total count is divisible by 8 or 4
    # Since we are processing in 8s, pad to multiple of 8 for simplicity
    while len(teams) % 8 != 0:
        teams.append("PLACEHOLDER")

    new_rows = []
    room_number = 1

    for i in range(0, len(teams), 8):
        block = teams[i:i+8]

        # If second half is all placeholders, just do one room
        real_teams_in_block = [team for team in block if team != "PLACEHOLDER"]
        if len(real_teams_in_block) <= 4:
            while len(real_teams_in_block) < 4:
                real_teams_in_block.append("PLACEHOLDER")

            assignment, _ = best_room_assignment(real_teams_in_block, history)

            new_rows.append({
                "round": round_number,
                "room": str(room_number),
                "OG": assignment["OG"],
                "OO": assignment["OO"],
                "CG": assignment["CG"],
                "CO": assignment["CO"],
            })

            update_history_with_assignment(history, assignment)
            room_number += 1

        else:
            assignment1, assignment2 = best_two_room_split(block, history)

            new_rows.append({
                "round": round_number,
                "room": str(room_number),
                "OG": assignment1["OG"],
                "OO": assignment1["OO"],
                "CG": assignment1["CG"],
                "CO": assignment1["CO"],
            })
            update_history_with_assignment(history, assignment1)
            room_number += 1

            new_rows.append({
                "round": round_number,
                "room": str(room_number),
                "OG": assignment2["OG"],
                "OO": assignment2["OO"],
                "CG": assignment2["CG"],
                "CO": assignment2["CO"],
            })
            update_history_with_assignment(history, assignment2)
            room_number += 1

    with open("team_draws.csv", "a", newline="") as file:
        fieldnames = ["round", "room", "OG", "OO", "CG", "CO"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for row in new_rows:
            writer.writerow(row)

    return new_rows

def format_team_draw_table(new_rows):
    """
    Converts the output of make_team_draw() into a table format
    usable by tabulate.
    """
    table = []

    for row in new_rows:
        table.append([
            row["round"],
            row["room"],
            row["OG"],
            row["OO"],
            row["CG"],
            row["CO"],
        ])

    return table