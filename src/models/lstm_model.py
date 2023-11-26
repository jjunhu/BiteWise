import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.utils import to_categorical
import tensorflow as tf

# Load the dataset
file_path = '../data/processed/processed_yelp_dataset.csv'
df = pd.read_csv(file_path)

# Preparing the Tokenizer
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(df['review_text'])

# Converting text to sequences of integers
sequences = tokenizer.texts_to_sequences(df['review_text'])
data = pad_sequences(sequences, maxlen=200)

# Label encoding the target variable
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(df['label'])
labels = to_categorical(encoded_labels)

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# LSTM Model
model = Sequential()
model.add(Embedding(input_dim=5000, output_dim=128, input_length=200))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(2, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Model summary
print(model.summary())

# Training the model
model.fit(X_train, y_train, epochs=5, batch_size=64, validation_data=(X_test, y_test))

# Save the model
model.save('../models/advanced/lstm_model.h5')
