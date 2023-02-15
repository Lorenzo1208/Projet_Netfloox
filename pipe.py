import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit
import pickle

# Charger les données
data = pd.read_csv('features_l.csv')
print(data.shape)
print(data.head())
print(data.columns)
# Extraire la variable cible
y = data['features'].str.split(',').str[0]

# Compter le nombre de films par classe
class_counts = y.value_counts()
print(class_counts)

# Filtrer les classes avec moins de 2 films
filtered_classes = class_counts[class_counts >= 2].index
mask = y.isin(filtered_classes)
data = data[mask]
y = y[mask]

# Définir le pipeline
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('knn', KNeighborsClassifier())
])

# Définir la grille de recherche
params = {
    'knn__n_neighbors': [3, 5, 7],
    'knn__weights': ['uniform', 'distance']
}

# Générer les indices pour la validation croisée stratifiée
cv = StratifiedShuffleSplit(n_splits=3, test_size=0.2, random_state=42)

grid_search = GridSearchCV(pipeline, params, cv=cv)

# Entraîner le modèle
grid_search.fit(data['features'], y)

# Afficher les meilleurs paramètres et le score
print('Best parameters:', grid_search.best_params_)
print('Best score:', grid_search.best_score_)

# Enregistrer le modèle entraîné à l'aide de pickle
with open('model.pkl', 'wb') as f:
    pickle.dump(grid_search.best_estimator_, f)
