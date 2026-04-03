import pandas as pd
import os
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "data")

files = [
    "daily_sales_data_0.csv",
    "daily_sales_data_1.csv",
    "daily_sales_data_2.csv"
]

df_list = [pd.read_csv(os.path.join(data_path, f)) for f in files]

df = pd.concat(df_list, ignore_index=True)

df = df[df["product"] == "pink morsel"]
df["sales"] = df["price"] * df["quantity"]
df["date"] = pd.to_datetime(df["date"])

app = Dash(__name__)

app.layout = html.Div(
    style={
        "textAlign": "center",
        "backgroundColor": "#f5f5f5",
        "padding": "20px"
    },
    children=[

        html.H1("Soul Foods Sales Visualiser"),

        html.Div([
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
        ]),

        
        dcc.Graph(id="sales-graph")
    ]
)


@app.callback(
    Output("sales-graph", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):
    filtered_df = df.copy()

    if selected_region != "all":
        filtered_df = filtered_df[filtered_df["region"] == selected_region]

    df_grouped = (
        filtered_df
        .groupby(pd.Grouper(key="date", freq="ME"))["sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(df_grouped, x="date", y="sales", title="Sales Trend")

    fig.add_vline(
        x=pd.to_datetime("2021-01-15"),
        line_dash="dash",
        annotation_text="Price Increase"
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)