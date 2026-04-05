import adjudicators
import ballots
import breaking
import checks
import draw
import init
import tabs
import teams
import ui
import scratches

class Exit(Exception):
    pass

def main():
    init.create_files()
    starting_ui = ui.starting_ui()
    for i in range(len(starting_ui)):
        print(starting_ui[i])
    function_number = ui.start_prompt()

    if function_number == "1.1":
        team_parameters = ui.ui_1_1()
        teams.create_teams(*team_parameters)

    if function_number == "1.2":
        team_modify, modify_parameter, modify_to = ui.ui_1_2()
        if modify_parameter == "del":
            teams.delete_teams(team_modify)
        else:
            teams.modify_teams(team_modify, modify_parameter, modify_to)

    if function_number == "2.1":
        adjudicator_name, chair_status, trainee_status = ui.ui_2_1()
        adjudicators.create_adjudicators(adjudicator_name, chair_status, trainee_status)

    if function_number == "2.2":
        adjudicator_modify, modify_parameter, modify_to = ui.ui_2_2()
        if modify_parameter == "del":
            adjudicators.delete_adjudicators(adjudicator_modify)
        else:
            adjudicators.modify_adjudicators(adjudicator_modify, modify_parameter, modify_to)
        
    if function_number == "2.3":
        adjudicator_name, round_number, scorer_type, scorer_name, score = ui.ui_2_3()
        adjudicators.create_adjudicator_feedback(adjudicator_name, round_number, scorer_type, scorer_name, score)

    if function_number == "2.4":
        adjudicator_feedback_modify, round_number, scorer_name, score = ui.ui_2_4()
        adjudicators.modify_adjudicator_feedback(adjudicator_feedback_modify, round_number, scorer_name, score)
        
    if function_number == "2.5":
        adjudicator_name = ui.ui_2_5()
        table = adjudicators.view_adjudicator_feedback(adjudicator_name)
        ui.display_adjudicator_feedback(table)

    if function_number == "3.1":
        round_number = ui.ui_3_1()
        new_rows = draw.make_team_draw(round_number)
        table_format_draw = draw.format_team_draw_table(new_rows)
        ui.display_draw(table_format_draw)

    if function_number == "3.2":
        party_1, party_1_status, party_2, party_2_status = ui.ui_3_2()
        scratches.create_scratches(party_1, party_1_status, party_2, party_2_status)
    
    if function_number == "3.3":
        party_1, party_2 = ui.ui_3_3()
        scratches.delete_scratches(party_1, party_2)
    
    if function_number == "3.4": 
        scratch_list = scratches.view_scratches()
        ui.ui_3_4(scratch_list)
    
    if function_number == "4.1":
        round_number, room_number, adjudicator, og_team_name, pm, dpm, oo_team_name, lo, dlo, cg_team_name, mg, gw, co_team_name, mo, ow = ui.ui_4_1()
        ballots.create_ballot(round_number, room_number, adjudicator, og_team_name, pm, dpm, oo_team_name, lo, dlo, cg_team_name, mg, gw, co_team_name, mo, ow)

    if function_number == "4.2":
        round_number, room_number = ui.ui_4_2()
        ballots.modify_ballot(round_number, room_number)

    if function_number == "4.3":
        round_number, room_number = ui.ui_4_3()
        ballot = ballots.display_ballot(round_number, room_number)
        ui.display_ballot(ballot)
    
    if function_number == "5":
        open_breaking, junior_breaking = ui.ui_5()
        open_break, junior_break = breaking.breaking(open_breaking, junior_breaking)
        ui.print_breaking(open_break, junior_break)
    
    if function_number == "6.1":
        table = tabs.speaker_tab()
        headers = ["Rank", "Speaker", "Total Score", "Junior Status"]
        ui.ui_6_1(table, headers)

    if function_number == "6.2":
        table = tabs.team_tab()
        headers = ["Rank", "Team", "Points", "Total Speaker Score", "Junior Status"]
        ui.ui_6_2(table, headers)


if __name__ == "__main__":
    main()