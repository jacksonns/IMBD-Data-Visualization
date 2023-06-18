import plotly.express as px

MAX_SAMPLE_SIZE = 200

colors = {
    'all': 'pubu',
    'Drama': 'redor',
    'Comedy': 'sunsetdark',
    'Action': 'brwnyl',
    'Romance': 'purd',
    'Crime': 'Reds',
    'Thriller': 'darkmint',
    'Horror': 'hot_R',
    'Adventure': 'emrld',
    'Mystery': 'ice_R',
    'Fantasy': 'purples',
    'Sci-Fi': 'mint',
    'Biography': 'solar_R',
    'History': 'gray_R',
    'War': 'ylorrd',
    'Animation': 'magma_R',
    'Musical': 'rdpu',
    'Western': 'oranges',
    'Documentary': 'greys'
}


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
                     color='year', color_continuous_scale=colors[self.genre])

        fig.update_traces(customdata=self.df['title'], hovertemplate='Filme: %{customdata}<br>Nota: %{y}<br>Ano: %{marker.color}')

        fig.update_layout(
        xaxis_title=None,
        yaxis_title='Nota',
        coloraxis_colorbar=dict(title='Ano')
        )

        fig.update_xaxes(showticklabels=False)

        return fig
    
    def filter_by_genre(self, genre):
        if genre == 'all':
            self.filtered_df = self.movies_df
        else: 
            self.filtered_df = self.movies_df[self.movies_df['genres'].str.contains(genre)]

    def set_sample(self):
        if self.sample_type == 'random':
            self.df = self.filtered_df.sample(n=MAX_SAMPLE_SIZE).reset_index(drop=True)
        elif self.sample_type == 'ranking':
            self.df = self.filtered_df.sort_values(by='averageRating', ascending=False)
            self.df = self.df.head(MAX_SAMPLE_SIZE)
    
    def update_graph(self, sample_type, sample_size, genre, sorting):
        if genre != self.genre:
            self.filter_by_genre(genre)
            self.genre = genre

        if sample_type != self.sample_type:
            self.sample_type = sample_type
        
        self.set_sample()
        
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