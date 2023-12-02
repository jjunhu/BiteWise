import nltk
from nltk.corpus import wordnet
import random
import pandas as pd

# Ensure you've downloaded the required NLTK data
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

def synonym_replacement(sentence, n):
    words = sentence.split()
    new_words = words.copy()
    random_word_list = list(set([word for word in words if wordnet.synsets(word)]))
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = get_synonyms(random_word)
        if len(synonyms) >= 1:
            synonym = random.choice(list(synonyms))
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1
        if num_replaced >= n:  # Only replace up to n words
            break

    sentence = ' '.join(new_words)
    return sentence

def create_new_dataset_with_synonyms():
    # Load your dataset
    df = pd.read_csv('../../data/processed/gpt_review_summary.csv')

    # Augmenting data
    augmented_sentences = []
    for comment in df['Combined Comments']:
        augmented_sentences.append(synonym_replacement(comment, n=2))  # Replace up to 2 words

    # Add augmented data to DataFrame
    df_augmented = pd.DataFrame({'Restaurant Name': df['Restaurant Name'], 'Combined Comments': augmented_sentences, 'Summary': df['Summary']})

    # Combine original and augmented data
    df_combined = pd.concat([df, df_augmented], ignore_index=True)

    # Save the combined dataset
    df_combined.to_csv('../../data/augmented/augmented_dataset.csv', index=False)
    
    return df_augmented
