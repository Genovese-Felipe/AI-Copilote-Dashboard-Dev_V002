# PASSO 1: Setup de ambiente e importação de bibliotecas
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import warnings

warnings.filterwarnings('ignore')

# Carregar os dados
try:
    df = pd.read_csv('incidents.csv')
except FileNotFoundError:
    # Gerar dados se o arquivo não existir
    categories = ['Customer', 'Spill', 'Injury', 'Transport', 'Equipment', 'Security', 'Divergence', 'Complaint']
    causes = ['Material', 'Procedure', 'Design', 'Training', 'Management', 'External', 'Equipment', 'Personnel']
    sites = ['Weston', 'Bolton', 'Shirley', 'Lincoln', 'Maynard', 'Acton', 'Concord', 'Hudson']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    years = [2007, 2008, 2009]
    severities = ['Critical', 'Major', 'Medium', 'Near Miss']
    status = ['Open', 'Closed']

    np.random.seed(42)
    records = []
    for year in years:
        for month in months:
            for site in sites:
                for category in categories:
                    for cause in np.random.choice(causes, size=2, replace=False):
                        severity = np.random.choice(severities)
                        stat = np.random.choice(status, p=[0.3, 0.7])
                        count = np.random.poisson(lam=8)
                        if count == 0:
                            continue
                        records.append({
                            'Category': category,
                            'Cause': cause,
                            'Site': site,
                            'Month': month,
                            'Year': year,
                            'Severity': severity,
                            'Status': stat,
                            'Count': count
                        })
    df = pd.DataFrame(records)
    df.to_csv('incidents.csv', index=False)

# Paleta de cores
COLORS = {
    'primary': '#1f77b4',
    'background': '#f8f9fa',
    'card_bg': '#fff',
}

# Iniciar o app Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do dashboard
app.layout = dbc.Container(fluid=True, style={'backgroundColor': COLORS['background'], 'padding': '12px'}, children=[
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(dcc.Graph(id='bar-category'), width=4),
                dbc.Col(dcc.Graph(id='bar-cause'), width=4),
                dbc.Col(dcc.Graph(id='line-month'), width=4),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='bar-site'), width=4),
                dbc.Col(dcc.Graph(id='bar-trend'), width=4),
                dbc.Col(dcc.Graph(id='pie-severity'), width=4),
            ]),
        ], width=10),
        dbc.Col([
            html.Div([
                html.H5("Filtros"),
                html.Label("Category"), dcc.Dropdown(id="filter-category", multi=True, options=[{'label': i, 'value': i} for i in sorted(df['Category'].unique())]),
                html.Label("Site"), dcc.Dropdown(id="filter-site", multi=True, options=[{'label': i, 'value': i} for i in sorted(df['Site'].unique())]),
                html.Label("Month"), dcc.Dropdown(id="filter-month", multi=True, options=[{'label': i, 'value': i} for i in sorted(df['Month'].unique())]),
                html.Label("Cause"), dcc.Dropdown(id="filter-cause", multi=True, options=[{'label': i, 'value': i} for i in sorted(df['Cause'].unique())]),
                html.Label("Severity"), dcc.Dropdown(id="filter-severity", multi=True, options=[{'label': i, 'value': i} for i in sorted(df['Severity'].unique())]),
                html.Label("Year"), dcc.Dropdown(id="filter-year", multi=True, options=[{'label': i, 'value': i} for i in sorted(df['Year'].unique())]),
                html.Label("Status"), dcc.Dropdown(id="filter-status", multi=True, options=[{'label': i, 'value': i} for i in sorted(df['Status'].unique())]),
                html.Hr(),
                html.Div("Total de registros filtrados:"),
                html.H5(id="filtered-count", style={'color': COLORS['primary']})
            ], style={'background': COLORS['card_bg'], 'padding': '16px', 'borderRadius': '8px'})
        ], width=2)
    ])
])

# Callbacks para os gráficos
@app.callback(
    [Output('bar-category', 'figure'),
     Output('bar-cause', 'figure'),
     Output('line-month', 'figure'),
     Output('bar-site', 'figure'),
     Output('bar-trend', 'figure'),
     Output('pie-severity', 'figure'),
     Output('filtered-count', 'children')],
    [Input('filter-category', 'value'),
     Input('filter-site', 'value'),
     Input('filter-month', 'value'),
     Input('filter-cause', 'value'),
     Input('filter-severity', 'value'),
     Input('filter-year', 'value'),
     Input('filter-status', 'value')]
)
def update_all_graphs(cat, site, month, cause, severity, year, stat):
    dff = df.copy()
    if cat: dff = dff[dff['Category'].isin(cat)]
    if site: dff = dff[dff['Site'].isin(site)]
    if month: dff = dff[dff['Month'].isin(month)]
    if cause: dff = dff[dff['Cause'].isin(cause)]
    if severity: dff = dff[dff['Severity'].isin(severity)]
    if year: dff = dff[dff['Year'].isin(year)]
    if stat: dff = dff[dff['Status'].isin(stat)]

    total_count = int(dff['Count'].sum())

    # Gráficos
    fig_cat = px.bar(dff.groupby('Category')['Count'].sum().reset_index(), x='Category', y='Count', title='Incidents by Category')
    fig_cause = px.bar(dff.groupby('Cause')['Count'].sum().reset_index(), x='Cause', y='Count', title='Incidents by Cause')
    fig_line = px.line(dff.groupby(['Year', 'Month'])['Count'].sum().reset_index(), x='Month', y='Count', color='Year', title='Monthly Trend')
    fig_site = px.bar(dff.groupby('Site')['Count'].sum().reset_index(), x='Count', y='Site', orientation='h', title='Incidents by Site')
    fig_trend = px.bar(dff.groupby('Month')['Count'].sum().reset_index(), x='Month', y='Count', title='Monthly Distribution')
    fig_pie = px.pie(dff.groupby('Severity')['Count'].sum().reset_index(), names='Severity', values='Count', title='Severity Distribution')

    return fig_cat, fig_cause, fig_line, fig_site, fig_trend, fig_pie, f"{total_count:,}"

# Execução do app
if __name__ == "__main__":
    app.run(debug=True, port=8050)