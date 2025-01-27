import streamlit as st
import math
from pathlib import Path
import numpy as np
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from data_loader import preprocess_data

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Oil Losses dashboard',
    page_icon='🌍', # This is an emoji shortcode
)
# -----------------------------------------------------------------------------
# Import the data

full_range, dates, subsidiaries, wells, losses = preprocess_data()

custom_colors = {
    "BR": "#00d4cf", "CD": "#444343", "CG":  "#ff6351", "CM":  "#9c27b0", "CO":  "#607d8b","GA": "#8bc34a", "GT":  "#f44336", "MX":  "#673ab7", "TD":  "#3f51b5", "TN":  "#2196f3", 
    "TR": "#cddc39", "TT":  "#e91e63", "UKS":  "#4caf50", "UKW":  "#795548", "VN":  "#ffeb3b", 
    "WELL WWO": "#9e9e9e"
    }

# Declare some useful functions.
st.sidebar.header("Filtros")
selected_dates = st.sidebar.slider(
    "Seleccionar rango de fechas",
    min_value=dates.min().to_pydatetime(),
    max_value=dates.max().to_pydatetime(),
    value=(dates.min().to_pydatetime(), dates.max().to_pydatetime()),
    format="YYYY-MM-DD"
)

selected_subsidiaries = st.sidebar.multiselect(
    "Seleccionar subsidiarias",
    options=subsidiaries,
    default=subsidiaries
)

# Filter the data from select
start_date, end_date = pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1])
filtered_dates = dates[(dates >= start_date) & (dates <= end_date)]
filtered_losses = losses.loc[filtered_dates, selected_subsidiaries]
filtered_wells = wells.loc[filtered_dates]

fig = go.Figure()

# Add area plot
for subsidiary in subsidiaries:
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=losses,
            mode="lines",
            #fill="tozeroy",
            name=subsidiary,
            line=dict(width=1, color=custom_colors.get(subsidiary, "#000000")),
            opacity=0.5,
            stackgroup='one',
        )
    )

# Add line plot for Wells WWO
fig.add_trace(
    go.Scatter(
        x=dates,
        y=wells,
        mode="lines",
        name="Cumulative Wells",
        line=dict(color="red", width=1),
        yaxis="y2",
    )
)

# Configure the layout
fig.update_layout(
    xaxis=dict(title="Date"),
    yaxis=dict(title="Oil losses (bopd)"),
    yaxis2=dict(title="Wells WWO", overlaying="y", side="right"),
    plot_bgcolor="white",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="center",
        x=0.5,
    ),
)

# Update layout
fig.update_layout(
    xaxis=dict(title="Date"),
    yaxis=dict(title="Oil losses (bopd)"),
    yaxis2=dict(title="Wells WWO", overlaying="y", side="right"),
    plot_bgcolor="white",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.1,
        xanchor="center",
        x=0.5,
        ),
    )
st.title("Oil Losses Dashboard")
st.plotly_chart(fig, use_container_width=True)


