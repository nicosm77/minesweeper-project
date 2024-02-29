import pandas as pd
import plotly.express as px
import sqlite3

# Mapping dictionary for board sizes to difficulty levels
board_size_mapping = {
    5: "Very Easy",
    10: "Easy",
    15: "Medium",
    20: "Hard"
}

def visualize_avg_completion_time(leaderboard_df):
    """
    Visualize average completion time for each board size using a bar chart.
    """
    # Filter leaderboard data for the four specified board sizes
    leaderboard_df = leaderboard_df[leaderboard_df['boardsize'].isin([5, 10, 15, 20])]
    avg_time_df = leaderboard_df.groupby('boardsize')['time'].mean().reset_index()
    avg_time_df['boardsize'] = avg_time_df['boardsize'].map(board_size_mapping)  # Map board sizes to difficulty levels
    fig = px.bar(avg_time_df, x='boardsize', y='time', title='Average Completion Time by Difficulty Level')
    fig.update_xaxes(title_text='Difficulty Level')
    fig.update_yaxes(title_text='Average Completion Time (seconds)')
    return fig

def visualize_players_distribution(leaderboard_df):
    """
    Visualize distribution of players across different board sizes using a pie chart.
    """
    # Filter leaderboard data for the four specified board sizes
    leaderboard_df = leaderboard_df[leaderboard_df['boardsize'].isin([5, 10, 15, 20])]
    player_counts_df = leaderboard_df['boardsize'].map(board_size_mapping).value_counts().reset_index()
    player_counts_df.columns = ['Difficulty Level', 'Player Count']
    fig = px.pie(player_counts_df, names='Difficulty Level', values='Player Count', title='Distribution of Players by Difficulty Level')
    return fig

def visualize_completion_time_scatter(leaderboard_df):
    """
    Visualize completion time of each player for each board size using a scatter plot.
    """
    # Filter leaderboard data for the four specified board sizes
    leaderboard_df = leaderboard_df[leaderboard_df['boardsize'].isin([5, 10, 15, 20])]
    leaderboard_df['boardsize'] = leaderboard_df['boardsize'].map(board_size_mapping)  # Map board sizes to difficulty levels
    fig = px.scatter(leaderboard_df, x='boardsize', y='time', color='name', title='Completion Time by Difficulty Level and Player')
    fig.update_xaxes(title_text='Difficulty Level')
    fig.update_yaxes(title_text='Completion Time (seconds)')
    return fig

def visualize_avg_completion_time_per_person(leaderboard_df):
    """
    Visualize average completion time per person per difficulty level.
    """
    avg_time_per_person_df = leaderboard_df.groupby(['name', 'boardsize'])['time'].mean().reset_index()
    avg_time_per_person_df['boardsize'] = avg_time_per_person_df['boardsize'].map(board_size_mapping)  # Map board sizes to difficulty levels
    fig = px.bar(avg_time_per_person_df, x='name', y='time', color='boardsize', title='Average Completion Time per Person by Difficulty Level')
    fig.update_xaxes(title_text='Player')
    fig.update_yaxes(title_text='Average Completion Time (seconds)')
    return fig



def main():
    # Fetch leaderboard data
    conn = sqlite3.connect("leaderboard_db.sqlite")
    query = "SELECT * FROM leaderboard"
    leaderboard_df = pd.read_sql_query(query, conn)

    # Visualize average completion time for each board size
    avg_completion_time_fig = visualize_avg_completion_time(leaderboard_df)
    avg_completion_time_fig.show()

    # Visualize distribution of players across different board sizes
    players_distribution_fig = visualize_players_distribution(leaderboard_df)
    players_distribution_fig.show()

    # Visualize completion time of each player for each board size
    completion_time_scatter_fig = visualize_completion_time_scatter(leaderboard_df)
    completion_time_scatter_fig.show()

    completion_time_per_person_fig = visualize_avg_completion_time_per_person(leaderboard_df)
    completion_time_per_person_fig.show()

if __name__ == "__main__":
    main()
