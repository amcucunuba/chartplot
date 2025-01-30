import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from data_loader import load_data, preprocess_data

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Oil Losses dashboard',
    page_icon='🌍', # This is an emoji shortcode
)
# -----------------------------------------------------------------------------
# Import the data
data = load_data("./data/Losses and number of wells waiting for workover by subsidiary 16012024.csv")

data['date'] = pd.to_datetime(data['date'])

data.columns = ["date", "Subsidiary", "Oil losses (bopd)", "Wells WWO"]

# Map colours
custom_colors = {
    "BR": "#00d4cf", "CD": "#444343", "CG":  "#ff6351", "CM":  "#f1c232", "CO":  "#607d8b",
    "GA": "#9fdee8", "GT":  "#98e76a", "MX":  "#ec8a6e", "TD":  "#a76988", "TN":  "#1e53f7", 
    "TR": "#53a4b6", "TT":  "#00a19d", "UKS":  "#e4bbbb", "UKW":  "#047774", "VN":  "#fd3bff", 
    }

'''
# 🌍 Oil losses and Wells WWO
Browse Oil losses data from the PDE-PowerBi website. As you'll notice, the data only goes to 2023 right now, 
and datapoints for certain years are often missing.
'''

#Filtred the date
min_value = data['date'].min().to_pydatetime()
max_value = data['date'].max().to_pydatetime()

from_date, to_date = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

#Filtred the subsidiarys by date
subsidiaries = data['Subsidiary'].unique()

if not len(subsidiaries):
    st.warning("Select at least one country")

selected_subsidiaries = st.multiselect(
    'Which countries would you like to view?',
    options=subsidiaries,
    default=subsidiaries)

filtered_data = data[
    (data['Subsidiary'].isin(selected_subsidiaries))
    & (data['date'] <= to_date)
    & (from_date <= data['date'])
]

#st.header(divider='gray')

filtered_data = data[
    (data['Subsidiary'].isin(selected_subsidiaries)) &
    (data['date'] >= from_date) &
    (data['date'] <= to_date)
]

# Recompute Wells WWO dynamically
daily_wells = filtered_data.groupby('date')['Wells WWO'].sum()  # Aggregate daily Wells WWO
cumulative_wells = daily_wells.cumsum()

# Make the plot
fig = go.Figure()
    # Area plot for Oil losses
for subsidiary in selected_subsidiaries:
    subsidiary_data = filtered_data[filtered_data['Subsidiary'] == subsidiary]
    fig.add_trace(
    go.Scatter(
            x=subsidiary_data['date'],
            y=subsidiary_data['Oil losses (bopd)'],
            mode="lines",
            name=f'{subsidiary}',
            line=dict(width=1, color=custom_colors.get(subsidiary, "#000000")),
            opacity=0.5,
            stackgroup='one',
        )
    )
    # Add line plot for Wells WWO
fig.add_trace(
        go.Scatter(
            x=daily_wells.index,
            y=daily_wells.values,
            mode="lines",
            name="Wells<br>WWO", #<br> It's a jump 
            line=dict(color="red", width=1.5),
            yaxis="y2",
        )
    )

# Configure the layout
fig.update_layout(title=dict(text="Oil losses over time", font=dict(size=40), automargin=True),
    xaxis=dict(title="Date"),
    yaxis=dict(title="Oil losses (bopd)"),
    yaxis2=dict(title="Wells WWO", overlaying="y", side="right", position=1),
    plot_bgcolor="white",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="right",
        x=1,
        entrywidth=20,
        title_font_family="Open Sans",
        font=dict(
            family="Open Sans",
            size=8,
            color="black",
            
         ), 
    )
)
fig.update_layout(template="simple_white",
                hovermode="x unified", 
                hoverlabel=dict(
                bgcolor="white",
                font_size=10,
                font_family="Open Sans"
    ) )
fig.update_layout(autosize=False,
                width=800,
                height=500,
                margin=dict(l=20, r=20, b=20, t=20))

st.plotly_chart(fig, use_container_width=True)