import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="La Liga 2 Analytics Dashboard", layout="wide")

@st.cache_data
def load_data():
    conn = sqlite3.connect('laliga2.db')
    
    teams = pd.read_sql("SELECT * FROM teams", conn)
    standings = pd.read_sql("SELECT * FROM standings", conn)
    offensive = pd.read_sql("SELECT * FROM offensive", conn)
    gk = pd.read_sql("SELECT * FROM goalkeeping", conn)
    standard = pd.read_sql("SELECT * FROM standard", conn)
    conn.close()
    
    master = pd.merge(teams, standings, on='team_id')
    master = pd.merge(master, offensive, on=['team_id', 'season'], how='left')
    master = pd.merge(master, gk, on=['team_id', 'season'], how='left')
    master = pd.merge(master, standard, on=['team_id', 'season'], how='left')
    
    return master

df = load_data()

# sidebar
st.sidebar.title("La Liga 2 Explorer")
st.sidebar.markdown(
    "Welcome to the interactive La Liga 2 dashboard. "
    "Use the controls below to filter the data and explore team performance."
)

#filtering
available_seasons = sorted(df['season'].unique(), reverse=True)
selected_season = st.sidebar.selectbox("Select Season", available_seasons)
season_df = df[df['season'] == selected_season]

team_list = sorted(season_df['team_name'].unique())
selected_team = st.sidebar.selectbox("Highlight Team (For Explorer Tab)", team_list)

compare_teams = st.sidebar.multiselect(
    "Compare Teams (For Comparison Tab)",
    team_list,
    default=[selected_team] if selected_team in team_list else team_list[:2]
)

st.sidebar.markdown("---")

st.title(f"La Liga 2 Season Overview ({selected_season})")

team_data = season_df[season_df['team_name'] == selected_team].iloc[0]
st.markdown(f"### Highlighted Team: {selected_team}")
m1, m2, m3, m4 = st.columns(4)
m1.metric("League Position", team_data['position'])
m2.metric("Total Points", team_data['points'])
m3.metric("Goal Difference", team_data['goals_difference'])
m4.metric("Win Percentage", f"{round((team_data['total_W'] / team_data['matches_played']) * 100, 1)}%")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "League Trends (Macro)", 
    "Team Explorer (Micro)", 
    "Team Comparison", 
    "Raw Data"
])

# league trends window
with tab1:
    st.markdown("### Playstyle vs. Success")
    st.write("Does having more possession or taking more shots actually translate to points on the board?")
    
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox(
            "Select X-Axis Metric", 
            ['possession_time_min_avg', 'shots', 'shots_on_goal', 'corner_kicks', 'yellow_cards']
        )
    with col2:
        y_axis = st.selectbox(
            "Select Y-Axis Metric", 
            ['points', 'goals_for', 'goals_against', 'clean_sheets']
        )
    
    fig1 = px.scatter(
        season_df, 
        x=x_axis, 
        y=y_axis, 
        text='team_name',
        size='points',
        color='goals_difference', 
        color_continuous_scale='RdYlGn',
        title=f"{y_axis.replace('_', ' ').title()} vs {x_axis.replace('_', ' ').title()}"
    )
    fig1.update_traces(textposition='top center')
    fig1.update_layout(height=600) 
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    st.markdown("### Goalkeeping Efficiency")
    fig2 = px.bar(
        season_df.sort_values('clean_sheets', ascending=True), 
        x='clean_sheets', 
        y='team_name', 
        orientation='h',
        color='saves',
        title="Clean Sheets by Team (Colored by Total Saves)"
    )
    st.plotly_chart(fig2, use_container_width=True)

# team explorer window
with tab2:
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### Home vs. Away Results")
        venue_data = pd.DataFrame({
            'Result': ['Wins', 'Draws', 'Losses', 'Wins', 'Draws', 'Losses'],
            'Venue': ['Home', 'Home', 'Home', 'Away', 'Away', 'Away'],
            'Count': [
                team_data['wins_home'], team_data['draws_home'], team_data['losses_home'],
                team_data['wins_away'], team_data['draws_away'], team_data['losses_away']
            ]
        })
        
        fig3 = px.bar(
            venue_data, 
            x='Result', 
            y='Count', 
            color='Venue', 
            barmode='group',
            color_discrete_map={'Home': '#1f77b4', 'Away': '#ff7f0e'},
            title=f"{selected_team} Venue Performance"
        )
        st.plotly_chart(fig3, use_container_width=True)
        
    with col4:
        st.markdown("#### Offensive Production Breakdown")
        goal_types = pd.DataFrame({
            'Goal Type': ['Kicked Goals', 'Header Goals'],
            'Total': [team_data['kicked_goals'], team_data['header_goals']]
        })
        
        fig4 = px.pie(
            goal_types, 
            values='Total', 
            names='Goal Type', 
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Teal,
            title=f"{selected_team} Goal Sources"
        )
        fig4.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig4, use_container_width=True)

# team comparsion window
with tab3:
    st.markdown("### Head-to-Head Comparison")
    
    if len(compare_teams) < 2:
        st.info("Select at least two teams in the sidebar to compare.")
    else:
        compare_df = season_df[season_df["team_name"].isin(compare_teams)].copy()
        compare_long = compare_df.melt(
            id_vars="team_name",
            value_vars=["points", "goals_for", "goals_against", "goals_difference", "total_W", "total_D", "total_L"],
            var_name="metric",
            value_name="value"
        )

        fig5 = px.bar(
            compare_long,
            x="metric",
            y="value",
            color="team_name",
            barmode="group",
            title="Selected Teams Across Key Metrics"
        )
        fig5.update_layout(xaxis_title="Metric", yaxis_title="Value")
        st.plotly_chart(fig5, use_container_width=True)

        st.markdown("#### Comparison Data Table")
        st.dataframe(
            compare_df[["team_name", "position", "points", "goals_for", "goals_against", "goals_difference", "total_W", "total_D", "total_L"]].sort_values('points', ascending=False),
            use_container_width=True
        )

with tab4:
    st.markdown("### Comprehensive League Data")
    st.write("Browse the full stats for the teams.")
    
    display_cols = ['position', 'team_name'] + [col for col in season_df.columns if col not in ['position', 'team_name', 'team_id', 'season']]
    
    st.dataframe(
        season_df[display_cols].sort_values('points', ascending=False), 
        use_container_width=True,
        hide_index=True
    )