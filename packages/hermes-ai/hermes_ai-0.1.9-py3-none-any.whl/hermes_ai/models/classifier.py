import pandas as pd
from .data_processor import clean_text

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

from importlib.resources import files
import joblib

def process_data():
    #load and process data sets
    ds_synthetic_path = files('hermes_ai.data').joinpath('synthetic_messages.csv')
    df_synthetic = pd.read_csv(ds_synthetic_path)
    ds_real_path = files('hermes_ai.data').joinpath('messages_actions.csv')
    df_real = pd.read_csv(ds_real_path)
    df = pd.concat([df_synthetic,df_real])
    df['clean_message'] = df['message'].apply(clean_text)
    c_df = df[['clean_message', 'action']]

    #split data into test-train
    X=c_df['clean_message']
    y=c_df['action']
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.1, random_state=1)
    
    #vectorize the data with bag-of words method
    count_vect = CountVectorizer(min_df=0.0, ngram_range=(1,2))
    X_train_counts = count_vect.fit_transform(X_train)
    X_test_counts = count_vect.fit_transform(X_test)

    #save vectorizer    
    vectorizer_path = files('hermes_ai.models').joinpath('vectorizer')
    joblib.dump(count_vect, vectorizer_path)

    return X_train_counts, X_test_counts, y_train, y_test

def train():
    
    X_train_counts, _ , y_train, _ = process_data()

    #take Naive Bayes classifier as model
    nb = MultinomialNB(alpha=1)
    nb.fit(X_train_counts, y_train)

    #save model
    classifier_path = files('hermes_ai.models').joinpath('classifier_model')
    joblib.dump(nb, classifier_path)

def score():
    _ , X_test_counts, _ , y_test = process_data()

    classifier_path = files('hermes_ai.models').joinpath('classifier_model')
    nb = joblib.load(classifier_path)
    y_pred =  nb.predict(X_test_counts)
    score = metrics.accuracy_score(y_test, y_pred)
    return score
    
def confusion_matrix():
    #create confusion matrix
    y_pred , y_test = process_data()
    labels = ['make appointment', 'cancel appointment', 'reschedule appointment', 'refer previous message', 'forward information', 'reply', 'ignore']
    cm = metrics.confusion_matrix(y_test, y_pred, labels = labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    return cm_df