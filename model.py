import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, SGDRegressor, Lasso, ElasticNet, Ridge
from sklearn.svm import LinearSVC, SVC
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import fbeta_score
from sklearn.decomposition import PCA
import pickle
import joblib
import random
import time

def train_model(csv_file):
    df = pd.read_csv(csv_file)

    le = LabelEncoder()
    for col in df.select_dtypes(include=['object']):
        df[col] = le.fit_transform(df[col].astype(str))

    X = df.drop(columns='averageRating')
    y = df['averageRating']

    # Recodage des variables catégorielles avant la PCA
    transfo_cat = Pipeline(steps=[
        ('encoding', OneHotEncoder(handle_unknown='ignore', sparse=False))
    ])

    preparation = ColumnTransformer(
        transformers=[
            ('data_cat', transfo_cat, X.select_dtypes(include=['object']).columns),
            ('data_num', PCA(n_components=2), X.select_dtypes(exclude=['object']).columns),
            ('imputer', KNNImputer(n_neighbors=3, weights="uniform"), X.columns),
            ('scaler', RobustScaler(), X.columns)
        ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    return X_train, X_test, y_train, y_test, preparation


def train_models(X_train, X_test, y_train, y_test, preparation):
    # Liste des modèles à entraîner
    models = [
        KNeighborsClassifier(),
        RandomForestClassifier(),
        # LinearSVC(max_iter=10000),
        # SVC()
    ]

    # Liste des grilles de paramètres à tester pour chaque modèle
    grid_params = [
        # {'model__n_neighbors': [1, 5], 'model__p': [1]},
        # {'model__n_estimators': [10], 'model__max_depth': [10]},
        # {'model__C': [0.1, 1], 'model__loss': ['hinge', 'squared_hinge']},
        # {'model__C': [0.1, 1], 'model__kernel': ['linear', 'rbf'], 'model__gamma': ['scale', 'auto']}
    ]

    random_params = [
        # {'model__n_neighbors': [1, 5], 'model__p': [1]},
        # {'model__n_estimators': [10], 'model__max_depth': [10]},
        
        {'model__n_neighbors': [9], 'model__p': [1]}, # {'model__p': 1, 'model__n_neighbors': 11}
        {'model__n_estimators': [10], 'model__max_depth': [10]}, # {'model__n_estimators': 200, 'model__max_depth': 30}
        # {'model__C': [0.1, 1], 'model__loss': ['hinge', 'squared_hinge']},
        # {'model__C': [0.1, 1], 'model__kernel': ['linear', 'rbf'], 'model__gamma': ['scale', 'auto']}
    ]

    # Fonction pour choisir la méthode d'optimisation des hyperparamètres
    def get_search(method):
        if method == 'grid':
            return GridSearchCV
        elif method == 'random':
            return RandomizedSearchCV

    # Liste pour stocker les résultats des modèles
    results = []

    # Boucle pour entraîner chaque modèle
    for i, model in enumerate(models):
        pipeline = Pipeline(steps=[('preparation', preparation), ('model', model)])

        # Choix de la méthode d'optimisation des hyperparamètres
        search_method = get_search('random')

        # Modification aléatoire de la méthode de recherche
        # if random.random() < 0.5:
        #     search_method = get_search('random')

        # Entraînement du modèle avec l'optimisation des hyperparamètres
        if search_method == GridSearchCV:
            search_params = grid_params[i]
        else:
            search_params = random_params[i]

        search = RandomizedSearchCV(pipeline, search_params, scoring='f1_weighted', cv=5, n_jobs=-1, n_iter=1)
        # search = search_method(pipeline, search_params, scoring='f1_weighted', cv=5, n_jobs=-1)
        search.fit(X_train, y_train)

        y_pred = search.predict(X_test)
        test_score = fbeta_score(y_test, y_pred, average='weighted', beta=0.5)

        # Ajouter les résultats à la liste
        results.append((model, search.best_params_, test_score))

        # Sauvegarder le modèle dans un fichier pickle
        filename = f'{model.__class__.__name__}_model.pkl'
        with open(filename, 'wb') as f:
            pickle.dump(search.best_estimator_, f)

    return results

def predictAverageRating(df, model_path):
    # Load the saved model
    grid = joblib.load(model_path)

    # Prepare the input data
    le = LabelEncoder()
    df = df.apply(lambda col: le.fit_transform(col.astype(str)) if col.dtype == 'object' else col)

    # Make predictions
    X = df.drop(columns='averageRating')
    y_pred = grid.predict(X)

    return y_pred

def main():
    
    start_time = time.time()
    
    # Chemin vers le fichier de données
    csv_file = 'knn_features.csv'

    # Entraînement du modèle
    
    X_train, X_test, y_train, y_test, preparation = train_model(csv_file)
    results = train_models(X_train, X_test, y_train, y_test, preparation)

    # Affichage des scores et des meilleurs paramètres de chaque modèle
    
    for model, best_params, score in results:
        print(f'{model.__class__.__name__} best parameters: {best_params}')
        print(f'{model.__class__.__name__} test score: {score:.4f}\n')

    # Prédiction d'une note moyenne
    test_data = pd.DataFrame({
        'originalTitle': [''],
        'genres': ['Drama,History'],
        'actor': ['nm0000338'],
        'director': ['nm0001104'],
        'runtimeMinutes': [152],
        'startYear': [''],
        'averageRating': ['']
    })

    print(predictAverageRating(test_data, 'RandomForestClassifier_model.pkl'))
    
    elapsed_time = time.time() - start_time
    print(f"Temps d'exécution : {elapsed_time:.2f} secondes.")

if __name__ == '__main__':
    main()