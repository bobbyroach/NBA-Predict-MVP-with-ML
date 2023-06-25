from urllib.request import urlopen
import pandas as pd 
from bs4 import BeautifulSoup


'''' 
Web Scrapes NBA mvp players' stats for the last 10 years and returns a pandas DataFrame.
'''
def get_mvp_stats(givenYear):

    calcYear = 2024 - givenYear - 1

    years = list(range(calcYear , 2024))
    url_start = "https://www.basketball-reference.com/awards/awards_{}.html"
    dfs = []


    for year in years:
        url = url_start.format(year)
        
        data = urlopen(url)
        
        soup = BeautifulSoup(data, 'html.parser')
        soup.find('tr', class_="over_header").decompose()
        mvp_table = soup.find_all(id="mvp")[0]
        mvp_df = pd.read_html(str(mvp_table))[0]
        mvp_df["Year"] = year
        dfs.append(mvp_df)

    return pd.concat(dfs)