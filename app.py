import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("task1_completed.csv")

# Clean + prepare
df["date"] = pd.to_datetime(df["date"])
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
df = df.sort_values("date")

# Initialize app
app = Dash(__name__)

# Layout
app.layout = html.Div(
    style={"backgroundColor": "#f4f6f8", "padding": "20px"},
    children=[

        html.H1(
            "Soul Foods Sales Visualiser",
            style={
                "textAlign": "center",
                "color": "#2c3e50",
                "marginBottom": "30px"
            }
        ),

        html.Div([
            html.Label(
                "Select Region:",
                style={"fontWeight": "bold", "marginRight": "10px"}
            ),

            dcc.RadioItems(
                id="region-filter",
                options=[
                    {"label": "All", "value": "all"},
                    {"label": "North", "value": "north"},
                    {"label": "East", "value": "east"},
                    {"label": "South", "value": "south"},
                    {"label": "West", "value": "west"},
                ],
                value="all",
                inline=True
            )
        ], style={"textAlign": "center", "marginBottom": "20px"}),

        dcc.Graph(id="sales-graph")
    ]
)

# Callback for dynamic updates
@app.callback(
    Output("sales-graph", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):

    # Filter by region
    if selected_region != "all":
        filtered_df = df[df["region"].str.lower() == selected_region]
    else:
        filtered_df = df.copy()

    # Aggregate daily
    df_daily = filtered_df.groupby("date", as_index=False)["sales"].sum()

    # Aggregate monthly
    df_monthly = df_daily.groupby(
        pd.Grouper(key="date", freq="ME")
    )["sales"].sum().reset_index()

    # Create figure
    fig = px.line(
        df_monthly,
        x="date",
        y="sales",
        title=f"Sales Trend ({selected_region.capitalize()})",
        labels={"date": "Date", "sales": "Total Sales"}
    )

    # Add price increase line
    fig.add_shape(
        type="line",
        x0="2021-01-15",
        x1="2021-01-15",
        y0=0,
        y1=df_monthly["sales"].max(),
        line=dict(color="red", dash="dash")
    )

    fig.add_annotation(
        x="2021-01-15",
        y=df_monthly["sales"].max(),
        text="Price Increase",
        showarrow=True,
        arrowhead=1
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="#f4f6f8",
        xaxis_tickangle=-45
    )

    return fig


# Run app
if __name__ == "__main__":
    app.run(debug=True)