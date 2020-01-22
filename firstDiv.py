# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import back
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc

# external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, suppress_callback_exceptions=True,)

colors = {"background": "#FFFFFF", "text": "#7FDBFF"}

graphs = html.Div(
    children=[
        html.Div(
            id="selectLabel",
            style={
                "float": "right",
                "width": "50%",
                "height": "30px",
                "margin": "10px",
            },
        ),
        html.Div(
            id="slider",
            style={
                "float": "right",
                "width": "50%",
                "height": "30px",
                "margin": "10px",
            },
        ),
        html.Div(
            children=[
                dcc.Graph(id="2d", style={"float": "right", "width": "50%",}),
                dcc.Graph(id="time", style={"float": "left", "width": "50%"}),
            ],
        ),
    ],
)

upload = dcc.Upload(
    id="upload",
    children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
    style={
        "float": "left",
        "width": "30%",
        "height": "60px",
        "lineHeight": "60px",
        "borderWidth": "1px",
        "borderStyle": "dashed",
        "borderRadius": "5px",
        "textAlign": "center",
    },
    # Allow multiple files to be uploaded
    multiple=True,
)

deroul = dcc.Dropdown(id=" selectLabel", multi=True,)

firstDiv = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.H1(children="ok", style={"textAlign": "center", "color": colors["text"]},),
        upload,
        graphs,
    ],
)


secondDiv = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.H1(
            children="tet", style={"textAlign": "center", "color": colors["text"]},
        ),
    ],
)

total = html.Div

app.layout = firstDiv


@app.callback(
    [Output("slider", "children"), Output("selectLabel", "children")],
    [Input("upload", "contents")],
    [State("upload", "filename")],
)
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            back.parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]
        print(children[0])

        return children[0]


@app.callback(
    [Output("time", "figure"), Output("2d", "figure")],
    [Input("slid", "value"), Input("drop", "value")],
)
def update_time(values1, values):
    print(values)
    return back.grphcreate(values1[0], values1[1], values)


if __name__ == "__main__":
    app.run_server(debug=True)
