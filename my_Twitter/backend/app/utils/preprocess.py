from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import joblib
import os


# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Define absolute paths based on script directory
tfidf_vectorizer_path = os.path.join(script_dir, '../../models/tfidf_vectorizer.joblib')
tokenizer_path = os.path.join(script_dir, '../../models/tokenizer.pickle')

# Load the vecotrizer
tfidf_vectorizer = joblib.load(tfidf_vectorizer_path)

# Load the tokenizer
with open(tokenizer_path, 'rb') as handle:
    tokenizer = pickle.load(handle)

MAX_SEQUENCE_LENGTH = 55 

def preprocess_tfidf(texts):
    return tfidf_vectorizer.transform(texts)

def preprocess_cnn(texts):
    tweet_sequences = tokenizer.texts_to_sequences(texts)
    return pad_sequences(tweet_sequences, maxlen=MAX_SEQUENCE_LENGTH, padding='post')