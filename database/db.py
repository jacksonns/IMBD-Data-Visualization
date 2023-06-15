from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import pandas as pd

class DBManager:

    def __init__(self):
        load_dotenv()
        client = MongoClient(os.getenv('MONGODB_URI'), server_api=ServerApi('1'))
        self.db = client["imdb"]


    def get_ranking_graph_data(self):
        collection = self.db['movies.data']
        pipeline = [
            {"$project": {"tconst": 1, "title": 1, 'year':1, "averageRating":1, "genres":1}},  # Desired Columns
        ]
        result = collection.aggregate(pipeline)
        return pd.DataFrame(result)


    def get_network_graph_data(self):
        collection = self.db['movies.data']
        # Aggregation to obtain the first 100 objects
        pipeline = [
            {"$project": {"tconst": 1, "title": 1, "actors": 1}},  # Desired Columns
            {"$limit": 100}  # 100 objects retrieved
        ]
        result = collection.aggregate(pipeline)
        return pd.DataFrame(result)
    
    
    def get_actors_list(self):
        collection = self.db['movies.data']
        pipeline = [
            {"$unwind": "$actors"},
            {"$group": {"_id": "$actors"}},
            {"$project": {"_id": 0, "actor": "$_id"}}
        ]
        result = collection.aggregate(pipeline)
        return [res["actor"] for res in result]


    def get_years_graph_data(self):
        # Years data
        collection = self.db['movies.basics']
        pipeline = [
        {"$group": {"_id": "$startYear", "count": {"$sum": 1}}}
        ]
        result = collection.aggregate(pipeline)
        years_df = pd.DataFrame.from_records(result)
        years_df = years_df.drop(years_df[years_df['_id'] == '\\N'].index)
        years_df = years_df.sort_values('_id')

        return years_df
    

    def get_genres_graph_data(self):
        collection = self.db['movies.basics']
        # Genres Data
        pipeline = [
        {"$project": {"genres": {"$split": ["$genres", ","]}}},  # Split genres
        {"$unwind": "$genres"},  # Unwind genres into separate documents
        {"$group": {"_id": "$genres", "count": {"$sum": 1}}}  # Group and count occurence of each genre
        ]
        result = collection.aggregate(pipeline)
        genres_df = pd.DataFrame.from_records(result)
        genres_df = genres_df.drop(genres_df[genres_df['_id'] == '\\N'].index)
        genres_df = genres_df.sort_values('count', ascending=False)

        return genres_df