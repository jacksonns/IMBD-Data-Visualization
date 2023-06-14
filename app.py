from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

from database.db import imdb_database
from graphs.network_graph import actors_network_graph
from graphs.ranking_bar import RankingGraph

# Initialize the app and incorporate a Dash Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Get MongoDB database
db = imdb_database()

# Saving dataframe on cache (global variable).
collection = db['movies.data']
pipeline = [
    {"$project": {"tconst": 1, "title": 1, 'year':1, "averageRating":1, "genres":1}},  # Desired Columns
]
result = collection.aggregate(pipeline)
movies_df = pd.DataFrame(result)
ranking_graph = RankingGraph(movies_df)


def movies_per_year_graph():
    collection = db['movies.basics']

    pipeline = [
    {"$group": {"_id": "$startYear", "count": {"$sum": 1}}}
    ]
    result = collection.aggregate(pipeline)

    years_df = pd.DataFrame.from_records(result)
    years_df = years_df.drop(years_df[years_df['_id'] == '\\N'].index)
    years_df = years_df.sort_values('_id')

    fig = px.line(years_df, x='_id',y='count')
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

    fig = px.bar(genres_df, x='_id', y='count')
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

    html.Hr(),

    dbc.Row([
        html.Div("Distribuição de Filmes", 
                 className="text-secondary text-center fs-4", 
                 style={'margin-bottom': '20px'}),

        dbc.RadioItems(
        id='movies_items',
        options=[
            {'label': 'Por gênero', 'value': 'genero'},
            {'label': 'Por ano', 'value': 'ano'}
        ],
        value='ano',
        ),

        dcc.Graph(id='movies_graph', figure=movies_per_year_graph()),
    ]),

    html.Hr(),

    dbc.Row([
        html.Div("Colaborações entre Atores", 
                 className="text-secondary text-center fs-4"),
        dcc.Graph(id='actors_network', figure=actors_network_graph(db))
    ]),

    html.Hr(),

    dbc.Row([
        html.Div("Avaliação dos Filmes", 
                 className="text-secondary text-center fs-4", 
                 style={'margin-bottom': '20px'}),

        dbc.Col([
            dbc.Label("Tipo de amostra:"),
            dbc.Select(
                id='select_sample_filter',
                options=[
                    {'label': 'Aleatória', 'value': 'random'},
                    {'label': 'Ranking', 'value': 'ranking'}
                ],
                value='random'
            ),
        ]),

        dbc.Col([
            dbc.Label("Tamanho da amostra:"),
            dbc.Select(
                id='select_sample_size_filter',
                options=[
                    {'label': '10', 'value': 10},
                    {'label': '50', 'value': 50},
                    {'label': '100', 'value': 100},
                    {'label': '150', 'value': 150},
                    {'label': '200', 'value': 200}
                ],
                value=200
            ),
        ]),

        dbc.Col([
            dbc.Label("Gênero:"),
            dbc.Select(
                id='select_genre_filter',
                options=[
                    {'label': '(Todos)', 'value': 'all'},
                    {'label': 'Drama', 'value': 'Drama'},
                    {'label': 'Comédia', 'value': 'Comedy'},
                    {'label': 'Ação', 'value': 'Action'},
                    {'label': 'Romance', 'value': 'Romance'},
                    {'label': 'Criminal', 'value': 'Crime'},
                    {'label': 'Suspense', 'value': 'Thriller'},
                    {'label': 'Terror', 'value': 'Horror'},
                    {'label': 'Aventura', 'value': 'Adventure'},
                    {'label': 'Mistério', 'value': 'Mistery'},
                    {'label': 'Fantasia', 'value': 'Fantasy'},
                    {'label': 'Ficção Científica', 'value': 'Sci-Fi'},
                    {'label': 'Biografia', 'value': 'Biography'},
                    {'label': 'História', 'value': 'History'},
                    {'label': 'Guerra', 'value': 'War'},
                    {'label': 'Animação', 'value': 'Animation'},
                    {'label': 'Musical', 'value': 'Musical'},
                    {'label': 'Faroeste', 'value': 'Western'},
                    {'label': 'Documentário', 'value': 'Documentary'}
                ],
                value='all'
            ),
        ]),

        dbc.Col([
            dbc.Label("Ordenar por:"),
            dbc.Select(
                id='select_sort_filter',
                options=[
                    {'label': '(Sem ordenação)', 'value': 'none'},
                    {'label': 'Ano', 'value': 'year'},
                    {'label': 'Nota', 'value': 'rating'},
                    {'label': 'Ano e Nota', 'value': 'year_and_rating'}
                ],
                value='none'
            ),
        ]),

        dcc.Graph(id='ranking_bar', figure=ranking_graph.get_graph())
    ]),

], fluid=True)


# Callback for 1st graph (movies number per year/genre)
@callback(
    Output(component_id='movies_graph', component_property='figure'),
    Input(component_id='movies_items', component_property='value')
)

def update_movies_graph(value):
    if value == 'genero':
        return genre_distribution_graph()
    elif value == 'ano':
        return movies_per_year_graph()
    else:
        return None


# Ranking Graph Callback
@callback(
    Output(component_id='ranking_bar', component_property='figure'),
    Input(component_id='select_sample_filter', component_property='value'),
    Input(component_id='select_sample_size_filter', component_property='value'),
    Input(component_id='select_genre_filter', component_property='value'),
    Input(component_id='select_sort_filter', component_property='value'),
)

def update_ranking_graph(sample_type, sample_size, genre, sorting):
    return ranking_graph.update_graph(sample_type, int(sample_size), genre, sorting)



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
