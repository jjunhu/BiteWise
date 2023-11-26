from flask import Flask, request, jsonify
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf

app = Flask(__name__)

# Load the BERT model
model = TFBertForSequenceClassification.from_pretrained('../models/advanced/bert_model')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def prepare_text(text):
    """
    Prepares text for sentiment analysis by the BERT model.
    """
    inputs = tokenizer(text, return_tensors="tf", truncation=True, padding=True, max_length=128)
    return inputs

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predicts the sentiment of the submitted review text.
    """
    data = request.get_json()
    text = data['text']
    inputs = prepare_text(text)
    prediction = model(inputs)[0]
    sentiment = tf.argmax(prediction, axis=1).numpy()[0]

    # Assuming 0 is negative and 1 is positive sentiment
    sentiment_label = 'Positive' if sentiment == 1 else 'Negative'

    return jsonify({'sentiment': sentiment_label})

if __name__ == '__main__':
    app.run(debug=True)
