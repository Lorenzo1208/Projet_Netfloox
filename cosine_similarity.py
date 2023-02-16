import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import numpy as np
import time

start_time = time.time()

data = pd.read_csv('all_movies.csv', encoding='utf-8')

cv = CountVectorizer()
count_matrix = cv.fit_transform(data['features']).tocsr()

svd = TruncatedSVD(n_components=200)
count_matrix_svd = svd.fit_transform(count_matrix)

liked_movie = 'Avatar'

liked_movie_idx = data[data['originalTitle'] == liked_movie].index

if len(liked_movie_idx) > 0:
    cosine_sim_light = cosine_similarity(X = count_matrix[liked_movie_idx], Y = count_matrix)
    row = cosine_sim_light[0]
    indices = np.argsort(-row)[1:6]

    print(f"Les 5 films les plus similaires à '{liked_movie}' sont:")
    for i in indices:
        movie = data.iloc[i]['originalTitle']
        print(f"{movie} ({row[i]:.2f})")
else:
    print(f"Aucun film trouvé avec le titre'{liked_movie}'.")

elapsed_time = time.time() - start_time
print(f"Temps d'exécution : {elapsed_time:.2f} secondes.")
