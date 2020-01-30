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
import seismic as sei


import pandas as pd

df1 = pd.DataFrame()


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
    result3 = html.Button("extract", id="export", style={"color": "#FF0000"})
    return (result1, result2, result3)

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
                        & (df1["type"].isin(["mainshock", "correlated sismicity"]))
                    ]["p0"],
                    y=df1[
                        (df1["sec"] > valmin)
                        & (df1["sec"] < valmax)
                        & (df1["label"].isin(values))
                        & (df1["type"].isin(["mainshock", "correlated sismicity"]))
                    ]["p1"],
                    mode="markers",
                    hovertext=df1[
                        (df1["sec"] > valmin)
                        & (df1["sec"] < valmax)
                        & (df1["label"].isin(values))
                        & (df1["type"].isin(["mainshock", "correlated sismicity"]))
                    ]["label"],
                    hoverinfo="text",
                    opacity=0.7,
                    marker={
                        "color": df1[
                            (df1["sec"] > valmin)
                            & (df1["sec"] < valmax)
                            & (df1["label"].isin(values))
                            & (df1["type"].isin(["mainshock", "correlated sismicity"]))
                        ]["label"],
                        "size": 8,
                        "line": {"width": 0.5, "color": "white"},
                    },
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
                        & (df1["type"].isin(["mainshock", "correlated sismicity"]))
                    ]["sec"],
                    y=df1[
                        (df1["sec"] > valmin)
                        & (df1["sec"] < valmax)
                        & (df1["label"].isin(values))
                        & (df1["type"].isin(["mainshock", "correlated sismicity"]))
                    ]["mag"],
                    mode="markers",
                    hovertext=df1[
                        (df1["sec"] > valmin)
                        & (df1["sec"] < valmax)
                        & (df1["label"].isin(values))
                        & (df1["type"].isin(["mainshock", "correlated sismicity"]))
                    ]["label"],
                    hoverinfo="text",
                    opacity=0.7,
                    marker={
                        "color": df1[
                            (df1["sec"] > valmin)
                            & (df1["sec"] < valmax)
                            & (df1["label"].isin(values))
                            & (df1["type"].isin(["mainshock", "correlated sismicity"]))
                        ]["label"],
                        "size": 8,
                        "line": {"width": 0.5, "color": "white"},
                    },
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


def clustering(delta_d, delta_t, min_clust):
    global df1
    df1 = sei.seismic_clust(df1, delta_d, delta_t, min_clust)
    print("ok")
    back1 = df1[df1["type"] == "background"]
    cor = df1[df1["type"] == "correlated sismicity"]
    main1 = df1[df1["type"] == "mainshock"]
    # sei.GraphInterEventTime2(main1.sec, back1.sec)


# sei.GraphInterEventTime2(main.sec, back.sec)


def graphMain():
    return [
        {
            "data": [
                {
                    "x": df1[(df1["type"].isin(["mainshock"]))]["sec"],
                    "y": df1[(df1["type"].isin(["mainshock"]))]["mag"],
                    "mode": "markers",
                    "hovertext": df1[(df1["type"].isin(["mainshock"]))]["label"],
                    "hoverinfo": "text",
                    "opacity": 0.7,
                    "name": "mainshock",
                    "mode": "markers",
                },
                {
                    "x": df1[(df1["type"].isin(["background"]))]["sec"],
                    "y": df1[(df1["type"].isin(["background"]))]["mag"],
                    "mode": "markers",
                    "hovertext": "background",
                    "hoverinfo": "text",
                    "opacity": 0.7,
                    "name": "background",
                },
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
