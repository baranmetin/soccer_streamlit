import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go

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

# Create the pitch layout for Plotly (resembling the vertical pitch)
def create_pitch():
    pitch_width = 120
    pitch_height = 80
    fig = go.Figure()

    # Add the field background
    fig.update_layout(
        plot_bgcolor='#a8bc95',
        shapes=[
            # Pitch outline
            dict(type="rect", x0=0, y0=0, x1=pitch_width, y1=pitch_height, line=dict(color="black", width=3)),
            # Center circle
            dict(type="circle", x0=pitch_width/2 - 9.15, y0=pitch_height/2 - 9.15, x1=pitch_width/2 + 9.15, y1=pitch_height/2 + 9.15, line=dict(color="black", width=2)),
            # Penalty area
            dict(type="rect", x0=0, y0=18, x1=18, y1=62, line=dict(color="black", width=2)),
            dict(type="rect", x0=pitch_width - 18, y0=18, x1=pitch_width, y1=62, line=dict(color="black", width=2)),
        ],
        xaxis=dict(range=[0, pitch_width], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0, pitch_height], showgrid=False, zeroline=False, showticklabels=False),
        width=700, height=500
    )
    return fig

# Create the pitch figure
fig = create_pitch()

# Add shots to the pitch with player name and minute as hover info
for _, row in filtered_df.iterrows():
    fig.add_trace(go.Scatter(
        x=[float(row['location'][0])],
        y=[float(row['location'][1])],
        mode='markers',
        marker=dict(
            size=1000 * row['shot_statsbomb_xg'],
            color='green' if row['shot_outcome'] == 'Goal' else 'white',
            line=dict(color='black', width=2),
            opacity=1 if row['shot_outcome'] == 'Goal' else 0.5
        ),
        hoverinfo='text',
        text=f"Player: {row['player']}<br>Minute: {row['minute']}",
        name=row['player']
    ))

# Display the plot
st.plotly_chart(fig)
