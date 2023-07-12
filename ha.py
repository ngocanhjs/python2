from dash import html
from dash import dcc
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import plotly.graph_objects as go
import plotly.express as px
from matplotlib import cm
from pandas.core.apply import frame_apply
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
data = pd.read_csv('https://raw.githubusercontent.com/ngocanhjs/python2/main/data.csv') 

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
    title='Top 5 countries with the most TV shows (1970-2020)',
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
            html.Hr(),
            # Sidebar
            dbc.Nav(
                [
                    dbc.NavLink("Bar Chart", href="#", id="bar-chart-link"),
                    dbc.NavLink("Box Chart", href="#", id="box-chart-link"),
                    dbc.NavLink("Pie Chart", href="#", id="pie-chart-link"),
                    dbc.NavLink("Scatter Plot", href="#", id="scatter-plot-link"),
                    dbc.NavLink("ALL", href="#", id="link-all"),
                ],
                vertical=False,
                pills=True,
            ),
        ], md=15),
        dbc.Col([
            html.Div(id="content"),
        ], md=15),
    ]),
], fluid=True)

# Callbacks to update content based on sidebar click
@app.callback(
    Output("content", "children"),
    [Input("bar-chart-link", "n_clicks"),
     Input("box-chart-link", "n_clicks"),
     Input("pie-chart-link", "n_clicks"),
     Input("scatter-plot-link", "n_clicks"),
     Input("link-all","n-clicks")]
)
def update_content(bar_chart_clicks, box_chart_clicks, pie_chart_clicks, scatter_plot_clicks,link_all_clicks):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "bar-chart-link":
        return html.Div([
            html.H2('The Distribution of Main Genre', style={'text-align': 'center', 'color': 'black'}),
            html.H5('THE BAR CHART'),
            html.P('Number of countries:'),
            dcc.Slider(id='slider', min=1, max=5, step=1, value=5),
            dcc.Graph(id='plot-bar'),
        ])
    elif button_id == "box-chart-link":
        return html.Div([
            html.H2('The Distribution of Main Genre', style={'text-align': 'center', 'color': 'black'}),
            html.H5('THE MAIN BOX CHART', style={'text-align': 'center'}),
            dcc.Graph(id='plot-box', style={'height': 950}),
        ])
        
    elif button_id == "link-all":
        return html.Div([
            html.H1('NETFLIX TV SHOW DATA VISUALIZATION', style={'text-align': 'center'}),
        html.H6("This interactive web application includes a bar chart visualizing the top 5 countries with the highest Netflix TV show production, as well as a box chart displaying the distribution of scores within different genres. Users can interact with the slider and dropdown menu to explore the data.",
                style={'text-align': 'center', 'color': 'lightblack', 'font-style': 'italic'}),
        html.A('Click here for more information', href='https://www.netflix.com/',
               style={'text-align': 'center', 'color': 'blue','font-style': 'italic','font-size': '14px'}),
   
    dbc.Row([ html.Hr(),
        html.H2('The Distribution of Main Genre', style={'text-align': 'center', 'color': 'black'}),
             html.Hr(),
        dbc.Col([
            
            html.H4('THE BAR CHART'),
            html.P('Number of countries:'),
            dcc.Slider(id='slider', min=1, max=5, step=1, value=5),
            dcc.Graph(id='plot-bar', figure=fig_bar)
        ], md=6),
        dbc.Col([
            
            html.H4('THE PIE CHART'),
            html.H5('Number of countries:'),
            html.H5('All the country'),
            html.H6('nfjsfdsgdsgsdgdsgsgsgjghsjkdhsidvmkcvmskgjidgskcmvkjpfoakspfalfm,lcdm,lfkpdfkpflmdlgmdog'),
            dcc.Graph(id='plot-pie', figure=fig_pie)
        ], md=6)
    ]),
    html.Hr(),
    dbc.Row([
        html.H2('The Distribution of Main Genre', style={'text-align': 'center', 'color': 'black'}),
        html.Hr(),
        dbc.Col([
            
            html.H4('THE BOX CHART'),
            html.H5('Number of countries:'),
            dcc.Graph(id='plot-box', figure=fig_box, style={'height': 700}),
        ], width=6),
        dbc.Col([
            html.H4('THE SCATTER PLOT'),
            html.H6('Select genre that you want to see:'),
            dcc.Dropdown(
                id='dropdown',
                options=[{"label": option, "value": option} for option in data["MAIN_GENRE"].unique()],
                value="drama"
            ),
            dcc.Graph(id="plot-sub-box", style={'height': 700}),
        ], width=6)
    ])
                        ])
    elif button_id == "pie-chart-link":
        return html.Div([
            html.H2('The Distribution of Main Genre', style={'text-align': 'center', 'color': 'black'}),
            html.H5('THE PIE CHART'),
            dcc.Graph(id='plot-pie'),
        ])
    elif button_id == "scatter-plot-link":
        return html.Div([
            html.H2('The Distribution of Main Genre', style={'text-align': 'center', 'color': 'black'}),
            html.H5('THE SCATTER PLOT', className='text-center'),
            html.H6('Select genre that you want to see:', className='text-center'),
            dcc.Dropdown(
                id='dropdown',
                options=[{"label": option, "value": option} for option in data["MAIN_GENRE"].unique()],
                value="drama"
            ),
            dcc.Graph(id="plot-sub-box"),
        ])
    else:
        return html.Div([
            html.H2('The Distribution of Main Genre', style={'text-align': 'center', 'color': 'black'}),
            html.H5('THE BAR CHART'),
            html.P('Number of countries:'),
            dcc.Slider(id='slider', min=1, max=5, step=1, value=5),
            dcc.Graph(id='plot-bar'),
        ])
# Callback to update the bar chart based on the slider value
@app.callback(Output('plot-bar', 'figure'), [Input('slider', 'value')])
def update_bar_chart(value):
    df1 = df_bar.nlargest(n=value, keep='all').sort_values(ascending=False)
    fig_bar.update_layout(title='Top {} countries that have the most TV shows in the period 1970 - 2020'.format(value))
    fig_bar.update_traces(y=df1.values, x=df1.index)
    return fig_bar

# Callback to update the scatter plot based on the dropdown selection
@app.callback(Output('plot-sub-box', 'figure'), [Input('dropdown', 'value')])
def update_scatter_plot(genre_selection):
    data_subset = data.loc[data['MAIN_GENRE'] == genre_selection]
    fig = px.scatter(
        data_subset,
        x="RELEASE_YEAR",
        y="SCORE",
        color="MAIN_GENRE",
        title=f"The scatter plot for {genre_selection} genre",
        color_discrete_map={genre: color for genre, color in zip(data['MAIN_GENRE'].unique(), colors)}
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
