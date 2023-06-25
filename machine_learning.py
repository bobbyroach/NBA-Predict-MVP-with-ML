import pandas as pd
from sklearn.svm import SVR


years = list(range(2001, 2024))





'''
This method takes in the statistics dataframe, creates a list of predictors for the machine learning algorithm, and then uses a support vector regression model to predict the number of MVP 'Shares' a player will earn based on their regular season stats. This regression model uses the data of prior years to predict the MVP for the current year it is calculating. 
'''
def predictMVP(stats):
    del stats['Unnamed: 0']
    stats = stats.fillna(0)


    predictors = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
       '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB','DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PER', 'TS%', 'USG%', 'OWS', 'DWS', 'WS','WS/48', 'OBPM','DBPM', 'BPM', 'VORP', 'ORtg','DRtg','Year','W', 'L', 'W/L%', 'GB', 'PS/G','PA/G', 'SRS']


    def calc_win_contr(row):
        return row['LOI'] * row['QOI']

    def calc_net_rating(row):
        return row['ORtg'] - row['DRtg']

    def calc_qoi(row):
        return 0.4 * (row['VORP'] + row['WS']) + 0.2 * row['NR']
        
    def calc_loi(row):
        return row["W"] * (row["G"]/82) * (row["MP"]/48) * (row["USG%"]/100)

    # LOI -> Level of Impact
    col = stats.apply(lambda row: calc_loi(row), axis=1)
    stats = stats.assign(LOI=col.values)

    # NR -> Net Rating, +/-
    col = stats.apply(lambda row: calc_net_rating(row), axis=1)
    stats = stats.assign(NR=col.values)

    # QOI -> Quality of Impact
    col = stats.apply(lambda row: calc_qoi(row), axis=1)
    stats = stats.assign(QOI=col.values)

    # WC -> Win Contribution
    col = stats.apply(lambda row: calc_win_contr(row), axis=1)
    stats = stats.assign(WC=col.values)

    predictors += ["NR", "LOI", "QOI", "WC"]





    svr = SVR()
    
    # Run support vector regression model to calculate predicted mvp "shares" a player will win given their regular season stats
    svr.fit(stats[predictors], stats['Share'])

    mean_ap, aps, all_predictions = backtest(stats, svr, years[1:], predictors)


    # Delete some shared columns to prevent errors
    del all_predictions['Share']
    del all_predictions['predictions']
    del all_predictions['Diff']

    # Combine calculated mvp data frame with originial player statistics data frame
    stats = stats.merge(all_predictions, how='outer', on=['Player', 'Year'])
    stats = stats.fillna(500)

    # Calculates amount of MVPs a player has won in their career up until that year, see method description for more on why
    stats = addMVPCount(stats)

    # Adding this mvp count to the list of predictors for machine learning
    predictors += ['mvps']

    # Rerun the svr algorithm
    svr = SVR()
    svr.fit(stats[predictors], stats['Share'])
    mean_ap, aps, all_predictions = backtest(stats, svr, years[1:], predictors)


    return mean_ap, aps, all_predictions





'''
Takes in all stats, calculates the amount of MVPs a player has won in their career up until that year.
This statistic is then added to the list of predictors for machine learning. When a player has won multiple MVPs, especially when they are won consecutively, their chances of winning more decrease due to a phenemenon called voters' fatigue. When two MVP candidates, one who has multiple MVP titles already and one who is relatively new to the process, are generally even in the race, voters will often lean towards voting for the newer player. 
'''
def addMVPCount(stats):

    stats['mvps'] = 0
    mvp_dict = {}

    def calc_mvps(row):
        player = row['Player']
        if row['Rk'] == 1:
            if player in mvp_dict:
                mvp_dict[player] += 1
                row['mvps'] = mvp_dict.get(player)
            else:
                mvp_dict[player] = 1
                row['mvps'] = mvp_dict.get(player)
        return row['mvps']

    col = stats.apply(lambda row: calc_mvps(row), axis=1) 
    stats = stats.assign(mvps = col.values)

    return stats



'''
Calculates the mean error metric across all years, a list of the mean error metrics for each year, and a data frame of every player who was considered for the mvp race and there stats for every year.
'''
def backtest(stats, model, years, predictors):
    aps = []
    all_predictions = []
    for year in years:
        train = stats[stats["Year"] < year]
        test = stats[stats["Year"] == year]
        model.fit(train[predictors],train["Share"])
        predictions = model.predict(test[predictors])
        predictions = pd.DataFrame(predictions, columns=["predictions"], index=test.index)
        combination = pd.concat([test[["Player", "Share"]], predictions], axis=1)
        combination['Year'] = 0
        combination = add_ranks(combination, year)
        all_predictions.append(combination)
        aps.append(find_ap(combination))
        
    all_pred = pd.concat(all_predictions)

    return sum(aps) / len(aps), aps, all_pred



''' 
Adds useful columns such as rank, predicted rank, and year to mvp prediction data frames.
'''
def add_ranks(combination, year):
    # Sorting by actual share, adding rank
    combination = combination.sort_values('Share', ascending=False)
    combination['Rk'] = list(range(1, combination.shape[0]+1))
    
    # Sorting by predicted rank
    combination = combination.sort_values('predictions', ascending=False)
    combination["Predicted_Rk"] = list(range(1, combination.shape[0] + 1))
    
    # Different between ranks
    combination['Diff'] = combination["Rk"] - combination['Predicted_Rk']
    
    combination["Year"] = year
    
    return combination


''' 
Calculates the error metric for mvp predictions for one year.
'''
def find_ap(combination):
    actual = combination.sort_values("Share", ascending=False).head(5)
    predicted = combination.sort_values("predictions", ascending=False)
    ps = []
    found = 0
    seen = 1
    for index,row in predicted.iterrows():
        if row["Player"] in actual["Player"].values:
            found += 1
            ps.append(found / seen)
        seen += 1

    #Error metric
    return sum(ps) / len(ps)