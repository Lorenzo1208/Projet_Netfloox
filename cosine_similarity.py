import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import numpy as np
import time

def load_data(csv_file):
    return pd.read_csv(csv_file, encoding='utf-8')

def get_similar_movies(movie_title, data, cv, count_matrix, svd, n_similar=5):
    liked_movie_idx = data[data['originalTitle'] == movie_title].index

    if len(liked_movie_idx) > 0:
        cosine_sim_light = cosine_similarity(X=count_matrix[liked_movie_idx], Y=count_matrix)
        row = cosine_sim_light[0]
        indices = np.argsort(-row)[1:n_similar+1]

        print(f"Les {n_similar} films les plus similaires à '{movie_title}' sont:")
        for i in indices:
            movie = data.iloc[i]['originalTitle']
            print(f"{movie} ({row[i]:.2f})")
    else:
        print(f"Aucun film trouvé avec le titre '{movie_title}'.")

def main():
    start_time = time.time()

    # Chargement des données
    data = load_data('cosine_features_no_date.csv')

    # Préparation des données
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['features']).tocsr()
    svd = TruncatedSVD(n_components=1)
    count_matrix_svd = svd.fit_transform(count_matrix)

    # Recherche de films similaires
    liked_movie = 'John Wick'
    get_similar_movies(liked_movie, data, cv, count_matrix, svd)

    elapsed_time = time.time() - start_time
    print(f"Temps d'exécution : {elapsed_time:.2f} secondes.")

if __name__ == '__main__':
    main()