import streamlit as st
import pandas as pd
import json
from mplsoccer import VerticalPitch
from matplotlib.patches import Patch


st.title("Euros 2024 Shot Map")
st.subheader("Select teams, players, and shot outcomes to visualize the shot map for comparison. \n To compare select 2 players")

# Load the data
df = pd.read_csv('euros_2024_shot_map.csv')
df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)

# Sidebar for first player selection
st.sidebar.header("First Player - (Shown by blue)")
team1 = st.sidebar.selectbox('Select first team', ['All'] + list(df['team'].sort_values().unique()), key="team1")
player1 = st.sidebar.selectbox('Select first player', ['All'] + list(df[df['team'] == team1]['player'].sort_values().unique()) if team1 != 'All' else ['All'], key="player1")
shot_outcome1 = st.sidebar.selectbox("First player's shot outcome", ['All'] + list(df[df['player'] == player1]['shot_outcome'].unique()) if player1 != 'All' else ['All'], key="outcome1")

# Sidebar for second player selection
st.sidebar.header("Second Player - (Shown by red)")
team2 = st.sidebar.selectbox('Select second team', ['All'] + list(df['team'].sort_values().unique()), key="team2")
player2 = st.sidebar.selectbox('Select second player', ['All'] + list(df[df['team'] == team2]['player'].sort_values().unique()) if team2 != 'All' else ['All'], key="player2")
shot_outcome2 = st.sidebar.selectbox("Second player's shot outcome", ['All'] + list(df[df['player'] == player2]['shot_outcome'].unique()) if player2 != 'All' else ['All'], key="outcome2")

# Function to filter data based on team, player, and shot outcome
def filter_data(df, team, player, shot_outcome):
    if team != 'All':
        df = df[df['team'] == team]
    if player != 'All':
        df = df[df['player'] == player]
    if shot_outcome != 'All':
        df = df[df['shot_outcome'] == shot_outcome]
    return df

# Filtered dataframes for each player
filtered_df1 = filter_data(df, team1, player1, shot_outcome1)
filtered_df2 = filter_data(df, team2, player2, shot_outcome2)

# Create a vertical pitch
pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10, 10))

# Function to plot shots
def plot_shots(df, ax, pitch, edge_color):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'],  # Scale the size by xG
            color='green' if x['shot_outcome'] == 'Goal' else 'white',  # Green for goal, white for others
            edgecolors=edge_color,  # Custom edge color for player
            alpha=1 if x['shot_outcome'] == 'Goal' else 0.5,
            linewidth=2,  # Outline thickness
            zorder=2 if x['shot_outcome'] == 'Goal' else 1
        )
# Plot shots for both players using different colors
plot_shots(filtered_df1, ax, pitch, 'blue')  # First player
plot_shots(filtered_df2, ax, pitch, 'red')   # Second player

# Create custom legend
legend_elements = [
    Patch(facecolor='white', edgecolor='blue', label=f'Player 1: {player1}', linewidth=2),
    Patch(facecolor='white', edgecolor='red', label=f'Player 2: {player2}', linewidth=2)
]

# Add legend to the plot
ax.legend(handles=legend_elements, loc='upper left', title="Legend")

# Display the plot
st.pyplot(fig)
