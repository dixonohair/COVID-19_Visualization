import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# load dataset
df = pd.read_csv('WHOcovidglobal.csv')
# Initialise the app
app = dash.Dash(__name__)

# Define the app
app.layout = html.Div(children=[

    html.Div(children=[
        html.H1('Travel Buddy', style={
            'color': 'White'
        }),
        html.Br(),
        html.Div(dcc.Graph(id='graph', style={
            'display': 'block',
            'margin': 'auto'
        }), style={
            'background-color': 'white',
            'width': '100%',
            'height': 'auto',
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center'
        }),
        html.Br(),
        dcc.Dropdown(id='input', value='europe', style={
            'width': '90%',
            'display': 'block',
            'margin': 'auto',
            'padding-bottom': 10
        }, options=[
            {'label': 'North America', 'value': 'north america'},
            {'label': 'South America', 'value': 'south america'},
            {'label': 'Europe', 'value': 'europe'},
            {'label': 'Asia', 'value': 'asia'},
            {'label': 'Africa', 'value': 'africa'}
        ]),
    ], style={
        'background-color': 'transparent',
        'border-radius': 10,
        'padding-bottom': 10,
        'width': '100%',
        'height': 'auto',
        # 'box-shadow': '2px 2px 10px black'
    }),

], style={
    'background-color': '#363636',
    'height': '100vh',
    'width': 'auto',
})


@app.callback(Output('graph', 'figure'), Input('input', 'value'))
def covid_info(country):
    fig = go.Figure(data=go.Choropleth(
        locations=df['Name'],
        locationmode='country names',
        z=df['Cases - cumulative total'],
        marker_line_color='grey',
        marker_line_width=.2,
        colorscale='algae',
        colorbar=dict(title='Cumulative COVID-19 Cases'),
        zmin=0
    ))
    # the base map
    fig.update_geos(
        projection_type="mercator",
        bgcolor='blue',
        framecolor='grey',
        landcolor='rgb(230,230,230)',
        coastlinecolor='white',
        scope=country,
        showocean=False,
        showlakes=False,
        resolution=110
    )
    fig.update_layout(
        height=700,
        width=800,
        margin={"r": 0, "t": 5, "l": 0, "b": 5},
        paper_bgcolor='rgba(255, 0, 0, 0.0)'
    )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
