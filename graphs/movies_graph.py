import pandas as pd
import plotly.express as px

class MoviesGraph():

    def __init__(self, years_df, genres_df):
        self.years_df = years_df
        self.genres_df = genres_df

    def get_year_graph(self):
        fig = px.line(self.years_df, x='_id',y='count')
        fig.update_layout(
            xaxis_title="Ano",
            yaxis_title="Número de Filmes",
            showlegend=False
        )
        return fig

    def get_genre_graph(self):
        fig = px.bar(self.genres_df, x='_id', y='count')
        fig.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False
        )

        return fig