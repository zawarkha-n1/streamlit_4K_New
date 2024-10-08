#-----------------------------------------------------------------

import pandas as pd
import streamlit as st
import plotly.express as px
import gspread
from datetime import timedelta
from google.oauth2 import service_account
import numpy as np

@st.cache_data(ttl=3600*1)
def all_data_for_stats():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Load credentials from Streamlit secrets
    service_account_info = st.secrets["gcp_service_account"]
    creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=scope)

    # Authorize the credentials with gspread
    client = gspread.authorize(creds)

    # Access the Google Sheet using the spreadsheet ID
    spreadsheet_id = "19PaTSR26LeiEPzmdCJqS_x3-GjZfaRzKLvsHwQ6mPts"
    sheet = client.open_by_key(spreadsheet_id)



    worksheet0 = sheet.worksheet("Sheet0")
    worksheet1 = sheet.worksheet("Sheet1")
    worksheet2 = sheet.worksheet("Sheet2")

    # Get the records from each worksheet
    data_for_graphs0 = worksheet0.get_all_records()
    data_for_graphs1 = worksheet1.get_all_records()
    data_for_graphs2 = worksheet2.get_all_records()


    # Convert the records to DataFrames ehdvhvhevd jhebjebdebdhebd
    df_for_graphs0 = pd.DataFrame(data_for_graphs0)
    df_for_graphs1 = pd.DataFrame(data_for_graphs1)
    df_for_graphs2 = pd.DataFrame(data_for_graphs2)

    all_data = pd.concat([df_for_graphs0, df_for_graphs1, df_for_graphs2], ignore_index=True)
    all_data.replace('NA', np.nan, inplace=True)
    all_data = all_data.fillna(0)
    return all_data

@st.cache_data(ttl=3600*1)
def df_for_comp():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Load credentials from Streamlit secrets
    service_account_info = st.secrets["gcp_service_account"]
    creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=scope)

    # Authorize the credentials with gspread
    client = gspread.authorize(creds)

    # Access the Google Sheet using the spreadsheet ID
    spreadsheet_id = "19PaTSR26LeiEPzmdCJqS_x3-GjZfaRzKLvsHwQ6mPts"
    sheet = client.open_by_key(spreadsheet_id)

    worksheet4 = sheet.worksheet("comparisons")

    data_for_comp = worksheet4.get_all_records()

    df_for_com = pd.DataFrame(data_for_comp)
    df_for_com.replace('NA', pd.NA, inplace=True)
    df_for_com.fillna(0, inplace=True)
    return df_for_com


 

all_data = all_data_for_stats()

all_data['Date'] = pd.to_datetime(all_data['Date'], format='%m/%d/%Y')


def zeniva_values_for_insights(data):
    zeniva_data = data[(data["Product"] == "zeniva") & (data["Platform"])]
    max_date = zeniva_data['Date'].max()
    
    latest_zeniva_data = zeniva_data[zeniva_data['Date'] == max_date]
    pivoted_data = latest_zeniva_data.pivot(index=['Date', 'Product', 'Platform'], columns='Matrix', values='Values').reset_index()
    zeniva_youtube = pivoted_data[pivoted_data["Platform"] == "youtube"]
    zeniva_x = pivoted_data[pivoted_data["Platform"] == "x"]
    zeniva_tiktok = pivoted_data[pivoted_data["Platform"] == "tiktok"]
    zeniva_linkedin = pivoted_data[pivoted_data["Platform"] == "linkedin"]
    zeniva_instagram = pivoted_data[pivoted_data["Platform"] == "instagram"]
    zeniva_facebook = pivoted_data[pivoted_data["Platform"] == "facebook"]
    return (
        zeniva_youtube[["total_followers", "today_followers", "yesterday_followers"]],
        zeniva_x[["total_followers", "today_followers", "yesterday_followers"]],
        zeniva_tiktok[["total_followers", "today_followers", "yesterday_followers"]],
        zeniva_linkedin[["total_followers", "today_followers", "yesterday_followers"]],
        zeniva_instagram[["total_followers", "today_followers", "yesterday_followers"]],
        zeniva_facebook[["total_followers", "today_followers", "yesterday_followers"]],
    )


def exarta_values_for_insights(data):
    exarta_data = data[(data["Product"] == "Exarta") & (data["Platform"])]
    max_date = exarta_data['Date'].max()
    
    latest_exarta_data = exarta_data[exarta_data['Date'] == max_date]
    pivoted_data = latest_exarta_data.pivot(index=['Date', 'Product', 'Platform'], columns='Matrix', values='Values').reset_index()
    exarta_youtube = pivoted_data[pivoted_data["Platform"] == "youtube"]
    exarta_x = pivoted_data[pivoted_data["Platform"] == "x"]
    exarta_facebook = pivoted_data[pivoted_data["Platform"] == "facebook"]
    exarta_linkedin = pivoted_data[pivoted_data["Platform"] == "linkedin"]
    exarta_instagram = pivoted_data[pivoted_data["Platform"] == "instagram"]
    return (
        exarta_youtube[["total_followers", "today_followers", "yesterday_followers"]],
        exarta_x[["total_followers", "today_followers", "yesterday_followers"]],
        exarta_facebook[["total_followers", "today_followers", "yesterday_followers"]],
        exarta_linkedin[["total_followers", "today_followers", "yesterday_followers"]],
        exarta_instagram[["total_followers", "today_followers", "yesterday_followers"]],
    )



def odyssey_values_for_insights(data):
    odyssey_data = data[(data["Product"] == "Odyssey") & (data["Platform"])]
    max_date = odyssey_data['Date'].max()
    
    latest_odyssey_data  = odyssey_data[odyssey_data['Date']== max_date]
    pivoted_data = latest_odyssey_data.pivot(index=['Date', 'Product', 'Platform'], columns='Matrix', values='Values').reset_index()
    odyssey_youtube = pivoted_data[pivoted_data["Platform"] == "youtube"]
    odyssey_tiktok = pivoted_data[pivoted_data["Platform"] == "tiktok"]
    odyssey_instagram = pivoted_data[pivoted_data["Platform"] == "instagram"]
    odyssey_facebook = pivoted_data[pivoted_data["Platform"] == "facebook"]
    return (
        odyssey_youtube[["total_followers", "today_followers", "yesterday_followers"]],
        odyssey_tiktok[["total_followers", "today_followers", "yesterday_followers"]],
        odyssey_instagram[["total_followers", "today_followers", "yesterday_followers"]],
        odyssey_facebook[["total_followers", "today_followers", "yesterday_followers"]],
    )






def plot_histograms(product_name, platform_name):
    # Load and preprocess the data
    df = all_data
    df = df[(df['Product'] == product_name)]
    
    platform_metrics = {
        'youtube': ['clicks', 'views', 'daily_spend'],
        'meta': ['clicks', 'reach', 'daily_spend'],
        'shopify': ['clicks', 'daily_spend', 'dummy_metric'],  # Add dummy metric for Shopify
        'ppc': ['clicks', 'daily_spend', 'impressions'],
    }

    if platform_name in platform_metrics:
        selected_metrics = platform_metrics[platform_name]
    else:
        st.error(f"Platform {platform_name} not recognised.")
        return

    df_platform = df[df['Platform'] == platform_name]
    

    # Convert 'date' column to datetime format for easier comparison
    df_platform['Date'] = pd.to_datetime(df_platform['Date'], format='%m/%d/%Y')

    # Get the latest date available for the selected platform
    if df_platform.empty:
        st.error(f"No data available for platform {platform_name}.")
        return

    latest_date = df_platform['Date'].max()

    # Get the last 3 available dates based on the latest date
    dates = [latest_date - timedelta(days=i) for i in range(3)]
    
    # Ensure formatted dates match the datetime format in the dataframe
    formatted_dates = [date.strftime("%m-%d-%y") for date in dates]

    # Filter the dataframe to include only the last 3 available dates
    df_filtered = df_platform[df_platform['Date'].isin(dates)]

  

    # Add dummy metric for Shopify to ensure consistent bar width
    if 'dummy_metric' in selected_metrics:
        df_filtered['dummy_metric'] = 0
        
    selected_matrix = ['clicks', 'views', 'daily_spend', "reach" ]

    df_filtered = df_filtered[df_filtered['Matrix'].isin(selected_matrix)]
    
    summary_df = df_filtered.groupby(['Date', 'Matrix'])['Values'].sum().reset_index()

    # Pivot the DataFrame to get dates as rows and metrics as columns
    summary_pivot = summary_df.pivot(index='Date', columns='Matrix', values='Values').fillna(0)

    # Reset index to have 'Date' as a column
    summary_pivot.reset_index(inplace=True)

   
    # Define color mapping for metrics
    color_discrete_map = {
        'clicks': '#BC679C',
        'views': '#F68C5B',
        'daily_spend': '#A6B174',
        'reach': '#F68C5B',
        'impressions': '#F68C5B',
        'dummy_metric': '#FFFFFF'  # Invisible color for the dummy metric
    }

    label_map = {
            'clicks': 'Clicks',
            'views': 'Views',
            'daily_spend': 'Daily Spend',
            'reach': 'Reach',
            'impressions': 'Impressions',
            'dummy_metric': ''  # No label for the dummy metric
        }
    summary_melted = summary_pivot.melt(id_vars='Date', var_name='Metric', value_name='Value')



    # Plot histogram
    fig = px.histogram(
        summary_melted, 
        x='Date', 
        y='Value', 
        color='Metric', 
        barmode='group', 
        height=220,
        width=620,
        color_discrete_map=color_discrete_map,
    )

    fig.for_each_trace(lambda trace: trace.update(name=label_map.get(trace.name, trace.name), showlegend=False if trace.name == 'dummy_metric' else True))
    
    
    # Extract unique dates for the x-axis and format them
    unique_dates = df['Date'].dt.to_period('D').astype('str').unique()
    formatted_dates = [pd.to_datetime(date).strftime('%d %B') for date in unique_dates]


    fig.update_layout(
    xaxis=dict(
         tickvals=pd.to_datetime(unique_dates).to_pydatetime(),  # Set tick values to unique dates
         ticktext=formatted_dates,  # Format tick text
         ticklabelposition="outside",  # Position the labels outside the plot area
         tickson="labels",  # Ensure ticks are aligned with labels
         title_standoff=24,  # Increase space between x-axis title and labels
         ticks="outside",  # Ensure ticks are outside the plot area
         tickfont=dict(size=7),
    ),
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background for the plot area
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the whole figure
    font_color='white',
    bargap=0.4,  # Adjust the gap between bars
    bargroupgap=0.3,  # Adjust the gap between groups of bars
    yaxis=dict(
        showgrid=True,  # Enable horizontal grid lines
        gridcolor='rgba(255,255,255,0.1)',  # Set grid line color to a very translucent white
        gridwidth=1,  # Set the width of grid lines
    ),
    xaxis_title=None,
    yaxis_title=None,
)

    # Update the layout to add border-radius effect
    fig.update_traces(marker=dict(
        line=dict(
            width=5,
            color='rgba(0,0,0,0)'  # Optional: border color
        ),
        opacity=0.9  # Optional: adjust bar opacity
    ))

    # Update legend settings
    fig.update_layout(
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": -0.5,
            "xanchor": "center",
            "x": 0.5,
            "font": {
                "color": "white",  # Legend text color
                "size": 7         # Increase the font size as needed
            },
        },
        legend_title_text="",
    )

    # Convert figure to HTML and return
    fig_html = fig.to_html(include_plotlyjs='cdn')
    return fig_html


def zeniva_overview(df):

    today_paid_installs = df[(df['Product'] == 'Zeniva') & (df['Matrix'] == 'today_paid_installs')]['Values'].values[0]
    todays_free_installs = df[(df['Product'] == 'Zeniva') & (df['Matrix'] == 'todays_free_installs')]['Values'].values[0] 
    lifetime_installs = df[(df['Product'] == 'Zeniva') & (df['Matrix'] == 'lifetime_installs')]['Values'].values[0] 
    today_paid_uninstalls = df[(df['Product'] == 'Zeniva') & (df['Matrix'] == 'today_paid_installs')]['Values'].values[0] 
    today_free_uninstalls = df[(df['Product'] == 'Zeniva') & (df['Matrix'] == 'today_free_uninstalls')]['Values'].values[0] 
    lifetime_uninstalls = df[(df['Product'] == 'Zeniva') & (df['Matrix'] == 'lifetime_uninstalls')]['Values'].values[0] 

    return today_paid_installs, todays_free_installs, lifetime_installs, today_paid_uninstalls, today_free_uninstalls, lifetime_uninstalls 




# Odyessey comparison overview part
def odyssey_overview(df):
    todays_forge_installs = df[(df['Product'] == 'odyssey') & (df['Matrix'] == 'todays_forge_installs')]['Values'].values[0] 
    todays_free_installs = df[(df['Product'] == 'odyssey') & (df['Matrix'] == 'todays_free_installs')]['Values'].values[0] 
    lifetime_installs = df[(df['Product'] == 'odyssey') & (df['Matrix'] == 'lifetime_installs')]['Values'].values[0] 
    todays_forge_uninstalls= df[(df['Product'] == 'odyssey') & (df['Matrix'] == 'todays_forge_uninstalls')]['Values'].values[0] 
    today_free_uninstalls = df[(df['Product'] == 'odyssey') & (df['Matrix'] == 'today_free_uninstalls')]['Values'].values[0] 
    lifetime_uninstalls = df[(df['Product'] == 'odyssey') & (df['Matrix'] == 'lifetime_uninstalls')]['Values'].values[0] 

    return todays_forge_installs, todays_free_installs, lifetime_installs, todays_forge_uninstalls, today_free_uninstalls, lifetime_uninstalls
















# def plot_histograms_zeniva(product_name, platform_name):
#     # Load and preprocess the data
#     df = pd.read_csv(combined_Data)
#     df = df.fillna(0)
#     df = df[df['product'] == product_name]

#     platform_metrics = {
#         'youtube': ['clicks', 'views', 'daily_spend'],
#         'meta': ['clicks', 'reach', 'daily_spend'],
#         'shopify': ['clicks', 'daily_spend', 'dummy_metric'],  # Add dummy metric for Shopify
#         'ppc': ['clicks', 'daily_spend', 'impressions'],
#     }

#     if platform_name in platform_metrics:
#         selected_metrics = platform_metrics[platform_name]
#     else:
#         st.error(f"Platform {platform_name} not recognised.")
#         return

#     df_platform = df[df['platform'] == platform_name]

#     # Convert 'date' column to datetime format for easier comparison
#     df_platform['date'] = pd.to_datetime(df_platform['date'], format='%m/%d/%Y')

#     # Get the latest date available for the selected platform
#     if df_platform.empty:
#         st.error(f"No data available for platform {platform_name}.")
#         return

#     latest_date = df_platform['date'].max()

#     # Get the last 3 available dates based on the latest date
#     dates = [latest_date - timedelta(days=i) for i in range(3)]
    
#     # Ensure formatted dates match the datetime format in the dataframe
#     formatted_dates = [date.strftime("%m-%d-%y") for date in dates]

#     # Filter the dataframe to include only the last 3 available dates
#     df_filtered = df_platform[df_platform['date'].isin(dates)]

#     # Create placeholders for missing dates if less than 3 are available
#     available_dates = df_filtered['date'].dt.strftime('%m-%d-%y').unique().tolist()
#     missing_dates = [date for date in formatted_dates if date not in available_dates]

#     # If no data exists for the last 3 days, fall back to available dates
#     if df_filtered.empty:
#         st.error("No data available for the last 3 days.")
#         return

#     # Add dummy metric for Shopify to ensure consistent bar width
#     if 'dummy_metric' in selected_metrics:
#         df_filtered['dummy_metric'] = 0

#     # Reshape the dataframe for plotting
#     df_grouped = df_filtered[['date'] + selected_metrics].melt(id_vars='date', var_name='Metric', value_name='Value')

#     # Define color mapping for metrics
#     color_discrete_map = {
#         'clicks': '#BC679C',
#         'views': '#F68C5B',
#         'daily_spend': '#A6B174',
#         'reach': '#F68C5B',
#         'impressions': '#F68C5B',
#         'dummy_metric': '#FFFFFF'  # Invisible color for the dummy metric
#     }

#     label_map = {
#             'clicks': 'Clicks',
#             'views': 'Views',
#             'daily_spend': 'Daily Spend',
#             'reach': 'Reach',
#             'impressions': 'Impressions',
#             'dummy_metric': ''  # No label for the dummy metric
#         }

#     # Plot histogram
#     fig = px.histogram(
#         df_grouped, 
#         x='date', 
#         y='Value', 
#         color='Metric', 
#         barmode='group', 
#         height=220,
#         width=620,
#         color_discrete_map=color_discrete_map,
#     )

#     fig.for_each_trace(lambda trace: trace.update(name=label_map.get(trace.name, trace.name)))

#     # Extract unique dates for the x-axis and format them
#     unique_dates = df_grouped['date'].dt.to_period('D').astype('str').unique()
#     formatted_dates = [pd.to_datetime(date).strftime('%d %B') for date in unique_dates]

#     # Update the layout to format x-axis labels
#     fig.update_layout(
#         xaxis=dict(
#             tickvals=pd.to_datetime(unique_dates).to_pydatetime(),  # Set tick values to unique dates
#             ticktext=formatted_dates,  # Format tick text
#             ticklabelposition="outside",  # Position the labels outside the plot area
#             tickson="labels",  # Ensure ticks are aligned with labels
#             title_standoff=24,  # Increase space between x-axis title and labels
#             ticks="outside",  # Ensure ticks are outside the plot area
#             tickfont=dict(size=7),
#         ),
#         plot_bgcolor='rgba(0,0,0,0)',  # Transparent background for the plot area
#         paper_bgcolor='rgba(0,0,0,0)',  # Transparent background for the whole figure
#         font_color='white',
#         bargap=0.4,  # Adjust the gap between bars
#         bargroupgap=0.3,  # Adjust the gap between groups of bars
#         yaxis=dict(
#             showgrid=False  # Disable horizontal grid lines
#         ),
#         xaxis_title=None,
#         yaxis_title=None,
#     )

#     # Update the layout to add border-radius effect
#     fig.update_traces(marker=dict(
#         line=dict(
#             width=5,
#             color='rgba(0,0,0,0)'  # Optional: border color
#         ),
#         opacity=0.9  # Optional: adjust bar opacity
#     ))

#     # Update legend settings
#     fig.update_layout(
#         legend={
#             "orientation": "h",
#             "yanchor": "bottom",
#             "y": -0.5,
#             "xanchor": "center",
#             "x": 0.5,
#             "font": {
#                 "color": "white",  # Legend text color
#                 "size": 7    # Increase the font size as needed
#             },
#         },
#         legend_title_text=""
#     )

#     # Convert figure to HTML and return
#     fig_html = fig.to_html(include_plotlyjs='cdn', config={'displayModeBar':False})
#     return fig_html

