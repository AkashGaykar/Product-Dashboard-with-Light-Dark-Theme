import dash
from dash import dcc,html
# import dash_core_components as dcc
# import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

# Sample data
df = pd.DataFrame({
    'Fruit': ['Apples', 'Oranges', 'Bananas','Mangoes'],
    'SF': [4, 1, 2, 5],
    'NYC': [2, 3, 1, 4],
    'India': [3,4,5,6]
})

# Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='city-dropdown',
        options=[
            {'label': 'San Francisco', 'value': 'SF'},
            {'label': 'New York City', 'value': 'NYC'},
            {'label':'INDIA','value':'India'}
        ],
        value='India'  # Default value
    ),
    dcc.RadioItems(
        id='fruit-radio',
        options=[
            {'label': 'Apples', 'value': 'Apples'},
            {'label': 'Oranges', 'value': 'Oranges'},
            {'label': 'Bananas', 'value': 'Bananas'},
            {'label': 'Grapes', 'value': 'Mangoes'}
        ],
        value='Mangoes'  # Default value
    ),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    dcc.Graph(id='bar-graph')
])

@app.callback(
    Output('bar-graph', 'figure'),
    Input('submit-button', 'n_clicks'),
    [State('city-dropdown', 'value'),
     State('fruit-radio', 'value')]
)
def update_bar_chart(n_clicks, selected_city, selected_fruit):
    filtered_df = df[df['Fruit'] == selected_fruit]
    fig = px.bar(filtered_df, x=[selected_city], y=filtered_df[selected_city].values,
                 title=f'Amount of {selected_fruit} in {selected_city}',
                 labels={'x': 'City', 'y': 'Quantity'})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
