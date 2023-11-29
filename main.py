import streamlit as st
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Carregar os dados
df = pd.read_csv('brasileirao-serie-a.csv', delimiter=';')

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div(children=[
    html.H1(children='Dashboard de Futebol'),

    # Componente de intervalo para seleção do período
    html.Label('Selecione o Período:'),
    dcc.RangeSlider(
        id='season-slider',
        min=df['season'].min(),
        max=df['season'].max(),
        marks={str(season): str(season) for season in df['season'].unique()},
        value=[df['season'].min(), df['season'].max()]
    ),

    # Gráficos
    dcc.Graph(id='not-bottom-4-chart'),
    dcc.Graph(id='most-championships-chart'),
    dcc.Graph(id='most-relegations-chart'),
    dcc.Graph(id='most-goals-for-chart'),
    dcc.Graph(id='most-goals-against-chart'),
    dcc.Graph(id='most-bottom-4-chart')
])

# Callbacks para atualizar os gráficos com base na seleção do período
@app.callback(
    [Output('not-bottom-4-chart', 'figure'),
     Output('most-championships-chart', 'figure'),
     Output('most-relegations-chart', 'figure'),
     Output('most-goals-for-chart', 'figure'),
     Output('most-goals-against-chart', 'figure'),
     Output('most-bottom-4-chart', 'figure')],
    [Input('season-slider', 'value')]
)
def update_charts(selected_period):
    filtered_df = df[(df['season'] >= selected_period[0]) & (df['season'] <= selected_period[1])]

    # Times que não ficaram entre os 4 últimos
    not_bottom_4_fig = px.bar(filtered_df.groupby('team')['goals_against'].sum().sort_values(ascending=False).head(5).reset_index(), x='team', title='Times que menos ficaram na zona de rebaixamento')

    # Times que mais venceram campeonatos durante o período (gráfico de dispersão)
    most_championships_fig = px.scatter(filtered_df.groupby('team')['place'].min().sort_values(ascending=True).head(5).reset_index(),
                                    x='team', y='place', title='Times que mais venceram campeonatos')

    # Times que mais ficaram na zona de rebaixamento
    most_relegations_fig = px.bar(filtered_df.groupby('team')['place'].max().sort_values(ascending=False).head(5).reset_index(),
                                  x='team', y='place', title='Times que mais ficaram na zona de rebaixamento')

    # Times que mais fizeram gol durante o período
    most_goals_for_fig = px.bar(filtered_df.groupby('team')['goals_for'].sum().sort_values(ascending=False).head(5).reset_index(),
                                x='team', y='goals_for', title='Times que mais fizeram gols')

    # Times que mais fizeram gols contra durante o período (gráfico de linha)
    most_goals_against_fig = px.line(filtered_df.groupby('team')['goals_against'].sum().sort_values(ascending=False).head(5).reset_index(),
                                    x='team', y='goals_against', title='Times que mais sofreram gols')

    # Times que mais ficaram nos 4 últimos durante o período
    most_bottom_4_fig = px.bar(filtered_df[filtered_df['place'] >= 20], x='team', y='place', title='Times que mais ficaram nos 4 últimos')

    return not_bottom_4_fig, most_championships_fig, most_relegations_fig, most_goals_for_fig, most_goals_against_fig, most_bottom_4_fig

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)

