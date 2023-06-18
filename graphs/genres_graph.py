import pandas as pd
import plotly.express as px

class GenresGraph:
    def __init__(self, df):
        self.df = df

    def create_box_plot(self, top_n=10):
        self.df['genre'] = self.df['genres'].str.split(',')
        self.df = self.df.explode('genre')

        self.df['averageRating'] = pd.to_numeric(self.df['averageRating'])

        genre_avg_ratings = self.df.groupby('genre')['averageRating'].mean()

        top_genres = genre_avg_ratings.sort_values(ascending=False).head(top_n) # Selecting the top n genres
        filtered_movies = self.df[self.df['genre'].isin(top_genres.index)]
        genre_order = top_genres.index

        fig = px.box(filtered_movies, x='genre', y='averageRating', labels={'genre': 'Genero','averageRating': 'Nota'},
                     category_orders={'genre': genre_order}, hover_data=['title'])


        fig.update_traces(hovertemplate='Title: %{customdata[0]}<br>Rating: %{y}')

        return fig
