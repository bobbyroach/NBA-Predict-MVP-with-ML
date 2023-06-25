# NBA-Predict-MVP-with-ML

This project uses Python and the Scikit-Learn and Pandas Python libraries to predict the NBA MVP of a specified season based on every players regular season stats.

### Step 1: 

The first part of this project involves scraping for data. Here, the website NBA-Reference is used to gather the regular per game stats, advanced stats, and per 100 possesion stats of every NBA player. Additionally, it scrapes the MVP data, such as amount of MVP 'shares' every player won for a season, and all the team statistics for every year. It takes all these stats and puts them in individual Pandas Data Frames. 

### Step 2: 

The second part of this project deals with cleaning the data for machine learning. This involves filling null values in the data frame, manipulating every data frame so some of the columns are the same so they can be combined, and then merging every data frame into one. In the final data frame, each row represents one player for one year, meaning there can be and are multiple rows of the same NBA player but contain stats from different years in their career. This data frame ends up having around 40-45 columns, where 30-35 of them are individual statistics for that year and the rest are their team's statistics for that year. 


### Step 3: 


 
![Screenshot (48)](https://github.com/bobbyroach/NBA-Predict-MVP-with-ML/assets/110302904/fa253f8a-fb05-404c-ab12-c2bcfe459ec8)
