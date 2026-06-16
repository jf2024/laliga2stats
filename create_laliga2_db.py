import pandas as pd
import sqlite3

seasons = [2024, 2025]
categories = {
    'standings': 'laliga2_standings_{season}_cleaned.csv',
    'goalkeeping': 'laliga2_team_stats_goalkeeping_{season}_cleaned.csv',
    'offensive': 'laliga2_team_stats_offensive_{season}_cleaned.csv',
    'standard': 'laliga2_team_stats_standard_{season}_cleaned.csv'
}

all_dataframes = {}
unique_teams = set()

for table_name, file_pattern in categories.items():
    combined_data = []
    
    for season in seasons:
        file_path = file_pattern.format(season=season)
        df = pd.read_csv(file_path)
        
        df['season'] = season
        
        unique_teams.update(df['team'].unique())
        combined_data.append(df)
        
    all_dataframes[table_name] = pd.concat(combined_data, ignore_index=True)

# master id team list 
teams_list = sorted(list(unique_teams))
teams_df = pd.DataFrame({
    'team_id': range(1, len(teams_list) + 1),
    'team_name': teams_list
})

team_mapping = dict(zip(teams_df['team_name'], teams_df['team_id']))

# creating db
conn = sqlite3.connect('laliga2.db')
teams_df.to_sql('teams', conn, if_exists='replace', index=False)
print(f"loaded {len(teams_df)} rows into the new 'teams' table.")


for table_name, df in all_dataframes.items():
    
    df['team_id'] = df['team'].map(team_mapping)
    
    df = df.drop(columns=['team'])
    
    cols = ['season', 'team_id'] + [col for col in df.columns if col not in ['season', 'team_id']]
    df = df[cols]
    
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"loaded {len(df)} rows into the '{table_name}' table.")

conn.commit()
conn.close()

print("database created")
