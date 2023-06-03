# Imports
from sklearn.cluster import KMeans

def kmeans_fit(train_data, N_clusters=5, max_iterations=500, n_iterations=100):
    model = KMeans(n_clusters=N_clusters, init='k-means++', max_iter=max_iterations, n_init=n_iterations)
    model.fit(train_data)
    return model 

def kmeans_predict(model, X_test):    
    prediction = model.predict(X_test)
    return int(prediction)

def add_prediction(data, model):
    data['ClusterPrediction'] = data['text'].apply(lambda x: kmeans_predict(model, x))
    return data