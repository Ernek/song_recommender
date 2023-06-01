# Imports
from sklearn.cluster import KMeans
from sklearn import metrics 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing

vectorizer = TfidfVectorizer(stop_words='english')

def vectorize_text(text_field):
    """
    Function to transform text field into numerical vector 
    Using NLP tfid method
    Args:
        
    """
    X_train = vectorizer.fit_transform(text_field)
    #print(X_train)
    print(f"n_samples: {X_train.shape[0]}, n_features: {X_train.shape[1]}")
    return X_train

def kmeans_fit(train_data, N_clusters=5, max_iterations=500, n_iterations=100):
    model = KMeans(n_clusters=N_clusters, init='k-means++', max_iter=max_iterations, n_init=n_iterations)
    model.fit(train_data)
    return model 

def kmeans_predict(model, str_input):
    if isinstance(str_input, str):
        # It is a single string element thus we cannot use list() and have to use brackets [] to transform to list
        X_test = vectorizer.transform([str_input])
        prediction = model.predict(X_test)
    else:
        # if is not a single string element so we can transform into a list directly using list()
        X_test = vectorizer.transform(list(str_input))
        prediction = model.predict(X_test)
    return int(prediction)

def add_prediction(data, model):
    data['ClusterPrediction'] = data['text'].apply(lambda x: kmeans_predict(model, x))
    return data