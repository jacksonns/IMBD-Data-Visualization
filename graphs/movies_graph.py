import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class MoviesGraph():
    def __init__(self, years_df, genres_df):
        self.years_df = years_df
        self.genres_df = genres_df

    def get_year_graph(self):
        frames = []
        for i in range(1, len(self.years_df['_id'])+1):
            frame_data = self.years_df[:i]
            frame = go.Frame(data=[go.Scatter(x=frame_data['_id'], y=frame_data['count'])])
            frames.append(frame)

        fig = go.Figure(
            data=[go.Scatter(x=self.years_df['_id'], y=self.years_df['count'])],
            frames=frames
        )

        fig.update_layout(
            xaxis_title="Ano",
            yaxis_title="Número de Filmes",
            showlegend=False,
            updatemenus=[
                dict(
                    type="buttons",
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[None, {"frame": {"duration": 350, "redraw": True}, "fromcurrent": True}]
                        ),
                        dict(
                            label="Pause",
                            method="animate",
                            args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]
                        )
                    ],
                    pad={"r": 20, "t": 20},
                    showactive=False,
                    x=0.1,
                    xanchor="right",
                    y=0,
                    yanchor="top"
                )
            ]
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