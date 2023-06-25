from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd



# Get players stats for the past 22 years

def get_player_stats(x, stat_type):

    calc_years = 2024 - x - 1

    years = list(range(calc_years, 2024))
    dfs = []


    for year in years:

        url = "https://www.basketball-reference.com/leagues/NBA_{}_{}.html".format(year, stat_type)
        html = urlopen(url)
        soup = BeautifulSoup(html)
        
        # use getText()to extract the text we need into a list
        headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]

        # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
        headers = headers[1:]
        
        # avoid the first header row
        rows = soup.findAll('tr')[1:]
        player_stats = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]
        
        stats_df = pd.DataFrame(player_stats, columns = headers)
        stats_df['Year'] = year
        dfs.append(stats_df)

    return pd.concat(dfs)