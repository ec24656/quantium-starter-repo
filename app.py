import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Load clean data
df = pd.read_csv("task1_completed.csv")

# Convert types
df["date"] = pd.to_datetime(df["date"])
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

# Sort
df = df.sort_values("date")

# Aggregate daily
df_daily = df.groupby("date", as_index=False)["sales"].sum()

# Aggregate monthly (clean visual)
df_monthly = df_daily.groupby(
    pd.Grouper(key="date", freq="ME")
)["sales"].sum().reset_index()

# Plot
fig = px.line(
    df_monthly,
    x="date",
    y="sales",
    title="Total Monthly Sales of Pink Morsels",
    labels={"date": "Date", "sales": "Total Sales"}
)

# Vertical line (price increase)
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

# Improve readability
fig.update_layout(xaxis_tickangle=-45)

# Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods Sales Visualiser", style={"textAlign": "center"}),
    dcc.Graph(figure=fig)
])

# Run
if __name__ == "__main__":
    app.run(debug=True)