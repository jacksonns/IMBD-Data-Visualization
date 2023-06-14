import plotly.express as px

MAX_SAMPLE_SIZE = 200

class RankingGraph:
    def __init__(self, movies_df) :
        self.movies_df = movies_df
        self.sample_type = 'random'
        self.sample_size = 200
        self.genre = 'all'
        self.sorting = 'none'
        self.df = self.movies_df.sample(n=MAX_SAMPLE_SIZE).reset_index(drop=True)
        self.filtered_df = self.df

    def get_graph(self):
        fig = px.bar(self.df.head(self.sample_size), 
                     x='tconst', y='averageRating', 
                     color='year', color_continuous_scale='Reds')

        fig.update_traces(hovertemplate='Filme: %{text}<br>Nota: %{y}<br>Ano: %{marker.color}', text=self.df['title'])

        fig.update_layout(
        xaxis_title=None,
        yaxis_title='Nota',
        coloraxis_colorbar=dict(title='Ano')
        )

        fig.update_xaxes(showticklabels=False)

        return fig
    
    def update_graph(self, sample_type, sample_size, genre, sorting):
        if genre != self.genre:
            if genre == 'all':
                self.df = self.movies_df.sample(n=MAX_SAMPLE_SIZE).reset_index(drop=True)
            else: 
                self.df = self.movies_df[self.movies_df['genres'].str.contains(genre)]
                if self.sample_type == 'random':
                    self.df = self.df.sample(n=MAX_SAMPLE_SIZE).reset_index(drop=True)
                elif self.sample_type == 'ranking':
                    self.df = self.df.sort_values(by='averageRating', ascending=False)
                    self.df = self.df.head(MAX_SAMPLE_SIZE)
            self.genre = genre

        if sample_type != self.sample_type and genre == self.genre:
            if sample_type == 'random':
                self.df = self.movies_df.sample(n=MAX_SAMPLE_SIZE).reset_index(drop=True)
            elif sample_type == 'ranking':
                self.df = self.movies_df.sort_values(by='averageRating', ascending=False)
                self.df = self.df.head(MAX_SAMPLE_SIZE)
            self.sample_type = sample_type
        
        if sample_size != self.sample_size:
            self.sample_size = sample_size
        
        if sorting == 'none':
            self.df =  self.df.sample(frac=1).reset_index(drop=True)
        elif sorting == 'year':
            self.df = self.df.sort_values(by='year', ascending=False)
        elif sorting == 'rating':
            self.df = self.df.sort_values(by='averageRating', ascending=False)
        elif sorting == 'year_and_rating':
            self.df = self.df.sort_values(by=['year', 'averageRating'], ascending=False)
        self.sorting = sorting

        return self.get_graph()