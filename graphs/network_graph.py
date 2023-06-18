import networkx as nx
import plotly.graph_objects as go

class NetworkGraph():

    def __init__(self, df):
        self.df = df
        self.actor_df = df.head(100)

    def get_graph(self):
        grafo = nx.Graph()

        # Add nodes
        for actors in self.actor_df['actors']:
            grafo.add_nodes_from(actors)

        # Add actors
        for index, actors in enumerate(self.actor_df['actors']):
            for i in range(len(actors)):
                for j in range(i + 1, len(actors)):
                    grafo.add_edge(actors[i], actors[j], movie=self.actor_df['title'][index])

        pos = nx.spring_layout(grafo)

        x = []
        y = []
        for actor, position in pos.items():
            x.append(position[0])
            y.append(position[1])

        # Create graph using plotly
        fig = go.Figure()

        # Add edges to graph
        for edge in grafo.edges:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            movie = grafo.edges[edge]['movie']
            fig.add_trace(go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode='lines',
                line=dict(width=1, color='gray'),
                showlegend=False
            ))

            fig.add_trace(go.Scatter(
                x=[(x0 + x1) / 2],
                y=[(y0 + y1) / 2],
                mode='markers',
                marker=dict(size=0.001, color='rgba(0, 0, 0, 0)'),
                hovertemplate=f'{edge[0]} - {edge[1]}<br>Filme: {movie}<extra></extra>'
            ))

        # Add nodes to graph
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker=dict(size=10, color='#00008B'),
            text=list(pos.keys()),
            hovertemplate='%{text}<extra></extra>'
        ))

        # Config layout
        fig.update_layout(
            showlegend=False,
            hovermode='closest',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=600
        )

        return fig

    def get_actor_graph(self, actor):
        if actor:
            self.actor_df = self.df[self.df['actors'].apply(lambda actors: actor in actors)].reset_index(drop=True)
        else:
            self.actor_df = self.df.head(100)
        return self.get_graph()