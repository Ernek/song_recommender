from sklearn import metrics 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing


vectorizer = TfidfVectorizer(stop_words='english')

def vectorize_fit(text_field):
    """
    Function to transform text field into numerical vector and fit  
    Using NLP tfid method
    Args:
        
    """
    X_train = vectorizer.fit_transform(text_field)
    #print(X_train)
    print(f"n_samples: {X_train.shape[0]}, n_features: {X_train.shape[1]}")
    return X_train

def vectorize_transform(text_field):
    """
    Function to transform text field into numerical vector 
    Using NLP tfid method
    Args:
        
    """
    if isinstance(text_field, str):
        # It is a single string element thus we cannot use list() and have to use brackets [] to transform to list
        X_test = vectorizer.transform([text_field])
    else:
        # if is not a single string element so we can transform into a list directly using list()
        X_test = vectorizer.transform(list(text_field))
    #print(X_train)
    print(f"n_samples: {X_test.shape[0]}, n_features: {X_test.shape[1]}")
    return X_test
