import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from dash.dependencies import Input, Output


# load datasets
df = pd.read_csv('WHOcovidglobal.csv')
cases_deaths_df = pd.read_csv('covidcases.csv')
vaccinations_df = pd.read_csv('vaccinations.csv')
travel_advisories_df = pd.read_csv('covid19TravelRestrictionsCountry.csv')


# Initialise the app
app = dash.Dash(__name__)

# figure containing choropleth map
fig = go.Figure(data=go.Choropleth(
    locations=df['Name'],
    locationmode='country names',
    z=df['Cases - newly reported in last 7 days per 100000 population'],
    marker_line_color='white',
    marker_line_width=1,
    reversescale= True,
    colorscale='RdYLGn',
    colorbar=dict(title='Covid cases in the last 7 days per 100000'),
    zmin=0,
    zmax=600
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
        'padding': 10,
        'width': 'auto',
        'background-color': '#303030',
        'box-shadow': '2px 2px 5px #191818'
    }),

    html.H1('Global Covid Data: At a Glance', style={
        'color': 'white',
        'font-size': 50,
        'margin-left': '50px'
    }),

    # div containing the world map
    html.Div(children=[

        # the graph
        dcc.Graph(figure=fig, style={
            'display': 'inline-block',
            'margin': 'auto',
            "overflow": "hidden",
            'box-shadow': '2px 2px 10px  #191818',
            'border-radius': '5px'
        }),

    ], style={
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center',
    }),

    html.Br(),

    html.H1('Covid Data by Country', style={
        'color': 'white',
        'margin-left': '50px',
        'font-size': 48
    }),
    html.Br(),

    # text input
    dcc.Input(id='country-search', type='text', value='Japan', placeholder='Enter a country...', style={
        'display': 'block',
        'margin': 'auto',
        'width': '50%',
        'height': 30,
        'border-style': 'none',
        'box-shadow': '2px 2px 10px  #191818',
        'border-radius': 20
    }),
    html.Br(),
    html.H1('Travel Advisory Information', style={
        'color': 'white',
        'margin-left': '90px',
        'font-size': '36px'
    }),
    # div containing information that was searched for
    html.Div(id='travel advisories'),
    html.Br(),

    html.H1('Covid Data', style={
        'color': 'white',
        'margin-left': '90px',
        'font-size': '36px'
    }),

    # div for new cases and deaths chart
    html.Div(dcc.Graph(id='new cases and deaths')),
    html.Br(),

    # div for cumulative cases and deaths chart
    html.Div(dcc.Graph(id='cumulative cases and deaths')),
    html.Br(),

# div for vaccinations chart
    html.Div(dcc.Graph(id='vaccinations')),
    html.Br()


]

    # style for main div containing all other components (the background)
    , style={
        'background-color': '#404040',
        'height': 'auto',
        'width': 'auto',
        'padding-bottom': 10,
        'font-family': 'Segoe UI, sans-serif'
    })


# returns linechart for covid deaths and cases of a country
# output is returned to graph with id of 'cases and deaths'
# input taken from search bar
@app.callback(Output('new cases and deaths', 'figure'), Input('country-search', 'value'))
def new_cases_and_deaths_linechart(country_search):
    # filter data for selected country
    filtered_df = cases_deaths_df[cases_deaths_df['Country'] == country_search]

    # create line chart
    trace1 = go.Scatter(x=filtered_df['Date_reported'], y=filtered_df['New_cases'], mode='lines', name='New Cases',
                        line={'color': 'salmon', 'width': 2})
    trace2 = go.Scatter(x=filtered_df['Date_reported'], y=filtered_df['New_deaths'], mode='lines', name='New Deaths',
                        line={'color': '#ccccff', 'width': 2})
    linedata = [trace1, trace2]

    return {'data': linedata, 'layout': go.Layout(
        title={'text': 'New Covid Cases and Deaths in ' + country_search, 'font_color': 'white'},
        paper_bgcolor='#404040',
        plot_bgcolor='#404040',
        yaxis={'color': 'white'},
        xaxis={'color': 'white'},
        legend={'font_color': 'white'}
    )}


@app.callback(Output('cumulative cases and deaths', 'figure'), Input('country-search', 'value'))
def cumulative_cases_and_deaths_linechart(country_search):
    # filter data for selected country
    filtered_df = cases_deaths_df[cases_deaths_df['Country'] == country_search]

    # create line chart
    trace1 = go.Scatter(x=filtered_df['Date_reported'], y=filtered_df['Cumulative_cases'], mode='lines',
                        name='Cumulative Cases', line={'color': '#8cf5b4', 'width': 2})
    trace2 = go.Scatter(x=filtered_df['Date_reported'], y=filtered_df['Cumulative_deaths'], mode='lines',
                        name='Cumulative Deaths', line={'color': '#e2ff68', 'width': 2})
    linedata = [trace1, trace2]

    return {'data': linedata, 'layout': go.Layout(
        title={'text': 'Cumulative Covid Cases and Deaths in ' + country_search, 'font_color': 'white'},
        paper_bgcolor='#404040',
        plot_bgcolor='#404040',
        yaxis={'color': 'white'},
        xaxis={'color': 'white'},
        legend={'font_color': 'white'},
    )}


@app.callback(Output('vaccinations', 'figure'), Input('country-search', 'value'))
def vaccinations_linechart(country_search):
    # filter data for selected country
    filtered_vaccinations_df = vaccinations_df[vaccinations_df['location'] == country_search]
    # create line chart
    trace1 = go.Scatter(x=filtered_vaccinations_df['date'], y=filtered_vaccinations_df['total_vaccinations'],
                        mode='lines',
                        name='Total Vaccinations', line={'color': '#8cf5b4', 'width': 2})
    trace2 = go.Scatter(x=filtered_vaccinations_df['date'], y=filtered_vaccinations_df['daily_vaccinations'],
                        mode='lines',
                        name='Daily Vaccinations', line={'color': '#e2ff68', 'width': 2})
    linedata = [trace1, trace2]

    return {'data': linedata, 'layout': go.Layout(
        title={'text': 'Vaccinations in ' + country_search, 'font_color': 'white'},
        paper_bgcolor='#404040',
        plot_bgcolor='#404040',
        yaxis={'color': 'white'},
        xaxis={'color': 'white'},
        legend={'font_color': 'white'},
    )}


# callback to get travel advisory for country
@app.callback(Output('travel advisories', 'children'), Input('country-search', 'value'))
def travel_advisories(country_search):
    # filter data for selected country
    filtered_df = travel_advisories_df[travel_advisories_df['Country'] == country_search]

    # return paragraph containing latest news
    return html.P(filtered_df['info'], style={
        'color': 'white',
        'width': '80%',
        'margin': 'auto',
        'display': 'block'
    })


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
