from db import imdb_database
from download_data import download_and_extract
import pandas as pd
import os

db = imdb_database()

def load_movie_basics(db):
    print('DOWNLOADING DATA')
    download_and_extract('title.basics.tsv')
    movies = pd.read_csv('title.basics.tsv', sep='\t')
    movies = movies.query(" titleType == 'movie' ")

    print('INSERTING MOVIES INTO DATABASE')
    collection = db['movies.basics']
    data_json = movies.to_dict(orient='records')
    collection.insert_many(data_json)

    os.remove('title.basics.tsv')


#load_movie_basics(db)