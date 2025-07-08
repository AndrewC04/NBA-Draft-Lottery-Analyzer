# NBA Draft Luck Analyzer

* [Tableau viz](https://public.tableau.com/app/profile/andrew.chau1438/viz/NBADraftLuckAnalyzer/NBADraftLuckAnalyzer)
* [HTML version link to download](https://github.com/AndrewC04/NBA-Draft-Luck-Analyzer/blob/main/draft_analyzer/tableau/draftlotteryanalyzer.html)
* [Link to full screenshots of all Tableau pages](https://github.com/AndrewC04/NBA-Draft-Luck-Analyzer/tree/main/draft_analyzer/tableau/screenshots)

## Table Of Contents
* [Project Overview](#project-overview)
* [Tableau Dashboards](#tableau-dashboards)
* [Jupyter Notebook SQL Queries](#jupyter-notebook-sql-queries)
* [Technologies](#technologies)
* [Data Sources](#data-sources)
* [Inspiration](#inspiration)

## Project Overview
This project provides data driven exploration of the NBA draft lottery using Python for data extraction and transformation, SQL for querying and analyzing draft data, and Tableau for rich, interactive visualizations. The visualizations aim to analyze "luck" in the draft process and its impact on franchises and the league as a whole.

## Tableau Dashboards
Each visualization explores a different aspect of draft lottery history, with historical data from its inception to today:
1. [Draft Lottery Page](https://github.com/AndrewC04/NBA-Draft-Luck-Analyzer/tree/main/draft_analyzer/tableau/screenshots/Draft_Lottery_Page)
    1. A comprehensive background of the NBA draft lottery's purpose and modifications over the years.
    2. Draft lottery visualization by odds descending.

<img width="829" height="520" alt="Image" src="https://github.com/user-attachments/assets/7315693d-4a90-42b6-8e93-47daf803a4c0" />

2. [Draft Results Page](https://github.com/AndrewC04/NBA-Draft-Luck-Analyzer/tree/main/draft_analyzer/tableau/screenshots/Draft_Results_Page)
    1. Notable year points in draft lottery history. 
    2. Table of players taken in the draft lottery. 
    3. Visualizations for draft order outcome by odds and shifts.

<img width="832" height="533" alt="Image" src="https://github.com/user-attachments/assets/95223d99-4ed4-4b7d-8313-fe51e0047120" />

3. [Team History Page](https://github.com/AndrewC04/NBA-Draft-Luck-Analyzer/tree/main/draft_analyzer/tableau/screenshots/Team_History_Page)
    1. Net shift visualization for pick change in draft lottery history.
    2. Interactive map with table and stats of a team's draft pick history, dynamic to team selection on map. 

<img width="830" height="528" alt="Image" src="https://github.com/user-attachments/assets/56517716-8343-446a-b0b3-d4283f01c436" />

4. [Pick Movement Page](https://github.com/AndrewC04/NBA-Draft-Luck-Analyzer/tree/main/draft_analyzer/tableau/screenshots/Pick_Movement_Page)
    1. Shift trend comparisons of the two recent eras in draft lottery history for every lottery position. 
    2. Holistic view of every pick in draft lottery history by its original lottery position vs actual pick outcome. 

<img width="828" height="528" alt="Image" src="https://github.com/user-attachments/assets/1828a446-04a7-41d3-9840-e21aefff9388" />

5. [Draft Analysis Page](https://github.com/AndrewC04/NBA-Draft-Luck-Analyzer/tree/main/draft_analyzer/tableau/screenshots/Draft_Analysis_Page)
    1. Visualizations of all top 3 outcomes in draft lottery history by unlikeliness, average shift for every pick position by era, and least likely first overall picks.
    2. Insights to how the latest changes to the draft lottery have affected the way teams work around worse chance probabilities.

<img width="831" height="530" alt="Image" src="https://github.com/user-attachments/assets/c7106335-e456-420e-a8b0-547ac8d12627" />

## Jupyter Notebook SQL Queries
In this project, several key SQL queries were executed to analyze draft lottery data. Below is a query that calculates the probability of a draft's top 3 outcome based on the combination chances of the corresponding draft. This query gives a clearer understanding of how lottery outcome trends are concurrent with the changes made to the lottery system over time, including outlier outcomes.

```
query2 = """
        WITH top3 AS (
          SELECT draft, pick, CAST(REPLACE(chances, '%', '') AS REAL) AS chances, draft_team
          FROM lottery_data
          WHERE pick IN (1, 2, 3)
        ),

        total_combinations AS (
          SELECT draft, SUM(CAST(REPLACE(chances, '%', '') AS REAL)) AS total_combinations
          FROM lottery_data
          GROUP BY draft
        ),

        pivot_columns AS (
          SELECT t.draft,
          tc.total_combinations,
          MAX(CASE WHEN t.pick = 1 THEN t.chances END) AS c1,
          MAX(CASE WHEN t.pick = 2 THEN t.chances END) AS c2,
          MAX(CASE WHEN t.pick = 3 THEN t.chances END) AS c3,
          MAX(CASE WHEN t.pick = 1 THEN t.draft_team END) AS team1,
          MAX(CASE WHEN t.pick = 2 THEN t.draft_team END) AS team2,
          MAX(CASE WHEN t.pick = 3 THEN t.draft_team END) AS team3  
          FROM top3 t
          JOIN total_combinations tc 
          ON t.draft = tc.draft
          GROUP BY t.draft, tc.total_combinations
        ),

        probabilities AS (
          SELECT draft, 
            ROUND(
              1.0 * c1 / total_combinations *
              c2 / (total_combinations - c1) *
              c3 / (total_combinations - c1 - c2) * 100,
              3
            ) AS top3_probability_percent,
            team1, team2, team3
          FROM pivot_columns
        )

        SELECT * FROM probabilities
        ORDER BY draft DESC;
"""

df2 = pd.read_sql_query(query2, conn)
df2.to_csv("data/top3_probability_results.csv", index=False)
pd.set_option('display.max_rows', None)
print(df2)
```

View the rest of the queries in the `notebook/queries.ipynb` [file](https://github.com/AndrewC04/NBA-Draft-Luck-Analyzer/tree/main/draft_analyzer/notebook/queries.ipynb). 

## Technologies
This project utilizes the following stack:
* Python 
    * Selenium
    * WebDriverManager
    * BeautifulSoup
    * Pandas
* SQLite3
* Jupyter Notebook
* Tableau

## Data Sources
* [RealGM](https://basketball.realgm.com/nba/draft/lottery_results/)
* [Simplemaps](https://simplemaps.com/data/us-cities)
* [Kaggle](https://www.kaggle.com/datasets/wyattowalsh/basketball)

## Inspiration
Inspired by [Wesley Morton's Peachtree Hoops article](https://www.peachtreehoops.com/2020/8/19/21353534/nba-draft-lottery-2020-lucky-history-atlanta-hawks-odds-math-results-protocol-probability) and [JR Copreros' Tableau viz](https://public.tableau.com/app/profile/jrcopreros/viz/TheGlobalizationoftheNBA_IV2023/Final).