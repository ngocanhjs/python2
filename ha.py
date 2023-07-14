import dash

import dash_bootstrap_components as dbc

from dash import html

from dash import dcc

from dash.dependencies import Input, Output

import pandas as pd

import plotly.express as px

import plotly.graph_objects as go



# Read the CSV data
data = pd.read_csv('https://raw.githubusercontent.com/ngocanhjs/1031/main/data.csv')

# Create the bar chart
df_bar = data['MAIN_PRODUCTION'].value_counts().nlargest(n=5, keep='all').sort_values(ascending=False)
trace_bar = go.Bar(
    y=df_bar.values,
    x=df_bar.index,
    orientation='v',
    marker=dict(
        color=['goldenrod', 'hotpink', 'chocolate', 'lawngreen', 'dodgerblue']
    )
)
data_bar = [trace_bar]
layout_bar = go.Layout(
    title='Top 10 countries with the most TV shows (1970-2020)',
    xaxis=dict(title='Main Production'),
    yaxis=dict(title='Number of TV shows'),
    height=400
)
fig_bar = go.Figure(data=data_bar, layout=layout_bar)

# Create the box chart
fig_box = px.box(
    data,
    x="MAIN_GENRE",
    y="SCORE",
    color="MAIN_GENRE",
    title="The box chart demonstrates the distribution of range score of TV shows according to TV show genres",
    color_discrete_map={genre: color for genre, color in zip(data['MAIN_GENRE'].unique(), ['goldenrod', 'hotpink', 'chocolate', 'lawngreen', 'dodgerblue'])}
)
med_score = data.groupby('MAIN_GENRE')['SCORE'].median().sort_values()
sorted_genre = med_score.index.tolist()
fig_box.update_layout(xaxis=dict(categoryorder='array', categoryarray=sorted_genre))

# Create the pie chart
country_df = data['MAIN_PRODUCTION'].value_counts().reset_index()
country_df = country_df[country_df['MAIN_PRODUCTION'] / country_df['MAIN_PRODUCTION'].sum() > 0.01]
fig_pie = px.pie(
    country_df,
    values='MAIN_PRODUCTION',
    names='index',
    color_discrete_sequence=['goldenrod', 'hotpink', 'chocolate', 'lawngreen', 'dodgerblue']
)
fig_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='white', width=1)))
fig_pie.update_layout(height=600)

# Create the scatter plot
fig_scatter = px.scatter(
    data,
    x="RELEASE_YEAR",
    y="SCORE",
    color="MAIN_GENRE",
    title="The scatter plot shows the scores of TV shows by genre",
    color_discrete_map={genre: color for genre, color in zip(data['MAIN_GENRE'].unique(), ['goldenrod', 'hotpink', 'chocolate', 'lawngreen', 'dodgerblue'])}
)

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('NETFLIX TV SHOW DATA VISUALIZATION', style={'text-align': 'center'}),
            html.H6("This interactive web application includes a bar chart visualizing the top 5 countries with the highest Netflix TV show production, as well as a box chart displaying the distribution of scores within different genres. Users can interact with the slider and dropdown menu to explore the data.",
                    style={'text-align': 'center', 'color': 'lightblack', 'font-style': 'italic'}),
            html.A('Click here for more information', href='https://www.netflix.com/',
                   style={'text-align': 'center', 'color': 'blue', 'font-style': 'italic', 'font-size': '14px'}),
            html.Hr(),
            # Sidebar
            dbc.Nav(
                [
                    dbc.NavLink("Bar Chart", href="#", id="bar-chart-link"),
                    dbc.NavLink("Box Chart", href="#", id="box-chart-link"),
                    dbc.NavLink("Pie Chart", href="#", id="pie-chart-link"),
                    dbc.NavLink("Scatter Plot", href="#", id="scatter-plot-link"),
                    dbc.NavLink("New Content", href="#", id="new-content-link"),  # New content link
                ],
                vertical=False,
                pills=True,
            ),
        ], md=15),
        dbc.Col([
            html.Div(id="content"),
        ], md=13),
    ]),
], fluid=True)

# Callbacks to update content based on sidebar click
...
...

elif button_id == "new-content-link":  # Check if the clicked button is the "New Content" link
    return html.Div([
        html.H2('New Content', style={'text-align': 'center', 'color': 'black'}),  # Heading for new content
        html.P("kakakakakakakkaak", style={'text-align': 'center', 'font-weight': 'bold', 'font-size': '20px'}),  # New content
    ])

...
...

if __name__ == '_main_':
    app.run_server(debug=True)
