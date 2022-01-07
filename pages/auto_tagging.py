import base64
import dash

"""
In dash 1.x, replace follow 2 lines with
import dash_html_components as html
import dash_core_components as dcc
"""
from dash import html
from dash import dcc

from dash.dependencies import Input, Output, State

import spacy
from spacy.displacy.render import DEFAULT_LABEL_COLORS


# Initialize the application
dash.register_page(__name__, path="/")
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def parse_contents(contents, filename, modified_date):
    if str(filename).lower().endswith('.txt'):
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string).decode('utf-8')

        return decoded
    else:
        return ""


def entname(name):
    return html.Span(name, style={
        "font-size": "0.8em",
        "font-weight": "bold",
        "line-height": "1",
        "border-radius": "0.35em",
        "text-transform": "uppercase",
        "vertical-align": "middle",
        "margin-left": "0.5rem"
    })


def entbox(children, color):
    return html.Mark(children, style={
        "background": color,
        "padding": "0.2em 0.5em",
        "margin": "0 0.25em",
        "line-height": "1",
        "border-radius": "0.35em",
    })


def entity(children, name):
    if type(children) is str:
        children = [children]

    children.append(entname(name))
    color = DEFAULT_LABEL_COLORS[name]
    return entbox(children, color)


def render(doc):
    children = []
    last_idx = 0
    for ent in doc.ents:
        children.append(doc.text[last_idx:ent.start_char])
        children.append(
            entity(doc.text[ent.start_char:ent.end_char], ent.label_))
        last_idx = ent.end_char
    children.append(doc.text[last_idx:])
    return children


# define de app
layout = html.Div(
    [
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '50%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': 'auto'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Br(),
        html.Div(id='my-output'),        
    ]
)


@dash.callback(
    Output(component_id='my-output', component_property='children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output_div(content, filename, last_date):
    if content is not None:
        nlp = spacy.load("en_core_web_sm")
        total_text = []
        for c, n, d in zip(content, filename, last_date):
            input_value = parse_contents(c, n, d)
            total_text.append(input_value)

        doc = nlp('\n'.join(total_text))
        return html.Div(children=render(doc))