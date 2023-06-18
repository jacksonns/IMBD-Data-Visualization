from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from database.db import DBManager
from graphs.network_graph import NetworkGraph
from graphs.ranking_bar import RankingGraph
from graphs.movies_graph import MoviesGraph
from graphs.genres_graph import GenresGraph

# Initialize the app and incorporate a Dash Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Get MongoDB database
db = DBManager()

# Initializing Graphs Classes.
df = db.get_ranking_graph_data()
ranking_graph = RankingGraph(df)
network_graph = NetworkGraph(db.get_network_graph_data())
movies_graph = MoviesGraph(db.get_years_graph_data(), db.get_genres_graph_data())
genres_graph = GenresGraph(df)

# Getting actor names for search bar
actors_list = db.get_actors_list()
actor_options =[{'label': actor, 'value': actor} for actor in actors_list]


app.layout = dbc.Container([
    dbc.Row([
        html.Div('Visualização de Dados IMDB', className="text-primary text-center fs-4")
    ]), 

    html.Hr(),

    dbc.Row([
        html.Div("Notas dos Filmes", 
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
                    {'label': 'Mistério', 'value': 'Mystery'},
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

    html.Hr(),

    dbc.Row([
        html.Div("Colaborações entre Atores", 
                 className="text-secondary text-center fs-4"),

        dbc.Label("Ator ou Atriz:"),

        dcc.Dropdown(
            id='actors_search_bar',
            placeholder='Digite para pesquisar um nome...'
        ),
        
        dcc.Graph(id='actors_network', figure=network_graph.get_graph(), style={'height': '100%'})
    ]),

    html.Hr(),

    dbc.Row([
        html.Div("Número de Filmes", 
                 className="text-secondary text-center fs-4", 
                 style={'margin-bottom': '20px'}),

        html.Div(
            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'},
            children=[
                dbc.RadioItems(
                    id='movies_items',
                    options=[
                        {'label': 'Por gênero', 'value': 'genre'},
                        {'label': 'Por ano', 'value': 'year'}
                    ],
                    value='genre',
                    inline=True
                )]
        ),

        dcc.Graph(id='movies_graph', figure=movies_graph.get_year_graph()),
    ]),

    dbc.Row([
        html.Div("Genero por nota", 
                 className="text-secondary text-center fs-4", 
                 style={'margin-bottom': '20px'}),

        dcc.Graph(id='genres_graph', figure=genres_graph.create_box_plot()),
    ]),


], fluid=True)



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



# Actors search Callback
@app.callback(
    Output('actors_search_bar', 'options'),
    [Input('actors_search_bar', 'search_value')]
)

def search_results(value):
    if not value:
        raise PreventUpdate()
    return [actor for actor in actor_options if value in actor["label"]]


@app.callback(
    Output('actors_network', 'figure'),
    [Input('actors_search_bar', 'value')]
)
def update_output(actor):
    return network_graph.get_actor_graph(actor)



# Callback for movies distribution (movies number per year/genre)
@callback(
    Output(component_id='movies_graph', component_property='figure'),
    Input(component_id='movies_items', component_property='value')
)

def update_movies_graph(value):
    if value == 'genre':
        return movies_graph.get_genre_graph()
    elif value == 'year':
        return movies_graph.get_year_graph()
    else:
        return None



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)