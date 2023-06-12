from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

from database.db import imdb_database
from graphs.network_graph import actors_network_graph

# Initialize the app and incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.COSMO]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Get MongoDB database
db = imdb_database()


def movies_per_year_graph():
    collection = db['movies.basics']

    pipeline = [
    {"$group": {"_id": "$startYear", "count": {"$sum": 1}}}
    ]
    result = collection.aggregate(pipeline)

    years_df = pd.DataFrame.from_records(result)
    years_df = years_df.drop(years_df[years_df['_id'] == '\\N'].index)
    years_df = years_df.sort_values('_id')

    fig = px.line(years_df, x='_id',y='count',
                   title='Quantidade de filmes lançados por ano')
    fig.update_layout(
        xaxis_title="Ano",
        yaxis_title="Número de Filmes",
        showlegend=False
    )
    return fig


def genre_distribution_graph():
    collection = db['movies.basics']
    pipeline = [
    {"$project": {"genres": {"$split": ["$genres", ","]}}},  # Divide a string em gêneros individuais
    {"$unwind": "$genres"},  # Desdobra os gêneros em documentos separados
    {"$group": {"_id": "$genres", "count": {"$sum": 1}}}  # Agrupa e conta a ocorrência de cada gênero
    ]
    result = collection.aggregate(pipeline)

    genres_df = pd.DataFrame.from_records(result)
    genres_df = genres_df.drop(genres_df[genres_df['_id'] == '\\N'].index)
    genres_df = genres_df.sort_values('count', ascending=False)

    fig = px.bar(genres_df, x='_id', y='count', 
                 title='Distribuição de filmes por gênero')
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

    dbc.Row([
        dcc.Graph(id='actors_network', figure=actors_network_graph(db))
    ]),

], fluid=True)


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
