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
import pickle
from sklearn.preprocessing import LabelEncoder
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

def score(request):
    if request.method == 'POST':
        # Collect the user inputs from the form
        title = request.POST.get('title', '')
        genres = request.POST.get('genres', '')
        actor = request.POST.get('actor', '')
        director = request.POST.get('director', '')
        runtime = request.POST.get('runtime', '')
        year = request.POST.get('year', '')

        # Check if runtime and year are valid integers
        try:
            if runtime:
                runtime = int(runtime)
            if year:
                year = int(year)
        except ValueError:
            return render(request, 'prediction2.html', {'error': 'Please enter valid runtime and year.'})

        # Check if title, genres, actor, and director are valid strings
        if not isinstance(title, str) or not isinstance(genres, str) or not isinstance(actor, str) or not isinstance(director, str):
            return render(request, 'prediction2.html', {'error': 'Please enter valid inputs for title, genres, actor, and director.'})

        # Create a DataFrame using the user inputs
        test_data = pd.DataFrame({
            'originalTitle': [title],
            'genres': [genres],
            'actor': [actor],
            'director': [director],
            'runtimeMinutes': [runtime] if runtime else [''],
            'startYear': [year] if year else [''],
            'averageRating': ['']
        })

        # Load the saved model
        model_path = 'app/RandomForestClassifier_model.pkl'
        with open(model_path, 'rb') as f:
            grid = pickle.load(f)

        # Prepare the input data
        le = LabelEncoder()
        test_data = test_data.apply(lambda col: le.fit_transform(col.astype(str)) if col.dtype == 'object' else col)

        # Make predictions
        X = test_data.drop(columns='averageRating')
        y_pred = grid.predict(X)

        # Pass the prediction to the template
        return render(request, 'score.html', {'prediction': y_pred[0]})

    return render(request, 'score.html')

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
    les_films = data["originalTitle"]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['features']).tocsr()
    svd = TruncatedSVD(n_components=1)
    count_matrix_svd = svd.fit_transform(count_matrix)

    liked_movie = request.GET.get('movie', 'The Matrix')
    movies = get_similar_movies(liked_movie, data, cv, count_matrix, svd)

    context = {
    'movies': movies,
    'liked_movie': liked_movie,
    'les_films': les_films
}
    return render(request, 'prediction.html', context)

