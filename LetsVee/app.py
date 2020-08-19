import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('./datasets/WA_Fn-UseC_-HR-Employee-Attrition.csv')

available_indicators = df['JobRole'].unique()

title_list = ['Sales Executive', 'Research Scientist', 'Laboratory Technician',
 'Manufacturing Director', 'Healthcare Representative', 'Manager',
 'Sales Representative', 'Research Director', 'Human Resources']

locations = ['Sales', 'Research & Development', 'Human Resources']

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Holder for X Axis'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Holder for Y Axis'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['JobInvolvement'].min(),
        max=df['JobInvolvement'].max(),
        value=df['JobInvolvement'].max(),
        marks={str(year): str(year) for year in df['JobInvolvement'].unique()},
        step=None
    ),
    html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['WorkLifeBalance'].min(),
        max=df['WorkLifeBalance'].max(),
        value=df['WorkLifeBalance'].min(),
        marks={str(year): str(year) for year in df['WorkLifeBalance'].unique()},
        step=None
        )
    ]),
        html.Div([
    html.H3(children='Attrition'),
    
    html.Div(dcc.Dropdown(
                id='title',
                options=[{'label': i, 'value': i} for i in title_list],
                value='Manager'
            )),
    
    dcc.Graph(id='competencies')],
    style={'width': '50%', 'display': 'inline-block'}),
    
    html.Div([
    html.H3(children='Sales'),

    html.Div(dcc.Dropdown(
                id = 'location-std',
                options=[{'label': i, 'value': i} for i in locations],
                value='Sales'
    )),
        
    dcc.Graph(id='location-graphic')],
    style={'width': '50%', 'display': 'inline-block'})

])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
                 
    filtered_df = df[df.WorkLifeBalance == year_value]

    fig = px.scatter(filtered_df, x="Age", y="MonthlyIncome", 
                     size="JobLevel", color="EducationField", hover_name="Attrition", 
                     log_x=True, size_max=55)

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_column_name, 
                     type='linear' if xaxis_type == 'Linear' else 'log') 

    fig.update_yaxes(title=yaxis_column_name, 
                     type='linear' if yaxis_type == 'Linear' else 'log') 

    return fig

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.WorkLifeBalance == selected_year]

    fig = px.scatter(filtered_df, x="Age", y="MonthlyIncome", 
                     size="JobLevel", color="EducationField", hover_name="Attrition", 
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

@app.callback(
    Output('competencies', 'figure'),
    [Input('title', 'value')]
)
def update_figure(title):
    data = df[df['JobRole'] == title]
    fig = px.bar(data, x='JobSatisfaction', y='DistanceFromHome', color='Gender',title = title)
    return fig

@app.callback(
    Output('location-graphic', 'figure'),
    [Input('location-std', 'value')])
def update_figure(location_std_name):
    filtered_df = df[df['Department'] == location_std_name]
    fig = px.histogram(filtered_df, x="JobInvolvement",title=location_std_name)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)