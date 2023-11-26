import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, TFBertForSequenceClassification
from transformers import InputExample, InputFeatures
import tensorflow as tf

# Function to convert DataFrame into TensorFlow's InputExample
def convert_data_to_examples(train, test, DATA_COLUMN, LABEL_COLUMN): 
    train_InputExamples = train.apply(lambda x: InputExample(guid=None,
                                                            text_a = x[DATA_COLUMN], 
                                                            text_b = None,
                                                            label = x[LABEL_COLUMN]), axis = 1)

    validation_InputExamples = test.apply(lambda x: InputExample(guid=None,
                                                            text_a = x[DATA_COLUMN], 
                                                            text_b = None,
                                                            label = x[LABEL_COLUMN]), axis = 1)
  
    return train_InputExamples, validation_InputExamples

# Function to convert InputExamples to InputFeatures
def convert_examples_to_tf_dataset(examples, tokenizer, max_length=128):
    features = []

    for e in examples:
        input_dict = tokenizer.encode_plus(e.text_a, add_special_tokens=True, max_length=max_length, return_token_type_ids=True, return_attention_mask=True, pad_to_max_length=True, truncation=True)
        
        input_ids, token_type_ids, attention_mask = (input_dict["input_ids"], input_dict["token_type_ids"], input_dict["attention_mask"])

        features.append(InputFeatures(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids, label=e.label))

    def gen():
        for f in features:
            yield (
                {
                    "input_ids": f.input_ids,
                    "attention_mask": f.attention_mask,
                    "token_type_ids": f.token_type_ids,
                },
                f.label,
            )

    return tf.data.Dataset.from_generator(gen, ({"input_ids": tf.int32, "attention_mask": tf.int32, "token_type_ids": tf.int32}, tf.int32), ({'input_ids': tf.TensorShape([None]), 'attention_mask': tf.TensorShape([None]), 'token_type_ids': tf.TensorShape([None])}, tf.TensorShape([])))

# Load the dataset
file_path = '../data/processed/processed_yelp_dataset.csv'
df = pd.read_csv(file_path)

# Splitting the dataset
train_df, test_df = train_test_split(df, test_size=0.2)

# BERT Tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Convert data to InputExamples
train_InputExamples, validation_InputExamples = convert_data_to_examples(train_df, test_df, 'review_text', 'label')

# Convert InputExamples to TensorFlow Dataset
train_data = convert_examples_to_tf_dataset(list(train_InputExamples), tokenizer)
train_data = train_data.shuffle(100).batch(32).repeat(2)

validation_data = convert_examples_to_tf_dataset(list(validation_InputExamples), tokenizer)
validation_data = validation_data.batch(32)

# Load pre-trained BERT model
model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased')

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0), 
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
              metrics=[tf.keras.metrics.SparseCategoricalAccuracy('accuracy')])

# Model summary
print(model.summary())

# Train the model
model.fit(train_data, epochs=2, validation_data=validation_data)

# Save the model
model.save_pretrained('../models/advanced/bert_model')
