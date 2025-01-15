import os
import json
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)


# Load and process JSON data
import os
import json
import pandas as pd


def load_json_files(folder_path):
    data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(folder_path, filename), "r") as file:
                    json_data = json.load(file)

                    if isinstance(json_data, dict):
                        for user, records in json_data.items():
                            if isinstance(records, list):
                                for record in records:
                                    data.append(
                                        {
                                            "user": user,
                                            "model": record.get("model", "unknown"),
                                            "timestamp": record.get(
                                                "timestamp", "unknown"
                                            ),
                                            "input_tokens": record.get(
                                                "input_tokens", 0
                                            ),
                                            "output_tokens": record.get(
                                                "output_tokens", 0
                                            ),
                                            "total_cost": float(
                                                record.get("total_cost", 0.0)
                                            ),
                                        }
                                    )
                            else:
                                print(
                                    f"Skipping records for user {user}, expected list but got {type(records)}"
                                )
                    else:
                        print(
                            f"Invalid JSON structure in {filename}, expected dictionary at top level."
                        )

                print(f"Successfully read {filename}")
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    return pd.DataFrame(data)


# Load data from the folder containing the .json files
folder_path = "/home/yhs/data"  # Update this with your folder path
df = load_json_files(folder_path)

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Calculate summaries
user_summary = (
    df.groupby("user")
    .agg(
        total_input_tokens=("input_tokens", "sum"),
        total_output_tokens=("output_tokens", "sum"),
        total_cost=("total_cost", "sum"),
    )
    .reset_index()
)


# Visualization Functions
def create_graphs(df):
    graphs = []

    # 1. Total Input Tokens by User
    fig1 = px.bar(
        user_summary,
        x="user",
        y="total_input_tokens",
        title="Total Input Tokens by User",
    )
    graphs.append(dcc.Graph(figure=fig1))

    # 2. Total Output Tokens by User
    fig2 = px.bar(
        user_summary,
        x="user",
        y="total_output_tokens",
        title="Total Output Tokens by User",
    )
    graphs.append(dcc.Graph(figure=fig2))

    # 3. Total Cost by User
    fig3 = px.bar(user_summary, x="user", y="total_cost", title="Total Cost by User")
    graphs.append(dcc.Graph(figure=fig3))

    # 4. Input vs Output Tokens (Proportion)
    fig4 = px.bar(
        user_summary,
        x="user",
        y=["total_input_tokens", "total_output_tokens"],
        title="Input vs Output Tokens by User",
    ).update_layout(barmode="stack")
    graphs.append(dcc.Graph(figure=fig4))

    # 5. Cost Over Time (Line Chart)
    fig5 = px.line(
        df, x="timestamp", y="total_cost", color="user", title="Cost Over Time by User"
    )
    graphs.append(dcc.Graph(figure=fig5))

    # 6. Tokens Over Time (Line Chart)
    tokens_df = df.groupby(["timestamp", "user"]).sum().reset_index()
    fig6 = px.line(
        tokens_df,
        x="timestamp",
        y="input_tokens",
        color="user",
        title="Input Tokens Over Time by User",
    )
    graphs.append(dcc.Graph(figure=fig6))

    # 7. Average Cost Per Transaction by User
    avg_cost = df.groupby("user").agg(avg_cost=("total_cost", "mean")).reset_index()
    fig7 = px.bar(
        avg_cost, x="user", y="avg_cost", title="Average Cost per Transaction"
    )
    graphs.append(dcc.Graph(figure=fig7))

    # 8. Cost Distribution (Histogram)
    fig8 = px.histogram(df, x="total_cost", color="user", title="Cost Distribution")
    graphs.append(dcc.Graph(figure=fig8))

    # 9. Model Usage by User
    model_summary = df.groupby(["user", "model"]).size().reset_index(name="count")
    fig9 = px.bar(
        model_summary,
        x="user",
        y="count",
        color="model",
        title="Model Usage by User",
        barmode="stack",
    )
    graphs.append(dcc.Graph(figure=fig9))

    # 10. Total Input and Output Tokens by User (Pie Chart)
    fig10 = px.pie(
        user_summary,
        names="user",
        values="total_input_tokens",
        title="Total Input Tokens by User (Pie)",
    )
    graphs.append(dcc.Graph(figure=fig10))

    # 11. Total Tokens by User (Stacked Bar)
    fig11 = px.bar(
        user_summary,
        x="user",
        y=["total_input_tokens", "total_output_tokens"],
        title="Total Tokens by User (Stacked)",
    ).update_layout(barmode="stack")
    graphs.append(dcc.Graph(figure=fig11))

    # 12. Cost by Model (Bar Chart)
    model_cost = df.groupby("model").agg(total_cost=("total_cost", "sum")).reset_index()
    fig12 = px.bar(model_cost, x="model", y="total_cost", title="Total Cost by Model")
    graphs.append(dcc.Graph(figure=fig12))

    # 13. User Token Usage Over Time (Line Chart)
    user_time_df = (
        df.groupby(["timestamp", "user"])
        .agg(total_tokens=("input_tokens", "sum"))
        .reset_index()
    )
    fig13 = px.line(
        user_time_df,
        x="timestamp",
        y="total_tokens",
        color="user",
        title="User Token Usage Over Time",
    )
    graphs.append(dcc.Graph(figure=fig13))

    # 14. Total Number of Transactions by User
    transaction_count = df.groupby("user").size().reset_index(name="transaction_count")
    fig14 = px.bar(
        transaction_count,
        x="user",
        y="transaction_count",
        title="Total Transactions by User",
    )
    graphs.append(dcc.Graph(figure=fig14))

    # 15. Cost vs Tokens (Scatter Plot)
    fig15 = px.scatter(
        df,
        x="total_cost",
        y="input_tokens",
        color="user",
        title="Cost vs Tokens by User (Scatter)",
    )
    graphs.append(dcc.Graph(figure=fig15))

    # 16. Average Tokens Per Transaction by User
    avg_tokens = (
        df.groupby("user").agg(avg_tokens=("input_tokens", "mean")).reset_index()
    )
    fig16 = px.bar(
        avg_tokens, x="user", y="avg_tokens", title="Average Tokens Per Transaction"
    )
    graphs.append(dcc.Graph(figure=fig16))

    return graphs


# Create the dashboard layout
app.layout = html.Div(
    [
        html.H1("User Token and Cost Dashboard"),
        html.Div(
            create_graphs(df),
            style={
                "display": "grid",
                "grid-template-columns": "repeat(4, 1fr)",  # 4 graphs per row for 16 graphs
                "gap": "20px",
            },
        ),
    ]
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=False)
