import streamlit as st
import pandas as pd
import json
from mplsoccer import VerticalPitch

st.title("Euros 2024 Shot Map")
st.subheader("Select team, player, and shot outcome to visualize the shot map, or view all shots.")

# Load the data
df = pd.read_csv('euros_2024_shot_map.csv')
df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)

# Sidebar for filtering
team = st.sidebar.selectbox('Select a team', ['All'] + list(df['team'].sort_values().unique()))
player = st.sidebar.selectbox('Select a player', ['All'] + list(df[df['team'] == team]['player'].sort_values().unique()) if team != 'All' else ['All'])
shot_outcome = st.sidebar.selectbox("Shot outcome", ['All'] + list(df[df['player'] == player]['shot_outcome'].unique()) if player != 'All' else ['All'])

# Function to filter data based on team, player, and shot outcome
def filter_data(df, team, player, shot_outcome):
    if team != 'All':
        df = df[df['team'] == team]
    if player != 'All':
        df = df[df['player'] == player]
    if shot_outcome != 'All':
        df = df[df['shot_outcome'] == shot_outcome]
    return df

# Filtered dataframe
filtered_df = filter_data(df, team, player, shot_outcome)

# Create a vertical pitch
pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10, 10))

# Function to plot shots
def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'],
            color='green' if x['shot_outcome'] == 'Goal' else 'white',
            edgecolors='black',
            alpha=1 if x['shot_outcome'] == 'Goal' else 0.5,
            zorder=2 if x['shot_outcome'] == 'Goal' else 1
        )

# Plot filtered shots
plot_shots(filtered_df, ax, pitch)

# Display the plot
st.pyplot(fig)
