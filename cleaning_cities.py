import pandas as pd

df = pd.read_csv('csvs/uscities.csv')

# Renaming column names, named subdivision to include Canada cities
df = df.rename(columns={'state_id': 'subdivision_id', 'state_name': 'subdivision_name'})

# Define cities to keep from US
NBA_cities = [
    "Boston", "Brooklyn", "New York", "Philadelphia",
    "Chicago", "Cleveland", "Detroit", "Indianapolis", "Milwaukee",
    "Atlanta", "Charlotte", "Miami", "Orlando", "Washington",
    "Denver", "Minneapolis", "Oklahoma City", "Portland", "Salt Lake City",
    "San Francisco", "Los Angeles", "Phoenix", "Sacramento",
    "Dallas", "Houston", "Memphis", "New Orleans", "San Antonio",
    "Seattle"
]

# Keep only those cities
df = df[df['city'].isin(NBA_cities)]

# Columns to keep
tokeep = ['city', 'subdivision_id', 'subdivision_name', 'lat', 'lng']
df_new = df[tokeep]

# Save new dataframe to a new csv file
df_new.to_csv('csvs/nba_cities.csv', index=False)

# Adding Canadian NBA cities 
new_data = [
    {'city': 'Toronto', 'subdivision_id': 'ON', 'subdivision_name': 'Ontario', 'lat': '43.6532', 'lng': '-79.3832'},
    {'city': 'Vancouver','subdivision_id': 'BC', 'subdivision_name': 'British Columbia', 'lat': '49.2827', 'lng': '-123.1207'}
]

# Creating path and dataframe to add Canadian cities to new csv file
df_to_add = pd.DataFrame(new_data)
df_update = pd.concat([df_new, df_to_add], ignore_index=True)

# Define NBA cities to a team
team_names = {
    'Atlanta': ['Atlanta Hawks'],
    'Boston': ['Boston Celtics'],
    'Brooklyn': ['Brooklyn Nets', 'New Jersey Nets'],
    'Charlotte': ['Charlotte Hornets', 'Charlotte Bobcats'],
    'Chicago': ['Chicago Bulls'],
    'Cleveland': ['Cleveland Cavaliers'],
    'Dallas': ['Dallas Mavericks'],
    'Denver': ['Denver Nuggets'],
    'Detroit': ['Detroit Pistons'],
    'Houston': ['Houston Rockets'],
    'Indianapolis': ['Indiana Pacers'],
    'Los Angeles': ['Los Angeles Lakers', 'Los Angeles Clippers'],
    'Memphis': ['Memphis Grizzlies', 'Vancouver Grizzlies'],
    'Miami': ['Miami Heat'],
    'Milwaukee': ['Milwaukee Bucks'],
    'Minneapolis': ['Minnesota Timberwolves'],
    'New Orleans': ['New Orleans Pelicans', 'New Orleans Hornets'],
    'New York': ['New York Knicks'],
    'Oklahoma City': ['Oklahoma City Thunder'],
    'Orlando': ['Orlando Magic'],
    'Philadelphia': ['Philadelphia 76ers'],
    'Phoenix': ['Phoenix Suns'],
    'Portland': ['Portland Trail Blazers'],
    'Sacramento': ['Sacramento Kings', 'Kansas City Kings'],
    'Salt Lake City': ['Utah Jazz'],
    'San Antonio': ['San Antonio Spurs'],
    'San Francisco': ['Golden State Warriors'],
    'Seattle': ['Seattle SuperSonics'],
    'Toronto': ['Toronto Raptors'],
    'Washington': ['Washington Wizards', 'Washington Bullets']
}

# Expand each city into one row per team
expanded_rows = []

for _, row in df_update.iterrows():
    city = row['city']
    teams = team_names.get(city, [])
    for team in teams:
        new_row = row.copy()
        new_row['nba_team'] = team
        expanded_rows.append(new_row)

# Final dataframe with NBA team names
df_final = pd.DataFrame(expanded_rows)
df_final.to_csv('csvs/nba_cities.csv', index=False)