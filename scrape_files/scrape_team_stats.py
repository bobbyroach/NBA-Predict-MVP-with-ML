from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd





def get_team_stats(x):

    calc_years = 2024 - x - 1

    years = list(range(calc_years, 2024))

    team_url = 'https://www.basketball-reference.com/leagues/NBA_{}_standings.html'


    # Grabs all the conference standings for each year and save the 
    # dataframes in the teams folder

    teams = []

    for year in years: 
        
        data = urlopen(team_url.format(year))
        soup = BeautifulSoup(data, 'html.parser')
        soup.find('tr', class_='thead').decompose()

        
        #Eastern conference    
        east_team_table = soup.find(id='all_divs_standings_E')
        team = pd.read_html(str(east_team_table))[0]
        team['Year'] = year 
        team['Team'] = team["Eastern Conference"]
        del team["Eastern Conference"]
        teams.append(team)
        
        
        #Western conference    
        west_team_table = soup.find(id='all_divs_standings_W')
        team = pd.read_html(str(west_team_table))[0]
        team['Year'] = year 
        team['Team'] = team["Western Conference"]
        del team["Western Conference"]

        teams.append(team)
        
    return pd.concat(teams)
