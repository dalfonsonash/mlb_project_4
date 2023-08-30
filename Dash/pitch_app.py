import dash
from dash import dcc, html, dash_table, Input, Output
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

external_stylesheets = ['https://fonts.googleapis.com/css2?family=Alfa+Slab+One&display=swap']

# Set up inline styles
BODY_STYLE = {
    'backgroundColor': '#e1ad01',
    'margin': '0',
    'padding': '0',
    'font-family': 'Alfa Slab One, cursive'
}

output_differences_style = (
    "display: flex; justify-content: space-between; margin: 10px 0;"
)

# Define inline styles for the z-score box
z_score_box_style_base = {
    "padding": "2px",
    "font-weight": "bold",
    "font-size": "18",
    "margin-top": "10px",
    "width": "fit-content",
    "color": '#3e363f',  # Text color
}

z_score_box_style_green = {
    **z_score_box_style_base,
    "background-color": "#3f826d",
    "border": "2px solid #3e363f", 
    "padding": "4px", # Green background
}

z_score_box_style_red = {
    **z_score_box_style_base,
    "background-color": "#e2725b",
    "border": "2px solid #3e363f",
    "padding": "4px",  # Red background
}


# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style=BODY_STYLE, children=[
    html.H1("Baseball Player Dashboard"),
    dcc.Input(id="player-name", type="text", placeholder="Enter player's name"),
    html.Div(id="output-container", children=[
        html.Div(id="output-differences", style={
            "display": "flex",
            "justify-content": "space-between",
            "margin": "10px 0",
        }, children=[
            html.Div(id="era-difference-box", className="z-score-box", style={
                **z_score_box_style_base,
                "flex": "1",
                "margin-right": "10px",
            }),
            html.Div(id="fip-difference-box", className="z-score-box", style={
                **z_score_box_style_base,
                "flex": "1",
                "margin-right": "10px",
            }),
            html.Div(id="whip-difference-box", className="z-score-box", style={
                **z_score_box_style_base,
                "flex": "1",
                "margin-right": "10px",
            }),
        ]),
        # Adding the four verdict boxes
        html.Div(id="verdict-boxes", style={
            "display": "flex",
            "justify-content": "space-between",
            "margin": "10px 0",
        }, children=[
            html.Div(id="era-verdict-box", className="verdict-box", style={
                **z_score_box_style_base ,
                "flex": "1",
                "margin-right": "10px",
            }),
            html.Div(id="fip-verdict-box", className="verdict-box", style={
                **z_score_box_style_base ,
                "flex": "1",
                "margin-right": "10px",
            }),
            html.Div(id="whip-verdict-box", className="verdict-box", style={
                **z_score_box_style_base ,
                "flex": "1",
                "margin-right": "10px",
            }),
            
        ]),
        html.Div(id="player-info-container", className="player-info-container"),
        html.Div(id="output-graphs")
    ])
])

@app.callback(
    [Output("output-graphs", "children"),
     Output("era-difference-box", "children"),
     Output("era-difference-box", "className"),
     Output("fip-difference-box", "children"),
     Output("fip-difference-box", "className"),
     Output("whip-difference-box", "children"),
     Output("whip-difference-box", "className"),
     Output("era-verdict-box", "children"),
     Output("era-verdict-box", "className"),
     Output("fip-verdict-box", "children"),
     Output("fip-verdict-box", "className"),
     Output("whip-verdict-box", "children"),
     Output("whip-verdict-box", "className"),
     Output("player-info-container", "children")],
    [Input("player-name", "value")]
)
def update_graphs(name):
    if not name:
        return (
            [],  # Output "output-graphs.children"
            [],  # Output "era-difference-box.children"
            "z-score-box",  # Output "era-difference-box.className"
            [],  # Output "fip-difference-box.children"
            "z-score-box",  # Output "fip-difference-box.className"
            [],  # Output "whip-difference-box.children"
            "z-score-box",  # Output "whip-difference-box.className"
            "",  # Output "era-verdict-box.children"
            "z-score-box",  # Output "era-verdict-box.className"
            "",  # Output "fip-verdict-box.children"
            "z-score-box",  # Output "fip-verdict-box.className"
            "",  # Output "whip-verdict-box.children"
            "z-score-box",  # Output "whip-verdict-box.className"
            [],  # Output "player-info-container.children"
        )

    player_data = pd.read_csv("full_pitcher_data.csv")
    verdict_data = pd.read_csv("pitching_verdict.csv")
    
    player_info = player_data[player_data["Name"].str.contains(name, case=False)]
    verdict_info = verdict_data[verdict_data["Name"].str.contains(name, case=False)]
    
    if player_info.empty:
        return [html.Div("Player not found")], [], "z-score-box", [], "z-score-box", [], "z-score-box", [], "z-score-box", "", "z-score-box", "", "z-score-box", "", "z-score-box", "", "z-score-box", [html.Div()]

    # Create a 2x2 grid of subplots
    fig = make_subplots(rows=2, cols=2, subplot_titles=["Avg. ERA  /  ERA", "Avg. FIP  /  FIP 2023", 
                                                        "Avg. WHIP  /  WHIP 2023"],
                        shared_xaxes=False, horizontal_spacing=0.1)

    # Add the four bar graphs to the subplots
    fig.add_trace(go.Bar(x=player_info["Name"], y=player_info["ERA_avg"], name="ERA_avg", marker_color='#44cec5'), row=1, col=1)
    fig.add_trace(go.Bar(x=player_info["Name"], y=player_info["ERA_2023"], name="ERA_2023", marker_color='#321b47'), row=1, col=1)

    fig.add_trace(go.Bar(x=player_info["Name"], y=player_info["FIP"], name="FIP", marker_color='#44cec5'), row=1, col=2)
    fig.add_trace(go.Bar(x=player_info["Name"], y=player_info["FIP_2023"], name="FIP_2023", marker_color='#321b47'), row=1, col=2)

    fig.add_trace(go.Bar(x=player_info["Name"], y=player_info["WHIP"], name="WHIP", marker_color='#44cec5'), row=2, col=1)
    fig.add_trace(go.Bar(x=player_info["Name"], y=player_info["WHIP_2023"], name="WHIP_2023", marker_color='#321b47'), row=2, col=1)

    fig.update_traces(showlegend=False)

    fig.update_layout(
    title={
        'text': "Player: Improvement or Decline",
        'font': {'family': 'Alfa Slab One, cursive', 'size': 20, 'color': '#3e363f'}
    },
    barmode="group"
    )

    # Calculate z-score differences and verdicts
    z_score_diff_era = player_info["z_score_diff_era"].values[0]
    z_score_color_class_era = "z-score-box-green" if z_score_diff_era > 0 else "z-score-box-red"
    verdict_era = verdict_info["ERA_Correctness"].values[0]
    verdict_box_class_era = "z-score-box-green" if verdict_era == "Correct :)" else "z-score-box-red"

    z_score_diff_fip = player_info["z_score_diff_fip"].values[0]
    z_score_color_class_fip = "z-score-box-green" if z_score_diff_fip > 0 else "z-score-box-red"
    verdict_fip = verdict_info["FIP_Correctness"].values[0]
    verdict_box_class_fip = "z-score-box-green" if verdict_fip == "Correct :)" else "z-score-box-red"

    z_score_diff_whip = player_info["z_score_diff_whip"].values[0]
    z_score_color_class_whip = "z-score-box-green" if z_score_diff_whip > 0 else "z-score-box-red"
    verdict_whip = verdict_info["WHIP_Correctness"].values[0]
    verdict_box_class_whip = "z-score-box-green" if verdict_whip == "Correct :)" else "z-score-box-red"

    print(verdict_data["ERA_Correctness"].values[0])

    # Apply the appropriate style based on z_score_color_class
    z_score_box_style_era = z_score_box_style_green if z_score_color_class_era == "z-score-box-green" else z_score_box_style_red
    z_score_box_era = html.Div(
        f"ERA Difference: {z_score_diff_era:.2f}",
        style=z_score_box_style_era
    )

    z_score_box_style_fip = z_score_box_style_green if z_score_color_class_fip == "z-score-box-green" else z_score_box_style_red
    z_score_box_fip = html.Div(
        f"FIP Difference: {z_score_diff_fip:.2f}",
        style=z_score_box_style_fip
    )

    z_score_box_style_whip = z_score_box_style_green if z_score_color_class_whip == "z-score-box-green" else z_score_box_style_red
    z_score_box_whip = html.Div(
        f"WHIP Difference: {z_score_diff_whip:.2f}",
        style=z_score_box_style_whip
    )

     # Create the verdict boxes using Div elements with the appropriate styles and classes
    verdict_box_style_era = z_score_box_style_green if verdict_box_class_era == "z-score-box-green" else z_score_box_style_red
    verdict_box_era = html.Div(
        f"ERA Prediction: {verdict_era}",
        style=verdict_box_style_era
    )

    verdict_box_style_fip = z_score_box_style_green if verdict_box_class_fip == "z-score-box-green" else z_score_box_style_red
    verdict_box_fip = html.Div(
        f"FIP Prediction: {verdict_fip}",
        style=verdict_box_style_fip,
    )

    verdict_box_style_whip = z_score_box_style_green if verdict_box_class_whip == "z-score-box-green" else z_score_box_style_red
    verdict_box_whip = html.Div(
        f"WHIP Prediction: {verdict_whip}",
        style=verdict_box_style_whip,
    )
    
    selected_columns = [
        "Name", "W", "L", "SO", "Pitches", "Balls", "Strikes", "K/9",
        "HR/9", "IP", "R", "LOB%"
    ]

    # Round numeric values to 3 decimal places
    player_info_rounded = player_info[selected_columns].round(3)

    player_info_table = dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in selected_columns],
        data=player_info_rounded.to_dict("records")
    )

    # Return the updated verdict boxes along with other outputs
    return (
        [dcc.Graph(figure=fig)],  # Output "output-graphs.children"
        z_score_box_era,  # Output "era-difference-box.children"
        z_score_color_class_era,  # Output "era-difference-box.className"
        z_score_box_fip,  # Output "fip-difference-box.children"
        z_score_color_class_fip,  # Output "fip-difference-box.className"
        z_score_box_whip,  # Output "whip-difference-box.children"
        z_score_color_class_whip,  # Output "whip-difference-box.className"
        verdict_box_era,  # Output "era-verdict-box.children"
        verdict_box_class_era,  # Output "era-verdict-box.className"
        verdict_box_fip,  # Output "fip-verdict-box.children"
        verdict_box_class_fip, # Output "fip-verdict-box.className"
        verdict_box_whip,  # Output "whip-verdict-box.children"
        verdict_box_class_whip, # Output "whip-verdict-box.className"
        [player_info_table]  # Output "player-info-container.children"
    )
if __name__ == "__main__":
    app.run_server(debug=True)