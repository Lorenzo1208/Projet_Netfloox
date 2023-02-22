from django.shortcuts import render
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import base64
import numpy as np
import os

# Get the current working directory
cwd = os.getcwd()
print(f"Current working directory: {cwd}")

# List the files in the current working directory
files = os.listdir(cwd)
print(f"Files in directory: {files}")

def home(request):
    return render(request, 'home.html')

def analyses(request):

    return render(request, 'analyses.html')

def load_data(csv_file):
    return pd.read_csv(csv_file, encoding='utf-8')

def get_similar_movies(movie_title, data, cv, count_matrix, svd, n_similar=5):
    liked_movie_idx = data[data['originalTitle'] == movie_title].index

    if len(liked_movie_idx) > 0:
        cosine_sim_light = cosine_similarity(X=count_matrix[liked_movie_idx], Y=count_matrix)
        row = cosine_sim_light[0]
        indices = np.argsort(-row)[1:n_similar+1]
        
        movies = []
        for i in indices:
            movie = data.iloc[i]['originalTitle']
            similarity = round(row[i] * 100, 2)
            movies.append((movie, similarity))
            print(f"{movie} ({similarity}%)")
    else:
        movies = [(f"Aucun film trouvé avec le titre '{movie_title}'.", 0)]

    return movies


def prediction(request):
    data = load_data('https://raw.githubusercontent.com/Lorenzo1208/Projet_Netfloox/main/cosine_features_no_date.csv')

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['features']).tocsr()
    svd = TruncatedSVD(n_components=1)
    count_matrix_svd = svd.fit_transform(count_matrix)

    liked_movie = request.GET.get('movie', 'The Matrix')
    movies = get_similar_movies(liked_movie, data, cv, count_matrix, svd)

    context = {
        'movies': movies,
        'liked_movie': liked_movie,
    }
    return render(request, 'prediction.html', context)