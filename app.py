# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 20:19:05 2019

@author: MEvans
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#import feather as ft
import functions as fxn
import figures as figs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H2(children='Tortoise Prioritization'),

    html.Div(children=[
            html.H3('How do we value habitat?'),
            html.P("The Bureau of Land Management is conducting a programatic environmental assessment for the Southern Nevada District that will identify conflicts between solar energy development and other public land uses & resources.  Public lands will ultimately be categorized into different levels of conflict."),
            html.P( "Typically, prioritization is achieved by looking at the distribution of , and dividing these observed values into 'bins.'  What we present below is a more transparent and explicit way of translating the values into scores.")
            ]),

    html.Div([
        html.P("This graph shows functions that represent different ways we might value habitat suitability and connectivity."),
        dcc.Graph(
            id='example-graph',
            figure = figs.example
        )]),
            
    html.Div(children = [
            html.Div([
                html.Label('Suitability weight'),
    
                dcc.Slider(
                        id = 'suit-slider',
                        min=0,
                        max=5,
                        marks={i: '{}'.format(i) for i in range(6)},
                        value=2
                        )
                ], style = {'width' : '48%', 'display': 'inline-block'}),

            html.Div([                        
                html.Label('Connectivity weight'),
                
                dcc.Slider(
                        id = 'conn-slider',
                        min = 0,
                        max = 5,
                        marks = {i: '%s'% i for i in range(6)},
                        value = 1
                        )
                ], style = {'width' : '48%', 'float': 'right', 'display': 'inline-block'}),
                
                html.Div(dcc.Graph(id = 'grid_plot'))
            ])
    

    
])
                
@app.callback(
        Output('grid_plot', 'figure'),
        [Input('suit-slider', 'value'),
         Input('conn-slider', 'value')])
def update_graph(suitability, connectivity):
    return fxn.plot_grid(suitability, connectivity)

if __name__ == '__main__':
    app.run_server(debug=False)