import pandas as pd 


def clean_data(team_stats, player_stats, mvp_stats, adv_stats, pos_stats):

    players = get_player_data(player_stats)
    adv_players = get_player_data(adv_stats)
    pos_players = get_player_data(pos_stats)
    mvps = get_mvp_data(mvp_stats)
    
    del adv_players['Tm']
    del pos_players['Tm']


    # Merge on player and year - combine them
    # outer merge - keep data that isn't found in both data frames
    combined = players.merge(mvps, how='outer', on=["Player", "Year"])
    combined = combined.merge(adv_players, how='outer', on=["Player", "Year"])
    combined = combined.merge(pos_players, how='outer', on=["Player", "Year"])


    # Fill NaN values with 0
    combined[['Pts Won', 'Pts Max', 'Share']] = combined[['Pts Won', 'Pts Max', 'Share']].fillna(0)

    # Get rid of null rows that don't have a position and other stats
    combined = combined[combined.Pos.notna()]

    # Turn 'Year' column into integers
    combined["Year"].astype(int)



    teams = get_team_data(team_stats)

    # Teams have full team names, players have abbr team names
    # Create dictionary to map names to abbreviations
    nicknames = {}
    noh_nicknames = {}
    charbob_nicknames = {}

    with open('names/nicknames.csv', encoding='utf-8') as f: 
        lines = f.readlines()
        
        # Read every line, skip first row
        for line in lines[1:]: 
            
            # Each line = "ATL, Atlanta Hawks\n"
            abbrev, name = line.replace('\n', '').split(",")
            nicknames[abbrev] = name
            
            
    with open('names/noh_nicknames.csv', encoding='utf-8') as f: 
        lines = f.readlines()
        for line in lines[1:]: 
            abbrev, name = line.replace('\n', '').split(",")
            noh_nicknames[abbrev] = name
            
    with open('names/charbob_nicknames.csv', encoding='utf-8') as f: 
        lines = f.readlines()
        for line in lines[1:]: 
            abbrev, name = line.replace('\n', '').split(",")
            charbob_nicknames[abbrev] = name




    # Need to use different dictionaries to map to different
    # parts of the combined dataframe due to faulty data involving 
    # the New Orleans Hornets (2012-2013 and earlier) and the Charlotte
    # Bobcats (2013-2014) and earlier

    dfs =[]

    temp_all = combined.loc[combined.Year <= 2013].copy()
    temp_noh = combined.loc[combined.Year == 2014].copy()
    temp_chb = combined.loc[combined.Year >= 2015].copy()

    temp_all['Team'] = temp_all['Tm'].map(nicknames)
    temp_noh['Team'] = temp_noh['Tm'].map(noh_nicknames)
    temp_chb['Team'] = temp_chb['Tm'].map(charbob_nicknames)
    dfs.append(temp_all)
    dfs.append(temp_noh)
    dfs.append(temp_chb)

    combined = pd.concat(dfs)

    # Finally, combine all three original DataFrames
    stats = combined.merge(teams, how='outer', on=['Team', 'Year'])
    # Try to convert all values to numeric, ignore on errors
    stats = stats.apply(pd.to_numeric, errors='ignore')

    # Replace dashes with zeroes in games back and make numeric
    stats["GB"] = stats["GB"].str.replace('—', '0')
    stats["GB"] = pd.to_numeric(stats["GB"])

    stats = stats[~stats.Pos.isnull()]

    return stats

















'''
Gets the team_stats DataFrame, cleans the data for machine learning, and returns it.
'''
def get_team_data(teams):
    del teams['Unnamed: 0']

    # Get rid of Unnamed column and astericks in team name column
    teams['Team'] = teams["Team"].str.replace('*', '', regex=False)

    # Gets rid of rows displaying divisions
    teams = teams[~teams["W"].str.contains("Division")].copy()  

    return teams











'''
Gets the player_stats DataFrame, cleans the data for machine learning, and returns it.
'''
def get_player_data(players):

    del players['Unnamed: 0']

    # Get rid of astericks 
    players['Player'] = players['Player'].str.replace('*','', regex=False)



    # Some players played on multiple teams in the same year and 
    # have multiple rows 
    # Group by player and year
    players.groupby(['Player', 'Year'])

    def single_team(df):
        if df.shape[0]==1:
            return df
        else:
            row = df[df["Tm"]=="TOT"]
            row["Tm"] = df.iloc[-1,:]["Tm"]
            return row

    players = players.groupby(["Player", "Year"]).apply(single_team)

    # Remove new extroneous columns on the left
    players.index = players.index.droplevel()
    players.index = players.index.droplevel()

    return players





'''
Gets the mvp_stats DataFrame, cleans the data for machine learning, and returns it.
'''
def get_mvp_data(mvps):
    mvps = mvps[['Player', 'Year', 'Pts Won', 'Pts Max', 'Share']]
    return mvps