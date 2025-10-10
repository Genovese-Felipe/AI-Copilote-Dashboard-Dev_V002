# PASSO 1: Setup de ambiente e importação de bibliotecas
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import warnings

from .data_generator import generate_data

warnings.filterwarnings('ignore')

print("✅ Bibliotecas importadas com sucesso!")

# Generate the dataset
df = generate_data()
# Define months for ordering
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# PASSO 3: Design do layout do dashboard
COLORS = {
    'primary': '#1f77b4',
    'success': '#2ca02c',
    'warning': '#ff7f0e',
    'danger': '#d62728',
    'info': '#17becf',
    'secondary': '#7f7f7f',
    'background': '#f8f9fa',
    'card_bg': '#fff',
    'text_primary': '#212529',
    'text_secondary': '#6c757d'
}

# Inicie o app Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(fluid=True, style={'backgroundColor': COLORS['background'], 'padding': '12px'}, children=[
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Category", className="text-center", style={'fontWeight': 'bold'}),
                        dcc.Graph(id='bar-category')
                    ])
                ], width=4),
                dbc.Col([
                    html.Div([
                        html.H4("Cause", className="text-center", style={'fontWeight': 'bold'}),
                        dcc.Graph(id='bar-cause')
                    ])
                ], width=4),
                dbc.Col([
                    html.Div([
                        html.H4("Month", className="text-center", style={'fontWeight': 'bold'}),
                        dcc.Graph(id='line-month')
                    ])
                ], width=4),
            ])
        ], width=10),
        dbc.Col([
            html.Div([
                html.H5("Filtros", style={'fontWeight': 'bold', 'marginBottom': '8px'}),
                html.Label("Category"), dcc.Dropdown(id="filter-category", multi=True),
                html.Label("Site"), dcc.Dropdown(id="filter-site", multi=True),
                html.Label("Month"), dcc.Dropdown(id="filter-month", multi=True),
                html.Label("Cause"), dcc.Dropdown(id="filter-cause", multi=True),
                html.Label("Severity"), dcc.Dropdown(id="filter-severity", multi=True),
                html.Label("Year"), dcc.Dropdown(id="filter-year", multi=True),
                html.Label("Status"), dcc.Dropdown(id="filter-status", multi=True),
                html.Hr(),
                html.Div("Total de registros filtrados:", style={'marginTop':'12px'}),
                html.H5(id="filtered-count", style={'color': COLORS['primary'], 'fontWeight': 'bold'})
            ], style={'background': COLORS['card_bg'], 'padding': '16px', 'borderRadius': '8px', 'boxShadow': '0 2px 8px #e3e3e3'})
        ], width=2)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Site", className="text-center", style={'fontWeight': 'bold'}),
                        dcc.Graph(id='bar-site')
                    ])
                ], width=4),
                dbc.Col([
                    html.Div([
                        html.H4("Trend", className="text-center", style={'fontWeight': 'bold'}),
                        dcc.Graph(id='bar-trend')
                    ])
                ], width=4),
                dbc.Col([
                    html.Div([
                        html.H4("Severity", className="text-center", style={'fontWeight': 'bold'}),
                        dcc.Graph(id='pie-severity')
                    ])
                ], width=4),
            ])
        ], width=10),
        dbc.Col([], width=2)
    ])
])

print("✅ Layout estruturado. Pronto para conectar os dados e gráficos!")

# PASSO 4: Implementação dos gráficos e preenchimento automático dos filtros
def get_dropdown_options(col):
    opts = [{'label': str(i), 'value': i} for i in sorted(df[col].unique())]
    return opts

@app.callback(
    [Output("filter-category", "options"),
     Output("filter-site", "options"),
     Output("filter-month", "options"),
     Output("filter-cause", "options"),
     Output("filter-severity", "options"),
     Output("filter-year", "options"),
     Output("filter-status", "options")],
    Input("filter-category", "options")
)
def fill_filter_options(_):
    return (
        get_dropdown_options("Category"),
        get_dropdown_options("Site"),
        get_dropdown_options("Month"),
        get_dropdown_options("Cause"),
        get_dropdown_options("Severity"),
        get_dropdown_options("Year"),
        get_dropdown_options("Status"),
    )

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
    if cat:      dff = dff[dff['Category'].isin(cat)]
    if site:     dff = dff[dff['Site'].isin(site)]
    if month:    dff = dff[dff['Month'].isin(month)]
    if cause:    dff = dff[dff['Cause'].isin(cause)]
    if severity: dff = dff[dff['Severity'].isin(severity)]
    if year:     dff = dff[dff['Year'].isin(year)]
    if stat:     dff = dff[dff['Status'].isin(stat)]
    total_count = int(dff['Count'].sum())

    def stacked_bar(data, x, color, title, orientation='v'):
        if orientation == 'v':
            fig = px.bar(data, x=x, y='Count', color=color, barmode='stack',
                         color_discrete_sequence=px.colors.qualitative.Plotly)
        else:
            fig = px.bar(data, y=x, x='Count', color=color, barmode='stack',
                         orientation='h', color_discrete_sequence=px.colors.qualitative.Plotly)
        fig.update_layout(title='', legend_title='', margin=dict(t=18, b=6, l=2, r=2))
        return fig

    fig_cat = stacked_bar(dff, x='Category', color='Severity', title='Category')
    fig_cause = stacked_bar(dff, x='Cause', color='Severity', title='Cause')

    dff_line = dff.groupby(['Year', 'Month', 'Category'], as_index=False)['Count'].sum()
    dff_line['MonthNum'] = dff_line['Month'].apply(lambda m: months.index(m))
    dff_line = dff_line.sort_values(['Year', 'MonthNum'])
    fig_line = go.Figure()
    for cat_name in dff_line['Category'].unique():
        sub = dff_line[dff_line['Category'] == cat_name]
        x_vals = sub['Year'].astype(str) + '-' + sub['Month']
        fig_line.add_trace(go.Scatter(x=x_vals, y=sub['Count'], mode='lines+markers', name=cat_name))
    fig_line.update_layout(title='', xaxis_title='', yaxis_title='Count', legend_title='', margin=dict(t=18, b=6, l=2, r=2))

    fig_site = stacked_bar(dff, x='Site', color='Severity', title='Site', orientation='h')
    fig_trend = stacked_bar(dff, x='Month', color='Severity', title='Trend', orientation='h')

    dff_pie = dff.groupby('Severity', as_index=False)['Count'].sum()
    fig_pie = px.pie(dff_pie, names='Severity', values='Count', color='Severity',
                     color_discrete_sequence=px.colors.qualitative.Plotly)
    fig_pie.update_layout(title='', legend_title='', margin=dict(t=18, b=6, l=2, r=2))

    return fig_cat, fig_cause, fig_line, fig_site, fig_trend, fig_pie, f"{total_count:,}"

print("✅ Gráficos e filtros prontos, aguardando execução do app.")

# PASSO 5: Execução do app Dash
if __name__ == "__main__":
    app.run(debug=True, port=8050)