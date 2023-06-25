import pandas as pd
from clean_data import clean_data
from machine_learning import predictMVP
from scrape_files.scrape_team_stats import get_team_stats 
from scrape_files.scrape_player_stats import get_player_stats
from scrape_files.scrape_mvp_stats import get_mvp_stats


years_back = 22


'''
This method scrapes www.basketball-reference.com for NBA info.
Avoid using this method as I've already saved csv files for all these
regular season stats from the past 22 years in the stats folder. This method 
makes a lot of requests from the website and can cause problems.
Use the get_stats method for same results
'''
def scrape_for_stats():
    # Returns pandas DF of stats of all players and teams for last x years
    # in x DataFrames contcatted together
    team_stats = get_team_stats(years_back)
    mvp_stats = get_mvp_stats(years_back)

    player_stats = get_player_stats(years_back, "per_game")

    # Gets advanced player statistics
    adv_stats = get_player_stats(years_back, "advanced")

    # Gets per 100 possesion player statistics
    pos_stats = get_player_stats(years_back, "per_poss")

    # Clean all the data and merge all 3 DataFrames into one
    return clean_data(team_stats, player_stats, mvp_stats, adv_stats, pos_stats)




'''
Returns the same dataframe of every NBA players stats using cvs files already saved from the function above. 
'''
def calculate_stats():
    mvp_stats = pd.read_csv('stats/mvp_stats_df.csv')
    player_stats = pd.read_csv('stats/all_years_player_stats.csv')
    team_stats = pd.read_csv('stats/teams_df.csv')
    advanced_stats = pd.read_csv('stats/adv_player_stats.csv')
    pos_stats= pd.read_csv('stats/pos_stats.csv')

    return clean_data(team_stats, player_stats, mvp_stats, advanced_stats, pos_stats)



''' 
Returns the dataframe of all the stats already saved.
'''
def get_stats():
    return pd.read_csv('stats/all_stats.csv')





stats = get_stats()


# Note: The data goes back 22 years but this only predicts the mvp for latest 21 seasons because there is no past data to train and make predictions on for the first year given

# Retrieves the mean error metric across all years, a list of the mean error metrics for each year, and a data frame of every player who was considered for the mvp race and there stats for every year.
mean_ap, aps, all_predictions = predictMVP(stats)

# Prints all the last 21 MVPs and their predicted rank by the algorithm
print(all_predictions[all_predictions["Rk"] < 2])


done = False
years = list(range(2002, 2024))

while not done:
    year = input("What year would you like to predict the MVP of?")
    try:
        year = int(year)

        if year not in years:
            print('Please give a year between 2002 to 2023')
        else:
            done = True
    except:
        print('Please give a year')




mvp_start = "The predicted MVP for the {} season is: ".format(year)

mvp = all_predictions.loc[(all_predictions['Year'] == year) & (all_predictions['Rk'] < 2)]['Player']

top_5_start = "The actual top 5 in the MVP race from this year is: "
top_5 = all_predictions[all_predictions['Year'] == year].sort_values('Rk').head(5)


print("{} {} \n {} \n {}".format(mvp_start, mvp, top_5_start, top_5))



