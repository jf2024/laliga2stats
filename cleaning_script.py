import pandas as pd

seasons = [2024, 2025]

# standings section
for season in seasons:
    standings_df = pd.read_csv(f'laliga2_standings_{season}.csv')

    standings_df[['total_W', 'total_D', 'total_L']] = standings_df['W-D-L'].str.split('-', expand=True).astype(int)
    standings_df[['wins_home', 'draws_home', 'losses_home']] = standings_df['HOME'].str.split('-', expand=True).astype(int)
    standings_df[['wins_away', 'draws_away', 'losses_away']] = standings_df['AWAY'].str.split('-', expand=True).astype(int)

    standings_df.drop(columns=['W-D-L', 'HOME', 'AWAY'], inplace=True)

    standings_df.rename(columns={
        'CLUBS': 'team', 
        'POSITION': 'position', 
        'MP': 'matches_played',
        'PTS': 'points', 
        'GF': 'goals_for', 
        'GA': 'goals_against',
        'GD': 'goals_difference'
    }, inplace=True)

    standings_df.to_csv(f'laliga2_standings_{season}_cleaned.csv', index=False)

for season in seasons:
    # goalkeeper section
    gk = pd.read_csv(f'laliga2_team_stats_goalkeeping_{season}.csv')

    gk.rename(columns={
        'TEAMS': 'team', 'POSITION': 'position', 'GP': 'matches_played',
        'GA': 'goals_against', 'S': 'shots', 'GD': 'goals_difference',
        'SOG': 'shots_on_goal', 'SV': 'saves', 'CS': 'clean_sheets'
    }, inplace=True)

    gk.drop(columns=['CLR'], errors='ignore', inplace=True) #dont need this column, all of it are 0s
    gk.to_csv(f'laliga2_team_stats_goalkeeping_{season}_cleaned.csv', index=False)

    # offensive section
    off = pd.read_csv(f'laliga2_team_stats_offensive_{season}.csv')
    off.rename(columns={
        'TEAMS': 'team', 'POSITION': 'position', 'GP': 'matches_played',
        'S': 'shots', 'SOG': 'shots_on_goal', 'SOP': 'shots_on_posts',
        'SOFF': 'shots_off_target', 'SAB': 'shot_attempts_blocked',
        'POSS': 'possession_time_min_avg', 'CK': 'corner_kicks', 'OFF': 'offsides'
    }, inplace=True)

    off.to_csv(f'laliga2_team_stats_offensive_{season}_cleaned.csv', index=False)

    # standard section
    standard = pd.read_csv(f'laliga2_team_stats_standard_{season}.csv')
    standard.rename(columns={
        'TEAMS': 'team', 'POSITION': 'position', 'GP': 'matches_played',
        'GF': 'goals_for', 'KG': 'kicked_goals', 'HG': 'header_goals',
        '1G': 'first_half_goals', '2G': 'second_half_goals', 'GA': 'goals_against',
        '1GC': 'goals_against_first_half', '2GC': 'goals_against_second_half',
        'A': 'assists', 'YC': 'yellow_cards', 'RC': 'red_cards'
    }, inplace=True)

    standard.drop(columns=['YRC'], errors='ignore', inplace=True) #dont need this column 
    standard.to_csv(f'laliga2_team_stats_standard_{season}_cleaned.csv', index=False)