import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# load datasets
df = pd.read_csv('WHOcovidglobal.csv')
cases_deaths_df = pd.read_csv('covidcases.csv')

# Initialise the app
app = dash.Dash(__name__)

# figure containing choropleth map
fig = go.Figure(data=go.Choropleth(
    locations=df['Name'],
    locationmode='country names',
    z=df['Cases - cumulative total'],
    marker_line_color='white',
    marker_line_width=1,
    colorscale='tealgrn',
    colorbar=dict(title='Cumulative COVID-19 Cases'),
    zmin=0,
    zmax=25000000
))

# the base map
fig.update_geos(
    projection_type="natural earth",
    framecolor='grey',
    landcolor='rgb(230,230,230)',
    coastlinecolor='white',
    scope='world',
    showocean=False,
    showlakes=False,
    resolution=110,
    framewidth=0,
)

fig.update_layout(
    margin={"r": 10, "t": 10, "l": 10, "b": 10},
    paper_bgcolor='#ffffff',
    width=1280,
    height=720
)

# Define the app, the main div containing all components
app.layout = html.Div(children=[

    # app header
    html.H1('Travel Buddy', style={
        'color': 'white',
        'font-size': '48',
        'font': 'Arial, sans-serif'
    }),

    # div containing the graph
    html.Div(children=[

        # the graph
        dcc.Graph(figure=fig, style={
            'display': 'inline-block',
            'margin': 'auto',
            "overflow": "hidden",
            'border-radius': 20,
            'box-shadow': '2px 2px 10px  #191818'
        }),

    ], style={
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center',
    }),

    html.Br(),

    # text input
    dcc.Input(id='country-search', type='text', value='Afghanistan', placeholder='Where would you like to go?', style={
        'display': 'block',
        'margin': 'auto',
        'width': '50%',
        'height': 30,
        'border-radius': 20,
        'border-style': 'none',
        'box-shadow': '2px 2px 10px  #191818'
    }),
    html.Br(),

    # div containing information that was searched for
    html.Div(dcc.Graph(id='new cases and deaths')),
    html.Div(dcc.Graph(id='cumulative cases and deaths'))
]

    # style for main div containing all other components (the background)
    , style={
        'background-color': '#404040',
        'height': 'auto',
        'width': 'auto',
        'padding-bottom': 10
    })


# returns linechart for covid deaths and cases of a country
# output is returned to graph with id of 'cases and deaths'
# input taken from search bar
@app.callback(
    Output('new cases and deaths', 'figure'),
    Input('country-search', 'value')
)
def new_cases_and_deaths_linechart(country_search):
    # filter data for selected country
    filtered_df = cases_deaths_df[cases_deaths_df['Country'] == country_search]

    # create line chart
    trace1 = go.Scatter(x=filtered_df['Date_reported'], y=filtered_df['New_cases'], mode='lines', name='New Cases')
    trace2 = go.Scatter(x=filtered_df['Date_reported'], y=filtered_df['New_deaths'], mode='lines', name='New Deaths')
    linedata = [trace1, trace2]

    return {'data': linedata, 'layout': go.Layout(
        title={'text': 'New Covid Cases and Deaths in ' + country_search, 'font_color': 'white'},
        paper_bgcolor='#404040',
        plot_bgcolor='#404040',
        yaxis={'color': 'white'},
        xaxis={'color': 'white'},
        legend={'font_color': 'white'}
    )}

@app.callback(
    Output('cumulative cases and deaths', 'figure'),
    Input('country-search', 'value')
)
def cumulative_cases_and_deaths_linechart(country_search):
    # filter data for selected country
    filtered_df = cases_deaths_df[cases_deaths_df['Country'] == country_search]

    # create line chart
    trace1 = go.Scatter(x=filtered_df['Date_reported'], y=filtered_df['Cumulative_cases'], mode='lines',
                        name='Cumulative Cases')
    trace2 = go.Scatter(x=filtered_df['Date_reported'], y=filtered_df['Cumulative_deaths'], mode='lines',
                        name='Cumulative Deaths')
    linedata = [trace1, trace2]

    return {'data': linedata, 'layout': go.Layout(
        title={'text': 'Cumulative Covid Cases and Deaths in ' + country_search, 'font_color': 'white'},
        paper_bgcolor='#404040',
        plot_bgcolor='#404040',
        yaxis={'color': 'white'},
        xaxis={'color': 'white'},
        legend={'font_color': 'white'}
    )}


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
