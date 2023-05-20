from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np


# Initialize the app and incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.COSMO]
app = Dash(__name__, external_stylesheets=external_stylesheets)


movies = pd.read_csv('data/title.basics.tsv', sep='\t')
movies = movies.query(" titleType == 'movie' ")
nan_index = movies[movies['startYear'] == '\\N'].index
movies_with_year = movies.drop(nan_index)
year_counts = movies_with_year['startYear'].value_counts().sort_index()

def movies_per_year_graph():
    fig = px.line(year_counts, title='Quantidade de filmes lançados por ano')
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Número de Filmes",
        showlegend=False
    )
    return fig


nan_genres = movies[movies['genres'] == '\\N'].index
movies_with_genres = movies.drop(nan_genres)
movies_genres_column = movies_with_genres['genres'].str.split(',')
genres_expanded = movies_genres_column.explode().value_counts()

def genre_distribution_graph():
    fig = px.bar(genres_expanded, title='Distribuição de filmes por gênero')
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False
    )
    return fig


app.layout = dbc.Container([
    dbc.Row([
        html.Div('Visualização de Dados IMDB', className="text-primary text-center fs-3")
    ]), 

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='movies_per_year', figure=movies_per_year_graph()), 
        ], width=6),

        dbc.Col([
            dcc.Graph(id='genre_distribution', figure=genre_distribution_graph()), 
        ], width=6),
    ]),

], fluid=True)




# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)