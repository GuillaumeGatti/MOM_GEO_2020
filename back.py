import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import plotly.graph_objects as go


import pandas as pd


def parse_contents(contents, filename):
    print(filename)
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        global df1
        df1 = pd.read_csv(io.StringIO(decoded.decode("utf-8")), sep=" ")
        df1["label"] = 1

    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    result1 = dcc.RangeSlider(
        id="slid",
        min=df1["sec"].min(),
        max=df1["sec"].max(),
        step=1000,
        value=[df1["sec"].min(), df1["sec"].max()],
    )

    result2 = dcc.Dropdown(
        id="drop",
        options=[{"label": i, "value": i} for i in df1.label.unique()],
        multi=True,
    )
    return (result1, result2)

    #     dcc.RangeSlider(
    #         id="slid",
    #         min=df1["sec"].min(),
    #         max=df1["sec"].max(),
    #         step=1000,
    #         value=[df1["sec"].min(), df1["sec"].max()],
    #     )
    # )


def grphcreate(valmin, valmax, values):
    a = [
        {
            "data": [
                dict(
                    x=df1[
                        (df1["sec"] > valmin)
                        & (df1["sec"] < valmax)
                        & (df1["label"].isin(values))
                    ]["p0"],
                    y=df1[
                        (df1["sec"] > valmin)
                        & (df1["sec"] < valmax)
                        & (df1["label"].isin(values))
                    ]["p1"],
                    mode="markers",
                    hovertext=df1["mag"],
                    hoverinfo="text",
                    labels=df1["label"],
                    opacity=0.7,
                    marker={"size": 8, "line": {"width": 0.5, "color": "white"},},
                )
            ],
            "layout": dict(
                xaxis={"title": "X"},
                yaxis={"title": "Y"},
                legend={"x": 0, "y": 1},
                hovermode="closest",
                margin={"l": 45, "r": 10},
            ),
        },
        {
            "data": [
                dict(
                    x=df1[
                        (df1["sec"] > valmin)
                        & (df1["sec"] < valmax)
                        & (df1["label"].isin(values))
                    ]["sec"],
                    y=df1[
                        (df1["sec"] > valmin)
                        & (df1["sec"] < valmax)
                        & (df1["label"].isin(values))
                    ]["mag"],
                    mode="markers",
                    hovertext=df1["mag"],
                    hoverinfo="text",
                    opacity=0.7,
                    marker={"size": 8, "line": {"width": 0.5, "color": "white"},},
                )
            ],
            "layout": dict(
                xaxis={"title": "X"},
                yaxis={"title": "Y"},
                legend={"x": 0, "y": 1},
                hovermode="closest",
                margin={"l": 25, "r": 25},
            ),
        },
    ]

    return a
