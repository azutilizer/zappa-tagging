import os
import dash
import dash_labs as dl
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.server.secret_key = os.environ.get('secret_key', 'secret')
server =app.server

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="More Pages",
    ),
    brand="NER tagging & training",
    color="primary",
    dark=True,
    className="mb-2",
)

app.layout = dbc.Container(
    [navbar, dl.plugins.page_container],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server()