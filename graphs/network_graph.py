import networkx as nx
import plotly.graph_objects as go

class NetworkGraph():

    def __init__(self, df):
        self.df = df

    def get_graph(self):
        grafo = nx.Graph()

        # Add nodes
        for actors in self.df['actors']:
            grafo.add_nodes_from(actors)

        # Add actors
        for index, actors in enumerate(self.df['actors']):
            for i in range(len(actors)):
                for j in range(i + 1, len(actors)):
                    grafo.add_edge(actors[i], actors[j], movie=self.df['title'][index])

        pos = nx.spring_layout(grafo)

        x = []
        y = []
        for actor, position in pos.items():
            x.append(position[0])
            y.append(position[1])

        # Create graph using plotly
        fig = go.Figure()

        # Add nodes to graph
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker=dict(size=10, color='blue'),
            text=list(pos.keys()),
            hovertemplate='%{text}<extra></extra>'
        ))

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
                hovertemplate=f'{edge[0]} - {edge[1]}<br>Filme: {movie}<extra></extra>'
            ))

        # Config layout
        fig.update_layout(
            showlegend=False,
            hovermode='closest',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )

        return fig



""" from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

def imdb_database():
    load_dotenv()

    client = MongoClient(os.getenv('MONGODB_URI'), server_api=ServerApi('1'))

    return client["imdb"]


if __name__=='__main__':
   db = imdb_database()
   fig = actors_network_graph(db)
   fig.show() """