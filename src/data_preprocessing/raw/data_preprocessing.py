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

def load_and_preprocess_data(review_file_path, business_file_path):
    """
    Function to load, preprocess, and merge Yelp dataset.
    :param review_file_path: path to the review data file
    :param business_file_path: path to the business data file
    :return: merged and preprocessed DataFrame
    """
    # Load the datasets
    df_review = pd.read_csv(review_file_path)
    df_business = pd.read_csv(business_file_path)

    # Drop unnecessary columns
    df_review = df_review[['review_id', 'user_id', 'business_id', 'stars', 'date', 'text']]
    df_business = df_business[['business_id', 'categories']]

    # Handle missing values
    df_review.dropna(subset=['text'], inplace=True)
    df_business.dropna(subset=['categories'], inplace=True)

    # Preprocess review text
    #df_review['text'] = df_review['text'].apply(preprocess_text)

    # Merge datasets on business_id
    df_merged = pd.merge(df_review, df_business, on='business_id', how='left')

    return df_merged

if __name__ == "__main__":
    review_file_path = 'yelp_academic_dataset_review.csv'
    business_file_path = 'yelp_academic_dataset_business.csv'
    merged_data = load_and_preprocess_data(review_file_path, business_file_path)
    merged_data.to_csv('processed_yelp_dataset.csv', index=False)
