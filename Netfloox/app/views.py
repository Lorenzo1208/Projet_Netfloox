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
from plotly.offline import plot
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
    
    data = {'Type': ['short', 'movie', 'tvSeries', 'tvShort', 'tvMovie', 'tvEpisode', 'MiniSeries', 'tvSpecial', 'video', 'videoGame'], 
        'Values': [912188, 634638, 238073, 9923, 140297, 7262412, 47097, 40390, 270104, 33433]}
    df = pd.DataFrame(data)
    fig4 = px.pie(df, values='Values', names='Type', width=1000, height=500)
    fig4.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
)

    
    data = pd.read_csv('https://raw.githubusercontent.com/Lorenzo1208/Projet_Netfloox/main/knn_features_names.csv', encoding='utf-8')
    data = data.head(1000)
    df_drop_outliers = data.drop(data[data['runtimeMinutes'] > 2500].index)
    print(df_drop_outliers.columns)
    fig = px.scatter_matrix(df_drop_outliers,
    dimensions=["runtimeMinutes","startYear","averageRating"], color="averageRating", width=1000, height=500)
    fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',)
    
    data = pd.read_csv('https://raw.githubusercontent.com/Lorenzo1208/Projet_Netfloox/main/knn_features_names.csv', encoding='utf-8')
    df_director = data.groupby(['director']).mean()
    df_director['nombre_observations'] = data['director'].value_counts()
    df_director_top = df_director[['runtimeMinutes', 'startYear', 'averageRating', 'nombre_observations']].loc[df_director['nombre_observations'] >= 10].sort_values('averageRating', ascending=False).head(15)
    df_director_bottom = df_director[['runtimeMinutes', 'startYear', 'averageRating', 'nombre_observations']].loc[df_director['nombre_observations'] >= 10].sort_values('averageRating', ascending=False).tail(15)
    df_director_top.reset_index(inplace=True)
    df_director_bottom.reset_index(inplace=True)
    df_director = pd.concat([df_director_top, df_director_bottom])
    fig2 = px.bar(df_director, x='director', y='runtimeMinutes',hover_data=['runtimeMinutes', 'averageRating'], color='director', width=1000, height=500)
    fig2.add_vline(x=14.5, line_dash="dash", line_color="red")
    fig2.add_hline(y=100, line_dash="dash", line_color="blue")
    fig2.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',)
    
    data = pd.read_csv('https://raw.githubusercontent.com/Lorenzo1208/Projet_Netfloox/main/knn_features_names.csv', encoding='utf-8')
    df_genres = data.groupby(['genres']).mean()
    df_genres['nombre_observations'] = data['genres'].value_counts()
    df_genres = df_genres[['averageRating', 'nombre_observations']].loc[df_genres['nombre_observations'] >= 10].sort_values('averageRating', ascending=False)
    df_genres = df_genres.head(15)
    df_genre = df_genres.reset_index()
    vectorizer = CountVectorizer()
    tokens = vectorizer.fit_transform(df_genre['genres'])
    df_tokens = pd.DataFrame(tokens.toarray(), columns=vectorizer.get_feature_names_out())
    df_top_genre = df_tokens.sum().sort_values(ascending=False)
    df_top_genre = pd.DataFrame(df_top_genre)
    fig3 = px.bar(df_top_genre, x=df_top_genre[0].index, y=df_top_genre[0].values, width=1000, height=500, color=df_top_genre[0].values)
    fig3.update_layout(
    xaxis_title='13 premiers Genres',
    yaxis_title="Nombre d'occurences",
    plot_bgcolor='black',
    paper_bgcolor='black',
)

    return render(request, 'analyses.html', context={'plot': plot(fig, output_type='div'),'plot2': plot(fig2, output_type='div'),'plot3': plot(fig3, output_type='div'), 'plot4': plot(fig4, output_type='div')})



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
            return render(request, 'score.html', {'error': 'Please enter valid runtime and year.'})

        # Check if title, genres, actor, and director are valid strings
        if not isinstance(title, str) or not isinstance(genres, str) or not isinstance(actor, str) or not isinstance(director, str):
            return render(request, 'score.html', {'error': 'Please enter valid inputs for title, genres, actor, and director.'})

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
    import requests

    api_key = "ed0a9324"

    liked_movie_idx = data[data['originalTitle'] == movie_title].index

    if len(liked_movie_idx) > 0:
        cosine_sim_light = cosine_similarity(X=count_matrix[liked_movie_idx], Y=count_matrix)
        row = cosine_sim_light[0]
        indices = np.argsort(-row)[1:n_similar+1]

        movies = []
        for i in indices:
            movie = data.iloc[i]['originalTitle']
            similarity = round(row[i] * 100, 2)
            response = requests.get(f"http://www.omdbapi.com/?t={movie}&apikey={api_key}")
            json_response = response.json()
            poster_url = json_response.get("Poster")
            movies.append((movie, similarity, poster_url))
    else:
        movies = [(f"Aucun film trouvé avec le titre '{movie_title}'.", 0, '')]

    return movies


def recommandation(request):
    import requests

    api_key = "ed0a9324"

    data = load_data('https://raw.githubusercontent.com/Lorenzo1208/Projet_Netfloox/main/cosine_features_no_date.csv')
    les_films = data["originalTitle"]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['features']).tocsr()
    svd = TruncatedSVD(n_components=1)
    count_matrix_svd = svd.fit_transform(count_matrix)

    liked_movie = request.GET.get('movie', 'The Matrix')

    # Make a GET request to OMDb API to get the poster URL for the liked movie
    response = requests.get(f"http://www.omdbapi.com/?t={liked_movie}&apikey={api_key}")
    json_response = response.json()
    poster_url = json_response.get("Poster")

    movies = get_similar_movies(liked_movie, data, cv, count_matrix, svd)

    posters = []
    for movie in movies:
        posters.append(movie[2])
         

    context = {
        'movies': movies,
        'liked_movie': liked_movie,
        'les_films': les_films,
        'poster_url': poster_url,
        'posters': posters,
    }

    return render(request, 'recommandation.html', context)



