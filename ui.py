import tabulate
import teams
import scratches
import sys
import adjudicators
import ballots

class Exit(Exception):
    pass

def starting_ui():
    starting_ui = [
    "\n"
    "MENU\n",
    "1.1 - Create teams",
    "1.2 - Modify team parameters",
    "\n"
    "2.1 - Create adjudicators",
    "2.2 - Modify adjudicator parameters",
    "2.3 - Input adjudicator feedback",
    "2.4 - Modify adjudicator feedback",
    "2.5 - View adjudicator feedback",
    "\n"
    "3.1 - Generate a draw",
    "3.2 - Input scratches",
    "3.3 - View scratches",
    "3.4 - Delete scratches",
    "\n"
    "4.1 - Input ballots",
    "4.2 - Modify ballots",
    "4.3 - View ballots",
    "\n"
    "5 - Advance teams and adjudicators to break",
    "\n"
    "6.1 - Display speaker tabs",
    "6.2 - Display team tabs",
    "\n"
    "Exit - Type \"exit\""
    ]
    return starting_ui

def start_prompt():
    while True:
        try:
            function_number = input("Please input the number of the function you want to use: ").strip().lower()
            if function_number == "exit":
                raise Exit
            
            function_numbers = ["1.1", 
            "1.2", 
            "2.1", 
            "2.2", 
            "2.3", 
            "2.4", 
            "2.5", 
            "3.1", 
            "3.2", 
            "4.1", 
            "4.3", 
            "5", 
            "6.1", 
            "6.2"]
            if function_number in function_numbers:
                return function_number
            else:
                raise Exception

        except Exit:
            sys.exit()

        except Exception:
            print("\nInvalid input, please enter the number of the function you want to use only\n")
            continue

def ui_1_1():
    print(
        "\nInput the new team's parameters.\nInput \"exit\" in the first prompt to exit.\n")
        
    while True:
        try:
            team_name = input("New team's name: ").strip()
            if team_name.lower() == "exit":
                raise Exit
            member_1 = input("Team member 1's full name: ").strip()
            member_1_junior_status = input("Is member 1 a junior speaker? Y/N: ").upper().strip()
            member_2 = input("Team member 2's full name: ").strip()
            member_2_junior_status = input("Is member 2 a junior speaker? Y/N: ").upper().strip()

            teams.create_team_check(team_name, member_1, member_1_junior_status, member_2, member_2_junior_status)

            print("\nTeam created.\n")
            return team_name, member_1, member_1_junior_status, member_2, member_2_junior_status

        except Exit:
            sys.exit()
        except Exception:
            print("\nInvalid input, try again\n")
            continue

def ui_1_2():
    print("\nTo delete a team, input \"del\" into the second prompt.\n"
        "Otherwise, input the parameter you want to modify in the same prompt: \"team_name\", \"member_1\", \"member_2\"," 
        "\"member_1_junior_status\", or \"member_2_junior_status\" exactly.\n"
        "Input \"exit\" in the first input to modify to exit.\n")
        
    while True:
        try:
            team_modify = input("Team to modify: ").strip()
            if team_modify.lower() == "exit":
                raise Exit
            modify_parameter = input("Modify which parameter? ").strip()
            if modify_parameter not in ["team_name", "member_1", "member_2", 
                                        "member_1_junior_status", "member_2_junior_status",
                                        "del"]:
                print("\nInvalid input, try again\n")
                continue

            modify_to = None
            if not modify_parameter == "del":
                modify_to = input("Modify to what? ").strip()
            
            else:
                teams.modify_team_check(modify_parameter, modify_to)                  

            print("\nModified team successfully.")
            return(team_modify, modify_parameter, modify_to)

        except Exit:
            sys.exit()
        except Exception:
            print("\nInvalid input, try again\n")
            continue

def ui_2_1():
    print("\nFor the first prompt, input the new adjudicator's name in format adjudicator's first and last name, then answer the questions about status with Y/N.\n"
    "Input \"exit\" in the first prompt to exit.\n")
    while True:
        try:
            adjudicator_name = input("New adjudicator's name: ").strip()
            if adjudicator_name.lower() == "exit":
                raise Exit
            adjudicators.check_adjudicator_already_exists(adjudicator_name)
            chair_status = input("Can they chair? Y/N: ").title().strip()
            trainee_status = input("Are they a trainee? Y/N: ").title().strip()

            print("Adjudicator created.\n")
            return adjudicator_name, chair_status, trainee_status

        except Exit:
            sys.exit()
        except Exception:
            print("\nInvalid input, try again\n")
            continue

def ui_2_2():
    print("\nTo delete an adjudicator, input \"del\" in the second prompt.\n"
    "Otherwise, type in the parameter you want to modify in the same " 
    "prompt: \"adjudicator_name\", \"chair_status\", or \"trainee_status\" exactly.\n"
    "To modify chair status or trainee status, input simply Y or N (capitalized as is here) " 
    "in the third prompt depending on what you want to modify it to.\n"
    "Input \"exit\" in the first input to exit. \n")
    while True:
        try:
            adjudicator_modify = input("Adjudicator to modify: ").strip()
            if adjudicator_modify.lower() == "exit":
                raise Exit
            modify_parameter = input("Modify which parameter? ").strip()
            if modify_parameter not in ["adjudicator_name", 
                                        "chair_status", 
                                        "trainee_status", 
                                        "del"]:
                print("\nInvalid input, try again\n")
                continue

            modify_to = None
            if not modify_parameter == "del":
                modify_to = input("Modify to what? ").strip()
            
            else:
                adjudicators.check_modify_adjudicators(modify_parameter, modify_to)

            print("\nModified adjudicator successfully.\n")
            return adjudicator_modify, modify_parameter, modify_to

        except Exit:
            sys.exit()
        except Exception:
            print("\nInvalid input, try again\n")
            continue

def ui_2_3():
    print("\nFor prompt 3, input \"adjudicator\" or \"speaker\".\n"
          "For prompt 2, input the round number only (e.g. \"1\", \"2\", etc.\n"
        "Input \"exit\" in the first prompt to exit.\n")
    while True:
        try:
            adjudicator_name = input("To which adjudicator is this feedback directed? ").strip()
            if adjudicator_name.lower() == "exit":
                raise Exit
            round_number = input("In which round? ").strip()
            scorer_type = input("Is the submitter an adjudicator or a speaker? ").strip()
            scorer_name = input("What is the scorer's name? ").strip()
            score = int(input("Feedback score: ").strip())

            print(f"\nInputted feedback score for {adjudicator_name} successfully.\n")
            return adjudicator_name, round_number, scorer_type, scorer_name, score
        
        except Exit:
            sys.exit()
        except Exception:
            print("\nInvalid input, try again\n")
            continue

def ui_2_4():
    print("\nThis function only deletes the feedback line that is faulty for practicality"
          " - to edit it, input the edited version again with 2.3.\n"
          "For prompt 3, input the round number only (e.g. \"1\", \"2\", etc.\n"
    "Input \"exit\" in the first prompt to exit.\n")
    while True:
        try:
            adjudicator_feedback_modify = input("To which adjudicator was the feedback directed to? ").strip()
            if adjudicator_feedback_modify.lower() == "exit":
                raise Exit
            scorer_name = input("Who was the submitter? ").strip()
            round_number = int(input("In which round was this score submitted? ").strip())
            score = int(input("What was the score? ").strip())

            print("\nFeedback score deleted - input the modified feedback again if desired with function 2.2.\n")
            return adjudicator_feedback_modify, round_number, scorer_name, score
        
        except Exit:
            sys.exit()        
        except ValueError:
            print("\nInvalid input, try again\n")
            continue

def ui_2_5():
    print("\nInput \"exit\" in the first prompt to exit.\n")
    while True:
        try:
            adjudicator_name = input("See which adjudicator's feedback scores? ").strip()
            if adjudicator_name.lower() == "exit":
                raise Exit
            
            return adjudicator_name

        except Exit:
            sys.exit()
        except ValueError:
            print("\nInvalid input, try again\n")
            continue

def display_adjudicator_feedback(table):
    headers = ["Round", "Submitter", "Submitter's status", "Feedback score"]
    print(tabulate.tabulate(table, headers, tablefmt="outline"))

def ui_3_1():
    print("\nInput the round number only (e.g. \"1\", \"2\", etc.).\n"
        "Input \"exit\" in the first prompt to exit.\n")
    while True:
        try:
            round_number = input("Generate a draw for which round? ")
            if round_number == "exit":
                raise Exit
            
            return int(round_number)

        except Exit:
            sys.exit()
        except Exception:
            print("\nInvalid input, try again\n")
            continue

def display_draw(table):
    headers = ["Round", "Room", "OG", "OO", "CG", "CO"]
    print(tabulate.tabulate(table, headers, tablefmt="outline"))    

def ui_3_2():
    print("\nInput the parties that need to be scratched by any form of conflict.\n"
    "In the second and fourth prompts, input the status of the party (\"team\" or \"adjudicator\") exactly.\n"
    "For a team, input the team name into the party name prompt(s). "
    "Do not input a given speaker's name, input their team name.\n"
    "Input \"exit\" in the first prompt to exit.\n")
    while True:
        try:
            party_1 = input("First party's name: ").strip()
            if party_1.lower() == "exit":
                raise Exit
            party_1_status = input("First party's status: ").strip()
            party_2 = input("Second party's name: ").strip()
            party_2_status = input("Second party's status: ").strip()

            scratches.check_create_scratches(party_1_status, party_2_status)
            
            print("\nScratch successfully inputted.\n")
            return party_1, party_1_status, party_2, party_2_status
            
        except Exit:
            sys.exit()
        except Exception:
            print("\nInvalid input, try again\n")
            continue

def ui_3_3():
    print("\nThis function only deletes the faulty scratch for practicality - to edit it, input the edited version again with 3.2.\n"
        "Input \"exit\" in the first prompt to exit.\n")
    while True:
        try:
            party_1 = input("First party's name: ").strip()
            if party_1.lower() == "exit":
                raise Exit
            party_2 = input("Second party's name: ").strip()

            print("\nScratch successfully deleted. Input the modified feedback again if desired with function 3.2.\n")
            return party_1, party_2
        
        except Exit:
            sys.exit()
        except Exception:
            print("\nInvalid input, try again\n")
            continue
        
def ui_3_4(scratch_list):
    for i in range(len(scratch_list)):
        print(scratch_list[i])

def ui_4_1():
    print("\nFor room and round number, input the number only (e.g. \"1\", \"2\", etc.\n"
        "Input \"exit\" in the first prompt to exit.\n")
    while True:
        try:
            round_number = input("Which round is this ballot from? ").strip()
            if round_number.lower() == "exit":
                raise Exit
            round_number = int(round_number)
            room_number = int(input("Which room is the ballot from? "))
            adjudicator = input("Who submitted this ballot? ").strip()
            
            og_team_name = input("What is the name of the team on OG? ").strip()
            pm_name = input("Who was the PM speaker? (Full Name) ").strip()
            pm_speaker_score = int(input("PM speaker score (whole number, 65-85): "))
            pm = {"name": pm_name, "speaker_score": pm_speaker_score}

            dpm_name = input("Who was the DPM speaker? (Full Name) ").strip()
            dpm_speaker_score = int(input("DPM speaker score (whole number, 65-85): "))
            dpm = {"name": dpm_name, "speaker_score": dpm_speaker_score}

            oo_team_name = input("What is the name of the team on OO? ").strip()
            lo_name = input("Who was the LO speaker? (Full Name) ").strip()
            lo_speaker_score = int(input("LO speaker score (whole number, 65-85): "))
            lo = {"name": lo_name, "speaker_score": lo_speaker_score}

            dlo_name = input("Who was the DLO speaker? (Full Name) ").strip()
            dlo_speaker_score = int(input("DLO speaker score (whole number, 65-85): "))
            dlo = {"name": dlo_name, "speaker_score": dlo_speaker_score}

            cg_team_name = input("What is the name of the team on CG? ").strip()
            mg_name = input("Who was the MG speaker? (Full Name) ").strip()
            mg_speaker_score = int(input("MG speaker score (whole number, 65-85): "))
            mg = {"name": mg_name, "speaker_score": mg_speaker_score}

            gw_name = input("Who was the GW speaker? (Full Name) ").strip()
            gw_speaker_score = int(input("GW speaker score (whole number, 65-85): "))
            gw = {"name": gw_name, "speaker_score": gw_speaker_score}
            
            co_team_name = input("What is the name of the team on CO? ").strip()
            mo_name = input("Who was the MO speaker? (Full Name) ").strip()
            mo_speaker_score = int(input("MO speaker score (whole number, 65-85): "))
            mo = {"name": mo_name, "speaker_score": mo_speaker_score}

            ow_name = input("Who was the OW speaker? (Full Name) ").strip()
            ow_speaker_score = int(input("OW speaker score (whole number, 65-85): "))
            ow = {"name": ow_name, "speaker_score": ow_speaker_score}

            ballots.check_create_ballot(round_number, room_number, adjudicator, pm, dpm, lo, dlo, mg, gw, mo, ow)
            return round_number, room_number, adjudicator, og_team_name, pm, dpm, oo_team_name, lo, dlo, cg_team_name, mg, gw, co_team_name, mo, ow
        
        except Exit:
            sys.exit()
        except Exception:
            print("\nInvalid input, try again\n")
            continue

def ui_4_2():
    while True:
        try:
            print("\nIt is virtually impossible to make acceptable code that doens't break anything when modifying a ballot in this system.\n"
                "Therefore this deletes a faulty ballot only. If you want to modify a ballot, delete it first and then re-input it.\n"
                "When prompted for round and room number, input the numbers only (e.g. \"1\", \"2\", etc.\n"
                "Input \"exit\" in the first prompt to exit.\n")
            round_number = input("Round number: ").strip()
            if round_number.lower() == "exit":
                raise Exit
            round_number = int(round_number)
            room_number = int(input("Room number: ").strip())

            print("\nBallot deleted - input the modified ballot again if desired with function .\n")
            return round_number, room_number
        
        except Exit:
            sys.exit()
        except Exception:
            print("\nInvalid input, try again\n")
            continue

def ui_4_3():
    while True:
        try:        
            print("\nWhen prompted for round and room number, input the numbers only (e.g. \"1\", \"2\", etc.\n"
                "Input \"exit\" in the first prompt to exit.\n")
            round_number = input("Round number: ").strip()
            if round_number.lower() == "exit":
                raise Exit
            round_number = int(round_number)
            room_number = int(input("Room number: ").strip())

            return round_number, room_number
        
        except Exit:
            sys.exit()
        except Exception:
            print("\nInvalid input, try again\n")
            continue

def display_ballot(ballot):
    for i in ballot:
        print(i)

def ui_5():
    print(
        "\nEnter the number of teams you want into each breaking bracket's prompt." 
        "If there is no junior break, ignore the junior breaking table.\n"
        "Input \"exit\" in any prompt to exit.\n")
    while True:
        try:
            open_breaking = input("How many teams break into the open bracket? ")
            if open_breaking.lower() == "exit":
                raise Exit
            junior_breaking = input("How many teams break into the junior category? ")
            if junior_breaking.lower() == "exit":
                raise Exit
            return int(open_breaking), int(junior_breaking)
                
        except Exit:
            sys.exit()
        except ValueError:
            print("\nPlease enter numbers in the inputs")
            continue
        except Exception:
            print("\nThere has been some sort of issue, try again\n")
            continue

def print_breaking(open_break, junior_break):    
    try:
        headers = ["Breaking Rank", "Team Name", "Points", "Total Speaker Score", "Junior Status"]
        print("\nOPEN BREAKING\n", tabulate.tabulate(open_break, headers, tablefmt="outline"))
        print("\nJUNIOR BREAKING\n", tabulate.tabulate(junior_break, headers, tablefmt="outline"))
    except:
        print("\nInvalid input, try again\n")

def ui_6_1(table, headers):
    print(tabulate.tabulate(table, headers, tablefmt="outline"))

def ui_6_2(table, headers):
    print(tabulate.tabulate(table, headers, tablefmt="outline"))