import pandas as pd
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_ag_grid as dag
from dash_bootstrap_templates import load_figure_template, ThemeSwitchAIO

# Load data
df = pd.read_csv("products-100.csv")

# Load bootstrap themes
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# App setup
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc_css, dbc.icons.FONT_AWESOME])
app.title = "Product Dashboard"

# Load Plotly templates
load_figure_template(["minty", "darkly"])

# Theme switch component
theme_switch = ThemeSwitchAIO(
    aio_id="theme",
    icons={"left": "fa fa-sun", "right": "fa fa-moon"},
    switch_props={"value": False}
)

# Availability dropdown
availability_dropdown = dcc.Dropdown(
    options=[{'label': cat, 'value': cat} for cat in df['Category'].unique()],
    multi=True,
    placeholder="Filter by Category",
    id='category-filter'
)

# Header
header = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col(dbc.NavbarBrand("Product Dashboard", className="ms-2")),
        ], align="center", className="g-0"),
        theme_switch
    ], fluid=True),
    color="#013576",
    dark=True,
    sticky="top",
    className="mb-2"
)

# Layout
app.layout = dbc.Container([
    header,

    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.Label("Availability Filter"),
                availability_dropdown
            ])
        ]), width=4)
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            html.H5("Full Data Table"),
            dag.AgGrid(
                id="data-table",
                columnDefs=[{"headerName": col, "field": col, "sortable": True, "filter": True} for col in df.columns],
                rowData=df.to_dict("records"),
                className="ag-theme-alpine",
                style={"height": "400px", "width": "100%"},
                columnSize="sizeToFit",
                defaultColDef={"resizable": True, "filter": True}
            )
        ])
    ]),

    html.Br(),

    dbc.Row([dbc.Col(dcc.Graph(id="bar-graph"))]),
    dbc.Row([dbc.Col(dcc.Graph(id="pie-graph"))]),
    dbc.Row([dbc.Col(dcc.Graph(id="scatter-graph"))]),
    dbc.Row([dbc.Col(dcc.Graph(id="sunburst-graph"))]),
    dbc.Row([dbc.Col(dcc.Graph(id="histogram-graph"))])
], fluid=True)


# Callback: update charts + AG Grid
@app.callback(
    Output("sunburst-graph", "figure"),
    Output("bar-graph", "figure"),
    Output("pie-graph", "figure"),
    Output("scatter-graph", "figure"),
    Output("histogram-graph", "figure"),
    Output("data-table", "columnDefs"),
    Output("data-table", "rowData"),
    Output("data-table", "className"),
    Input("category-filter", "value"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def update_dashboard(selected_availability, is_dark_mode):
    theme = "dark" if is_dark_mode else "light"
    template = "plotly_dark" if is_dark_mode else "plotly_white"
    ag_theme = "ag-theme-alpine-dark" if is_dark_mode else "ag-theme-alpine"

    filtered_df = df.copy()
    if selected_availability:
        filtered_df = df[df["Category"].isin(selected_availability)]

    # Sunburst
    sunburst = px.sunburst(filtered_df, path=['Category', 'Brand', 'Color'], values='Stock',
                           title="Sunburst: Category > Brand > Color", template=template)

    # Bar Chart
    avg_price = filtered_df.groupby('Category')['Price'].mean().reset_index()
    bar = px.bar(avg_price, x='Category', y='Price',
                 title='Average Price by Category', template=template)

    # Pie Chart
    pie = px.pie(filtered_df, names='Availability', title='Availability Distribution', template=template)

    # Scatter Plot
    scatter = px.scatter(filtered_df, x='Price', y='Stock', color='Category', size='Stock',
                         hover_data=['Brand', 'Color'], title='Price vs. Stock', template=template)

    # Histogram
    hist = px.histogram(filtered_df, x='Stock', nbins=20,
                        title='Stock Distribution', template=template)

    column_defs = [{"headerName": col, "field": col, "sortable": True, "filter": True} for col in df.columns]

    return sunburst, bar, pie, scatter, hist, column_defs, filtered_df.to_dict("records"), ag_theme


if __name__ == '__main__':
    app.run(debug=True)


# import pandas as pd
# from dash import Dash, html, dcc, Input, Output
# import dash_bootstrap_components as dbc
# import plotly.express as px

# # Load data
# df = pd.read_csv("products-100.csv")

# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# # Dropdown for filtering
# availability_dropdown = dcc.Dropdown(
#     options=[{'label': avail, 'value': avail} for avail in df['Availability'].unique()],
#     multi=True,
#     placeholder="Filter by Availability",
#     id='availability-filter'
# )

# # App layout with tabs
# app.layout = dbc.Container([
#     dbc.Row([
#         dbc.Col(html.H1("Product Dashboard"), width=12)
#     ]),

#     dbc.Row([
#         dbc.Col(
#             dbc.Card([
#                 dbc.CardBody([
#                     html.Label("Availability Filter"),
#                     availability_dropdown
#                 ])
#             ]),
#             width=4
#         )
#     ]),

#     dbc.Tabs([
#         dbc.Tab(label="Sunburst Chart", tab_id="sunburst"),
#         dbc.Tab(label="Bar Chart", tab_id="bar"),
#         dbc.Tab(label="Pie Chart", tab_id="pie"),
#         dbc.Tab(label="Scatter Plot", tab_id="scatter"),
#         dbc.Tab(label="Histogram", tab_id="histogram"),
#     ], id='tabs', active_tab='sunburst'),

#     html.Br(),

#     dbc.Row([
#         dbc.Col(dcc.Graph(id="graph-output"), width=12)
#     ])
# ], fluid=True)


# # Callback to update chart based on selected tab and filter
# @app.callback(
#     Output("graph-output", "figure"),
#     Input("tabs", "active_tab"),
#     Input("availability-filter", "value")
# )
# def update_graph(tab, selected_availability):
#     filtered_df = df.copy()
#     if selected_availability:
#         filtered_df = df[df["Availability"].isin(selected_availability)]

#     if tab == "sunburst":
#         fig = px.sunburst(filtered_df,
#                           path=['Category', 'Brand', 'Color'],
#                           values='Stock',
#                           title="Category > Brand > Color (Stock Based)")
#     elif tab == "bar":
#         avg_price = filtered_df.groupby('Category')['Price'].mean().reset_index()
#         fig = px.bar(avg_price,
#                      x='Category', y='Price',
#                      title='Average Price by Category')
#     elif tab == "pie":
#         fig = px.pie(filtered_df,
#                      names='Availability',
#                      title='Availability Distribution')
#     elif tab == "scatter":
#         fig = px.scatter(filtered_df,
#                          x='Price', y='Stock',
#                          color='Category',
#                          size='Stock',
#                          hover_data=['Brand', 'Color'],
#                          title='Price vs Stock by Category')
#     elif tab == "histogram":
#         fig = px.histogram(filtered_df,
#                            x='Stock', nbins=20,
#                            title='Stock Distribution')
#     else:
#         fig = px.scatter(title="No Tab Selected")

#     return fig


# if __name__ == '__main__':
#     app.run(debug=True)


# import pandas as pd
# from dash import Dash,html,dcc,Input,Output,callback
# import dash_bootstrap_components as dbc
# import plotly.express as px

# df = pd.read_csv("products-100.csv")
# # print(df.head())

# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# category_dropdown = dcc.Dropdown(df.Availability.unique(),
#                                  multi=True,
#     placeholder="Select Category"
# )

# sunburst_chart = dcc.Graph()

# app.layout = dbc.Container([
#     dbc.Row([
#         dbc.Col(html.H1("Product Data"))
#     ]),
    
#     dbc.Row([
#         dbc.Col(
#             dbc.Card([
#                 dbc.Label("Category"),
#                 html.Br(),
#                 category_dropdown
#             ])
#         )
#     ]),
#     dbc.Row([
#         dbc.Col(dbc.Card([sunburst_chart]))
#     ])
# ])

# @callback(
#     Output(sunburst_chart, 'figure'),
#     Input(category_dropdown, 'option')
# )
# def update_dashboard(category_dropdown):
#     fig = px.sunburst(df, values=category_dropdown)
#     return fig
    

# if __name__ =='__main__':
#     app.run(debug=True)
