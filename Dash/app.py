import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Baseball Player Dashboard"),
    dcc.Input(id="player-name", type="text", placeholder="Enter player's name"),
    html.Div(id="output-container", children=[
        html.Div(id="z-score-box", className="z-score-box"),  # Add the z-score box div here
        html.Div(id="output-graphs"),
        html.Div(id="player-info-container", className="player-info-container")
    ])
])

@app.callback(
    [Output("output-graphs", "children"),
     Output("z-score-box", "children"),
     Output("z-score-box", "className"),
     Output("player-info-container", "children")],
    [Input("player-name", "value")]
)
def update_graphs(name):
    if not name:
        return [], [], "z-score-box", []

    player_data = pd.read_csv("batting_for_learning copy.csv")

    # Use case-insensitive search for player name
    player_info = player_data[player_data["name"].str.contains(name, case=False)]

    if player_info.empty:
        return [html.Div("Player not found")], [], "z-score-box", []

    fig = px.bar(player_info, x="name", y=["avg_woba", "woba_2023"], 
                 labels={"value": "wOBA"}, title="Average wOBA for Player {}".format(name),
                 barmode="group")

    z_score_difference = player_info["z_scores_avg_woba"].values[0]
    z_score_color_class = "z-score-box-green" if z_score_difference > 0 else "z-score-box-red"

    z_score_box = html.Div(
        f"Z-Score Difference: {z_score_difference:.2f}",
        className=z_score_color_class
    )

    selected_columns = [
        "name", "bip", "ba", "est_ba", "est_ba_minus_ba_diff",
        "slg", "est_slg", "est_slg_minus_slg_diff", "est_woba",
        "est_woba"
    ]

    # Round numeric values to 3 decimal places
    player_info_rounded = player_info[selected_columns].round(3)
    
    player_info_table = dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in selected_columns],
        data=player_info_rounded.to_dict("records")
    )

    return [dcc.Graph(figure=fig)], z_score_box, z_score_color_class, [player_info_table]

if __name__ == "__main__":
    app.run_server(debug=True)
