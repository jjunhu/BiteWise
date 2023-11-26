import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_features(input_path, output_path):
    """
    Function to extract features from the preprocessed data.
    :param input_path: path to the processed data file
    :param output_path: path to save the file with extracted features
    """
    df = pd.read_csv(input_path)

    # Using TF-IDF Vectorizer for text vectorization
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(df['review_text'])

    # Convert to DataFrame
    features = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())

    # Assuming 'label' is the column with sentiment labels
    features['label'] = df['label']

    # Save the features
    features.to_csv(output_path, index=False)

if __name__ == "__main__":
    processed_data_path = 'data/processed/processed_yelp_dataset.csv'
    features_data_path = 'data/processed/features.csv'
    extract_features(processed_data_path, features_data_path)
