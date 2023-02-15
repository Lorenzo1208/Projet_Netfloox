import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import numpy as np

data = pd.read_csv('17000_features_index.csv', encoding='utf-8')
data = data.head(10000)

cv = CountVectorizer()
count_matrix = cv.fit_transform(data['features']).tocsr()

svd = TruncatedSVD(n_components=1000)
count_matrix_svd = svd.fit_transform(count_matrix)

cosine_sim_svd = cosine_similarity(count_matrix_svd)

liked_movie = 'Admiral'

liked_movie_idx = data[data['originalTitle'] == liked_movie].index

if len(liked_movie_idx) > 0:
    idx = liked_movie_idx[0]

    row = cosine_sim_svd[idx]
    indices = np.argsort(-row)[1:6]

    print(f"Les 5 films les plus similaires à '{liked_movie}' sont:")
    for i in indices:
        movie = data.iloc[i]['originalTitle']
        print(f"{movie} ({row[i]:.2f})")
else:
    print(f"Aucun film trouvé avec le titre'{liked_movie}'.")
