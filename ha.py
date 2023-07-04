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
data = pd.read_csv('https://raw.githubusercontent.com/ngocanhjs/lancuoi/main/data.csv') 


fig = px.box(data,x="MAIN_GENRE", y="SCORE",color = "MAIN_GENRE", title="The box chart demonstrates the distribution of range score of TV shows according to TV show genres")
med_score = data.groupby('MAIN_GENRE')['SCORE'].median().sort_values()
sorted_genre = med_score.index.tolist()
fig.update_layout(xaxis=dict(categoryorder='array', categoryarray=sorted_genre))

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

app.layout = dbc.Container(
    [
        
        dbc.Row([
          
            dbc.Col([
                html.Hr(),
                html.H5('NETFLIX TV SHOW DATA VISUALIZATION', className='text-center'),
                dcc.Graph(id='plot',
                          figure= fig,
                          style={'height':750},
                          ),
            ],
                width={'size': 9, 'offset': 0, 'order': 2}),
            # Second column
            dbc.Col([
                html.Hr(),
                html.H5('Select genre that you want see:', className='text-center'),
                html.Hr(),
                dcc.Dropdown(
                    id='dropdown',
                    options=[{"label": option, "value" : option}for option in data["MAIN_GENRE"].unique()],
                    value="drama"
                ),
                dcc.Graph(id="graph")])
    ])])
@app.callback(Output("graph", "figure"), [Input("dropdown", "value")])
def update_chart(MAIN_GENRE_selection):
    # create a filtered dataframe based on the genre selection
    data_subset = data.loc[data["MAIN_GENRE"] == MAIN_GENRE_selection]
    # create a new figure for the genre selection
    fig = px.box(data_subset, x="MAIN_GENRE", y="SCORE", color="MAIN_GENRE", title=f"The chart for {MAIN_GENRE_selection} genre")
    return fig

# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
