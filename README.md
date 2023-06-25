# NBA-Predict-MVP-with-ML

This project uses Python and the Scikit-Learn and Pandas Python libraries to predict the NBA MVP of a specified season based on every players regular season stats.

### Step 1: 

The first part of this project involves scraping for data. Here, the website NBA-Reference is used to gather the regular per game stats, advanced stats, and per 100 possesion stats of every NBA player. Additionally, it scrapes the MVP data, such as amount of MVP 'shares' every player won for a season, and all the team statistics for every year. It takes all these stats and puts them in individual Pandas Data Frames. 

### Step 2: 

The second part of this project deals with cleaning the data for machine learning. This involves filling null values in the data frame, manipulating every data frame so some of the columns are the same so they can be combined, and then merging every data frame into one. In the final data frame, each row represents one player for one year, meaning there can be and are multiple rows of the same NBA player but contain stats from different years in their career. This data frame ends up having around 40-45 columns, where 30-35 of them are individual statistics for that year and the rest are their team's statistics for that year. 


### Step 3: 

In this step, the machine learning library, Scikit-Learn, is used to predict the MVP 'shares' every player will win in each season based on their regular season statistics. After trying a few different machine learning algorithms, I found that the support vector regression model was the most accurate. Here are the steps I took to calculate and predict the MVPs of each season:

1) First, I made sure there are no null or extraneous values in the data frame
2) Created a list of predictors. These predictors are the stats the machine learning algorithm will train on and make predictions based on, and they should all be names of columns in the main data frame with all the statistics
3) Using existing stats in the data frame, I created new stats, such as net rating, quality of impact, level of impact, and win contribution, which I then added to the list of predictors. Here is how I calculated those stats:

          - NR: Offensive Rating (ORtg) - Defensive Rating (DRtg)

          - QOI: (Value over replacement player (VORP) + Win share (WS)) * 0.4 + Net Rating (NR) * 0.2

          - LOI: Team Wins * (Games played / 82) * (Minutes played / 48) * (Usage rate / 100)

          - WC: Level of impact (LOI) * Quality of impact (QOI)

4) Then, I created an instance of the support vector regression model and fit it to the predictors and the value I was trying to calculate, MVP shares
5) Taking in the regression model, the stats data frame, the amount of years I was calculating from, and the list of predictors, I created a function that calculates the number of shares every player will earn in every year in the total amount of years. The basic structure of the function is as follows:

          - For loop that runs through every year in the years passed in

          - For every iteration, we train on the years of data less than the current year, and test and predict on the current year's data

          - We create a list of predictions using the model's predict method on the test data and turn that list into pandas data frame and concat that with a data frame of the players and their share value

          - Then, we add columns such as a player's rank and predicted rank and concatenate every year's prediction data frame together to end up with our final data frame


Here is a screenshot of the output when listing the actual MVPs for the last 21 years:
 
![Screenshot (48)](https://github.com/bobbyroach/NBA-Predict-MVP-with-ML/assets/110302904/fa253f8a-fb05-404c-ab12-c2bcfe459ec8)

As you can see, it lists every player that recieved a rank of 1, meaning they had the most actual MVP shares that season, the year they won it in, their predicted rank, and the difference between their actual rank and the rank the algorithm predicted for them. 

## Conclusion

Overall, this algorithm was able to predict the past 15/21 MVPs correctly. Unfortunately, since the MVP voting isn't run by a machine learning algorithm, and is determined by voters, each year's MVP is not going to be selected based on the same statistics that the last was. On some of the years the algorithm was wrong, you could always make the argument that that player should have won, based on their stats for that year and the stats that past MVP players had. 

For example, in 200
