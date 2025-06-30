import csv
import sqlite3

# Filenames
lottery_csv = "csvs/lottery_data.csv"
cities_csv = "csvs/nba_cities.csv"
num_lottery_picks_csv = "csvs/num_lottery_picks.csv"
top3_csv = "csvs/top3_probability_results.csv"
unlikely_firsts_csv = "csvs/top10_unlikely_first.csv"
most_firsts_csv = "csvs/most_firsts.csv"

# Connecting to database
conn = sqlite3.connect("nba_data.db")
cursor = conn.cursor()

# Creating tables from csv files and dropping if updating
cursor.execute("DROP TABLE IF EXISTS lottery_data")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS lottery_data (
        draft TEXT,
        pick INTEGER,
        team TEXT,
        record TEXT,
        odds TEXT,
        chances INT,
        prelottery_position TEXT,
        pick_change TEXT,
        player_taken TEXT,
        draft_team TEXT,
        PRIMARY KEY (draft, pick)
    )
''')
conn.commit()

cursor.execute("DROP TABLE IF EXISTS nba_cities")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS nba_cities (
        city TEXT,
        subdivision_id TEXT,
        subdivision_name TEXT,
        lat REAL,
        lng REAL,
        nba_team TEXT,
        PRIMARY KEY (nba_team)
    )
''')
conn.commit()

cursor.execute("DROP TABLE IF EXISTS num_lottery_picks")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS num_lottery_picks (
        franchise TEXT,
        number_of_picks INT,
        PRIMARY KEY (franchise)
    )
''')
conn.commit()

cursor.execute("DROP TABLE IF EXISTS top3_probability_results")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS top3_probability_results (
        draft TEXT,
        top3_probability_percent REAL,
        team1 TEXT,
        team2 TEXT,
        team3 TEXT,
        PRIMARY KEY (draft)
    )
''')
conn.commit()

cursor.execute("DROP TABLE IF EXISTS top10_unlikely_first")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS top10_unlikely_first (
        draft TEXT,
        draft_team TEXT,
        odds_real REAL,
        player_taken TEXT,
        prelottery_position TEXT,
        record TEXT,
        PRIMARY KEY (draft)
    )
''')
conn.commit()

cursor.execute("DROP TABLE IF EXISTS most_firsts")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS most_firsts (
        franchise TEXT,
        first_pick_count INT,
        PRIMARY KEY (franchise)
    )
''')
conn.commit()

# Inserting data into database tables
with open(lottery_csv, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute('''
            INSERT INTO lottery_data
            (draft, pick, team, record, odds, chances, prelottery_position, pick_change, player_taken, draft_team)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['Draft'],
            int(row['Pick']),
            row['Team'],
            row['Record'],
            row['Odds'],
            int(row['Chances']),
            row['Pre-Lottery Position'],
            row['Pick Change'],
            row['Player Taken'],
            row['Draft Team']            
        ))

with open(cities_csv, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute('''
            INSERT INTO nba_cities
            (city, subdivision_id, subdivision_name, lat, lng, nba_team)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            row['city'],
            row['subdivision_id'],
            row['subdivision_name'],
            float(row['lat']),
            float(row['lng']),
            row['nba_team']           
        ))

with open(num_lottery_picks_csv, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute('''
            INSERT INTO num_lottery_picks
            (franchise, number_of_picks)
            VALUES (?, ?)
        ''', (
            row['franchise'],
            int(row['number_of_picks'])       
        ))

with open(top3_csv, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute('''
            INSERT INTO top3_probability_results
            (draft, top3_probability_percent, team1, team2, team3)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            row['draft'],
            float(row['top3_probability_percent']),
            row['team1'],
            row['team2'],
            row['team3']      
        ))

with open(unlikely_firsts_csv, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute('''
            INSERT INTO top10_unlikely_first
            (draft, draft_team, odds_real, player_taken, prelottery_position, record)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            row['draft'],
            row['draft_team'],
            float(row['odds_real']),
            row['player_taken'],
            row['prelottery_position'],
            row['record']   
        ))

with open(most_firsts_csv, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute('''
            INSERT INTO most_firsts
            (franchise, first_pick_count)
            VALUES (?, ?)
        ''', (
            row['franchise'],
            int(row['first_pick_count'])       
        ))

conn.commit()
conn.close()
print("CSV Data Successfully Imported")
