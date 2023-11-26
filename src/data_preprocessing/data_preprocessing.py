import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure required NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    """
    Function to preprocess text data: tokenization, lowercasing, removing stop words, and lemmatization.
    :param text: input string to be processed
    :return: processed string
    """
    # Tokenization and lowercasing
    tokens = nltk.word_tokenize(text.lower())

    # Removing stop words and lemmatization
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    return ' '.join([lemmatizer.lemmatize(word) for word in tokens if word not in stop_words])

def preprocess_data(file_path, output_path):
    """
    Function to preprocess the Yelp dataset.
    :param file_path: path to the raw data file
    :param output_path: path to save the processed data file
    """
    df = pd.read_csv(file_path)

    # Assuming 'review_text' is the column with review texts
    df['review_text'] = df['review_text'].apply(preprocess_text)

    # Save the processed data
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    raw_data_path = 'data/raw/yelp_dataset.csv'
    processed_data_path = 'data/processed/processed_yelp_dataset.csv'
    preprocess_data(raw_data_path, processed_data_path)
