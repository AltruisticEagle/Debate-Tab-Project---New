import csv
import checks

def check_create_scratches(party_1_status, party_2_status):
    matches1 = checks.checks(party_1_status, "status_check")
    matches2 = checks.checks(party_2_status, "status_check")
    matches = [matches1, matches2]
    for i in matches:
        if i == None:
            print("match failed")
            raise Exception

def create_scratches(party_1, party_1_status, party_2, party_2_status):
    with open("scratches.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    with open("scratches.csv", "a", newline="") as file:
        new_scratch = {"party_1": party_1, "party_1_status": party_1_status,
        "party_2": party_2, "party_2_status": party_2_status}

        for row in rows:
            if row == new_scratch:
                raise ValueError("\nThis scratch already exists, try again to input other scratches")
            
        fieldnames = ["party_1", "party_1_status", "party_2", "party_2_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(new_scratch)

def delete_scratches(party_1, party_2):
    parties = [party_1, party_2]
    with open("scratches.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    
    with open("scratches.csv", "w", newline="") as file:
        fieldnames = ["party_1", "party_1_status", "party_2", "party_2_status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if row["party_1"] in parties and row["party_2"] in parties:
                continue
            writer.writerow(row)

def view_scratches():
    scratch_list = []
    with open("scratches.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

        i = 0
        print("\nSCRATCHES")
        for row in rows:
            i += 1
            scratch_list.append(f"Scratch {i}: {row['party_1']}, {row['party_2']}")

    return scratch_list