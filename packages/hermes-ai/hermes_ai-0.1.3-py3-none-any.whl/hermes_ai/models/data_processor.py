#download necesary NTLK resources
#import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
import pandas as pd


#define function to clean and preprocess text
def clean_text(text):
    
    #tokenization
    tokens = word_tokenize(text)

    #remove tokens that are not purely letters
    tokens = [word for word in tokens if word.isalpha()]

    #lowercase the text
    tokens = [word.lower() for word in tokens]

    #remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    #lematization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    #join tokens back into a single string
    clean_text = ' '.join(tokens)
    return clean_text

def increase_data(old_df, new_df):
    if (not np.array_equal(old_df.columns,new_df.columns)):
        return 'Error: the data sets sets must have same columns'
    
    df = pd.concat([old_df,new_df])
    
    return df