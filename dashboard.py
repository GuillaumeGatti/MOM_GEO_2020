import dash
import dash_core_components as dcc
import dash_html_components as html
import back
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import seismic
import base64


app = dash.Dash(__name__, suppress_callback_exceptions=True,)
colors = {"background": "#FFFFFF", "text": "#7FDBFF"}

path = "./seq/"

# image_filename = "my-image.png"  # replace with your own image
# encoded_image = base64.b64encode(open(image_filename, "rb").read())

click = 0

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
        html.H1(
            children="Declustering Seismes",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        upload,
        graphs,
        html.Div(id="extract",),
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


secondDiv = html.Div(
    children=[
        html.Div(
            children=[
                html.Div(children=[html.H6(children="clustering parameters")]),
                html.Div(
                    id="abc",
                    children=[
                        html.H5(children="Δt"),
                        dcc.Slider(
                            id="my-slider", min=259, max=259000, step=0.5, value=259000,
                        ),
                        html.H6(children="Enter Δt max"),
                        dcc.Input(
                            id="deltaTmax",
                            placeholder="Δt max",
                            value="259000",
                            type="text",
                        ),
                        html.Div(id="slider-output-t"),
                    ],
                ),
                html.Div(
                    children=[
                        html.H5(children="Δd"),
                        dcc.Slider(
                            id="my-slider2", min=5, max=5000, step=0.5, value=5000
                        ),
                        html.H6(children="Enter Δd max"),
                        dcc.Input(
                            id="deltaDmax",
                            placeholder="Δd max",
                            value="5000",
                            type="text",
                        ),
                        html.Div(id="slider-output-d"),
                    ]
                ),
            ],
            style={
                "width": "25%",
                "float": "right",
                "border": "2px black solid",
                "border-radius": "25px",
            },
        ),
        html.Div(
            children=[html.Div([html.H3("Column 3"), dcc.Graph(id="g3"),],),],
            style={
                "width": "70%",
                "margin-top": "60px",
                "float": "left",
                "border": "2px black solid",
            },
        ),
    ]
)

app.layout = html.Div([firstDiv, secondDiv])


@app.callback(
    dash.dependencies.Output("slider-output-t", "children"),
    [dash.dependencies.Input("my-slider", "value")],
)
def t2(value):
    return "Δt=" + str(value) + " s"


@app.callback(
    dash.dependencies.Output("slider-output-d", "children"),
    [dash.dependencies.Input("my-slider2", "value")],
)
def k2(value):
    return "Δd=" + str(value) + " m"


@app.callback(
    dash.dependencies.Output("my-slider", "max"),
    [dash.dependencies.Input("deltaTmax", "value")],
)
def k2(value):
    if value == "":
        while value == "":
            1 == 1
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
    dash.dependencies.Output("my-slider2", "min"),
    [dash.dependencies.Input("my-slider2", "max")],
)
def t2(v):
    return int(v) / 1000


@app.callback(
    dash.dependencies.Output("my-slider", "min"),
    [dash.dependencies.Input("my-slider", "max")],
)
def t2(v):
    return int(v) / 1000


@app.callback(
    dash.dependencies.Output("my-slider2", "max"),
    [dash.dependencies.Input("deltaDmax", "value")],
)
def k2(value):
    if value == "":
        while value == "":
            1 == 1
    value = str(value).lower()
    value.replace(" ", "")
    if value.endswith("km"):
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
    if value.endswith("k"):
        value = value[:-1]
        value.replace(" ", "")
        value = int(value)
        value = 1000 * value
        return value
    return int(value)


@app.callback(
    [
        Output("slider", "children"),
        Output("selectLabel", "children"),
        Output("extract", "children"),
    ],
    [Input("upload", "contents")],
    [State("upload", "filename")],
)
def load(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            back.parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)
        ]

        return children[0]


@app.callback(
    [Output("time", "figure"), Output("2d", "figure")],
    [Input("slid", "value"), Input("drop", "value")],
)
def update_graph(values1, values):

    return back.grphcreate(values1[0], values1[1], values)


@app.callback(
    [Output("drop", "options"), Output("g3", "figure"),],
    [Input("my-slider2", "value"), Input("my-slider", "value")],
)
def clustering(deltD, deltT):

    back.clustering(deltD, deltT, 10)

    # image_filename = "poisson.png"  # replace with your own image
    # encoded_image = base64.b64encode(open(image_filename, "rb").read())
    # src = "data:image/png;base64,{}".format(encoded_image.decode())

    a = [
        {"label": i, "value": i}
        for i in back.df1[
            back.df1["type"].isin(["mainshock", "correlated sismicity"])
        ].label.unique()
    ]

    print("ok")

    c = back.graphMain()

    return a, c[0]


@app.callback(
    Output("export", "style"), [Input("export", "n_clicks"), Input("drop", "value")]
)
def download(n_clicks, clusters):
    global click
    print(click)
    if n_clicks > click:
        back.export(clusters)
        click += 1

    return {}


if __name__ == "__main__":
    app.run_server(debug=True)
