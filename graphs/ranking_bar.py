import plotly.express as px

SAMPLE_NUM = 200

def ranking_bar_graph(df):
    fig = px.bar(df.sample(n=SAMPLE_NUM), x='tconst', y='averageRating', color='year', color_continuous_scale='Reds')

    fig.update_traces(hovertemplate='Filme: %{text}<br>Nota: %{y}<br>Ano: %{marker.color}', text=df['title'])

    fig.update_layout(
    xaxis_title=None,
    yaxis_title='Nota',
    coloraxis_colorbar=dict(title='Ano')
    )

    fig.update_xaxes(showticklabels=False)

    return fig