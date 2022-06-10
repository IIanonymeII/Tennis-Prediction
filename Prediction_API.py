from keras.models import load_model
import pickle
import keras
import pandas as pd
import web_scrapping
import datetime
import argparse

parser = argparse.ArgumentParser(description='Code for player')
parser.add_argument('--test', help='yeau to study (int)', default=False) #choisir le nom du ficher
args = parser.parse_args()
test_arg = bool(args.test)



date_now = datetime.date.today()

 

def retrieve_percentages(player_id, srface):
    df_players = pd.read_csv('Players_Statistics_.csv')
    df = df_players.loc[df_players['id'] == player_id]
    df = df.reset_index(drop=True)
    victory_percentage = df['victory_percentage'][0]
    victory_percentage_surface = df['%s_victory_percentage' % srface.lower()][0]
    ace_percentage = df['ace_percentage'][0]
    doublefaults_percentage = df['doublefault_percentage'][0]
    first_serve_success = df['first_serve_success_percentage'][0]
    winning_on_first_serve = df['winning_on_1st_serve_percentage'][0]
    winning_on_second_serve = df['winning_on_2nd_serve_percentage'][0]
    overall_win_on_serve = df['overall_win_on_serve_percentage'][0]
    break_points_faced = df['breakpoint_faced_percentage'][0]
    break_points_saved = df['breakpoint_saved_percentage'][0]
    return[victory_percentage, victory_percentage_surface, ace_percentage, doublefaults_percentage, first_serve_success,
           winning_on_first_serve, winning_on_second_serve, overall_win_on_serve, break_points_faced, break_points_saved]

# MODEL PARAMETERS
liste = web_scrapping.main()

df_test = pd.DataFrame(columns=['Player_1', 'pourcentage_victory_1',  'Player_1', 'pourcentage_victory_2', 'tournoi'])

for i in liste:
    print("\n\n\n\n===============================================================================\n\n\n\n")
    print(i)

    model_year = 2021
    model = load_model('prediction_model.h5')

    with open('indicators_dicts_year/indicators_dicts_%i' % model_year, 'rb') as file:
        my_Unpickler = pickle.Unpickler(file)
        [tournaments_dict, level_dict, surface_dict, extrema_dict] = my_Unpickler.load()





    # INPUT DATA

    # Match
    tournament = i[0]
    surface = 'Grass'
    level = 'G'

    # Player 1

    name_p1 = i[1]["name"]
    id_p1 = int(i[1]["id"])

    rank_p1 = int(i[1]["classement"])
    points_p1 = int(i[1]["points"])
    hand_p1 = 'R'
    height_p1 = int(i[1]["Taille"])
    fatigue_p1 = 3
    age_p1 = int(i[1]["age"])

    percentages_p1 = retrieve_percentages(id_p1, surface)
    print('PERCENTAGES P1:', percentages_p1)

    last_matches_win_percentages_p1 = int(i[1]["last_5_matches_win"])/5  # Last 5 matches
    last_matches_surface_p1 = 0.4  # Last 5 matches
    win_percentage_actual_over_other_p1 = int(float(i[1]["proba"]))/100


    # Player 2

    name_p2 = i[2]["name"]
    id_p2 = int(i[2]["id"])

    rank_p2 = int(i[2]["classement"])
    points_p2 = int(i[2]["points"])
    hand_p2 = 'R'
    height_p2 = int(i[2]["Taille"])
    fatigue_p2 = 3
    age_p2 = int(i[2]["age"])

    percentages_p2 = retrieve_percentages(id_p2, surface)
    print('PERCENTAGES P2:', percentages_p2)

    last_matches_win_percentages_p2 = int(i[2]["last_5_matches_win"])/5 # Last 5 matches
    last_matches_surface_p2 = 0.4  # Last 5 matches
    win_percentage_actual_over_other_p2 = int(float(i[2]["proba"]))/100

    # TREATMENT FUNCTIONS


    def percentage_treatment(prctg):
        if prctg > 1:
            return 0.01 * prctg
        else:
            return prctg


    def float_treatment(floated, maximum, minimum):
        return (2 / (maximum - minimum)) * floated - ((maximum + minimum) / (maximum - minimum))


    data_treated = []

    # TREATMENT TO FEED THE NETWORK

    # Match

    match_data = []

    # Tournament

    maxi = 69
    mini = 1

    if tournament in tournaments_dict.keys():
        match_data.append(float_treatment(tournaments_dict[tournament], maxi, mini))
    elif 'Davis' in tournament:
        match_data.append(float_treatment(69, maxi, mini))
    else:
        print('--  New Tournament  --')
        print(tournament)
        match_data.append(float_treatment(70, maxi, mini))

    # Level

    maxi = 6
    mini = 1
    match_data.append(float_treatment(level_dict[level], maxi, mini))

    # Surface

    maxi = 4
    mini = 1
    match_data.append(float_treatment(surface_dict[surface], maxi, mini))

    # Player 1

    p1_data = []

    # Rank

    couple = extrema_dict[3]
    p1_data.append(float_treatment(rank_p1, couple[1], couple[0]))

    # Points

    couple = extrema_dict[4]
    p1_data.append(float_treatment(points_p1, couple[1], couple[0]))

    # Hand

    if hand_p1 == 'L':
        p1_data.append(0)
    else:
        p1_data.append(1)

    # Height

    couple = extrema_dict[6]
    p1_data.append(float_treatment(height_p1, couple[1], couple[0]))

    # Fatigue

    couple = extrema_dict[7]
    p1_data.append(float_treatment(fatigue_p1, couple[1], couple[0]))

    # Age

    couple = extrema_dict[8]
    p1_data.append(float_treatment(age_p1, couple[1], couple[0]))

    # Percentages

    for percentage in percentages_p1:
        p1_data.append(percentage_treatment(percentage))

    # Last_matches_win_percentage

    p1_data.append(percentage_treatment(last_matches_win_percentages_p1))

    # Last matches surface win percentage

    p1_data.append(percentage_treatment(last_matches_surface_p1))

    # Win percentage over P2

    p1_data.append(percentage_treatment(win_percentage_actual_over_other_p2))

    # Player 2

    p2_data = []

    # Rank

    couple = extrema_dict[3]
    p2_data.append(float_treatment(rank_p2, couple[1], couple[0]))

    # Points

    couple = extrema_dict[4]
    p2_data.append(float_treatment(points_p2, couple[1], couple[0]))

    # Hand

    if hand_p2 == 'L':
        p2_data.append(0)
    else:
        p2_data.append(1)

    # Height

    couple = extrema_dict[6]
    p2_data.append(float_treatment(height_p2, couple[1], couple[0]))

    # Fatigue

    couple = extrema_dict[7]
    p2_data.append(float_treatment(fatigue_p2, couple[1], couple[0]))

    # Age

    couple = extrema_dict[8]
    p2_data.append(float_treatment(age_p2, couple[1], couple[0]))

    # Percentages

    for percentage in percentages_p2:
        p2_data.append(percentage_treatment(percentage))

    # Last_matches_win_percentage

    p2_data.append(percentage_treatment(last_matches_win_percentages_p2))

    # Last matches surface win percentage

    p2_data.append(percentage_treatment(last_matches_surface_p2))

    # Win percentage over P1

    p2_data.append(percentage_treatment(win_percentage_actual_over_other_p2))

    input_data = match_data + p1_data + p2_data
    # print('P2 data:', p2_data)
    # print(input_data)
    input_data = pd.DataFrame([input_data])
    # print(input_data)
    prediction = model.predict(input_data.values)

    print('Prediction: ', prediction)

    print('What will ne the results?')
    print(name_p1, ':', prediction[0][0]*100, '% Chances of victory')
    print(name_p2, ':', prediction[0][1]*100, '% Chances of victory')

    
    
    if test_arg:
        add_test = pd.DataFrame([[name_p1, prediction[0][0]*100,  name_p2, prediction[0][1]*100, tournament]],
                                                    columns=['Player_1', 'pourcentage_victory_1',  'Player_1', 'pourcentage_victory_2', 'tournoi'])
        
        try :
            df_test = df_test.append(add_test)
            
        except:
            print("\n\n\n\n===================== ereur =====================\n\n\n\n")
    
if test_arg:                                          
    df_test.to_csv('test_stat'+'_'+str(date_now.strftime("%d"))+'_'+str(date_now.strftime("%m"))+'_'+str(date_now.strftime("%Y"))+'.csv', index=False)