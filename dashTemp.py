import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
import base64
import os

image_filename = 'my-image.png'  # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


app = dash.Dash(__name__)

secondDiv = html.Div(children=[
                                html.Div(children=[html.Div(children=[
                                    html.H6(children='clustering parameters')]),
                                    html.Div(id="abc", children=[html.H5(children='Δt'),

                                                                 dcc.Slider(
                                                                     id='my-slider',
                                                                     min=0,
                                                                     max=100,
                                                                     step=0.5,
                                                                     value=30,

                                                                 ), html.H6(children='Enter Δt max'),dcc.Input(id='deltaTmax', placeholder='Δt max',
                                                                              value='60', type='text'),
                                                                 html.Div(id='slider-output-t')]),
                                    html.Div(children=[html.H5(children='Δd'),
                                                       dcc.Slider(
                                                           id='my-slider2',
                                                           min=0,
                                                           max=100,
                                                           step=0.5,
                                                           value=10
                                                       ), html.H6(children='Enter Δd max'),dcc.Input(id='deltaDmax', placeholder='Δd max', type='text',value='100'),
                                                       html.Div(id='slider-output-d')])
                                ], style={'width': '30%', 'float': 'right', "border": "2px black solid",
                                          'border-radius': '25px'}),html.Div(children=[ html.Div([
        html.H3('Column 2'),
        dcc.Graph(id='g3', figure={'data': [{'y': [1, 2, 3]}]}),
    ], style={'width': '35%', 'float': 'left'}),

    html.Div([
        html.H3('Column 3'),

        html.Img(id="body-image", src='data:image/png;base64,{}'.format(encoded_image.decode()))
    ], style={'width': '35%', 'float': 'right'})], style={'width': '80%',"margin-top":"60px", 'float': 'left', "border": "2px black solid"})])

app.layout=secondDiv





@app.callback(
    dash.dependencies.Output('slider-output-t', 'children'),
    [dash.dependencies.Input('my-slider', 'value')])
def t2(value):
    return 'Δt=' + str(value) + ' s'


@app.callback(
    dash.dependencies.Output('my-slider', 'min'),
    [dash.dependencies.Input('my-slider', 'max')])
def t2(v):
    return int(v)/1000


@app.callback(
    dash.dependencies.Output('my-slider', 'max'),
    [dash.dependencies.Input('deltaTmax', 'value')])
def k2(value):
    if value == '':
        while value == '':
            1 == 1
    value=value.lower()
    value.replace(" ", "")
    if value.endswith("j"):
        value = value[:-1]
        value.replace(" ", "")
        value = int(value)
        value = 24 * 3600 * value
        return value
    if value.endswith("h"):
        value = value[:-1]
        value.replace(" ", "")
        value = int(value)
        value = 3600 * value
        return value
    if value.endswith("s"):
        value = value[:-1]
        value.replace(" ", "")
        value = int(value)
        value = 3600 * value
        return value
    return int(value)


@app.callback(
    dash.dependencies.Output('slider-output-d', 'children'),
    [dash.dependencies.Input('my-slider2', 'value')])
def t2(value):
    return 'Δd=' + str(value) + ' m'


@app.callback(
    dash.dependencies.Output('my-slider2', 'min'),
    [dash.dependencies.Input('my-slider2', 'max')])
def t2(v):
    return int(v)/1000


@app.callback(
    dash.dependencies.Output('my-slider2', 'max'),
    [dash.dependencies.Input('deltaDmax', 'value')])
def k2(value):
    if value == '' :
        while value == '' :
            1 == 1
    value=value.lower()
    value.replace(" ", "")
    if value.endswith("km") :
        value = value[:-2]
        value.replace(" ", "")
        value = int(value)
        value = 1000 * value
        return value
    if value.endswith("m"):
        value = value[:-1]
        value.replace(" ", "")
        value = int(value)
        return value
    if  value.endswith('k'):
        value = value[:-1]
        value.replace(" ", "")
        value = int(value)
        value = 1000 * value
        return value
    return int(value)



@app.callback(Output("body-image", "src"),
              [Input('my-slider', 'value'),Input('my-slider2', 'value')])
def update_body_image(value1,value2):
    image_filename = 'poisson.png'  # replace with your own image
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    src = 'data:image/png;base64,{}'.format(encoded_image.decode())
    return src


if __name__ == '__main__':
    app.run_server(debug=True)
