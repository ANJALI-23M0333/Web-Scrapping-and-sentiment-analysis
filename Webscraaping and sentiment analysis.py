# -*- coding: utf-8 -*-
"""BlackCoffer_internship_assignment

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SkC8laZHN_fGqyDAc_jGui0Se-pp24fX
"""

pip install pandas requests beautifulsoup4

import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# Function to extract plain text article content
def extract_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting the article content from <div> tag with class "td-post-content tagdiv-type"
    article_content = soup.find('div', class_='td-post-content tagdiv-type')
    if article_content:
        text = article_content.get_text(separator='\n\n', strip=True)
    else:
        text = 'No Article Content Found'









pip install pandas requests beautifulsoup4

from google.colab import files
import pandas as pd
data = files.upload()

from google.colab import files
import pandas as pd
data = files.upload()

input_csv = pd.read_csv('articles_urls.csv')

input_file  = pd.read_excel("input.xlsx")

import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

def extract_article_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: Extract all paragraphs
        paragraphs = soup.find_all('p')
        article_text = '\n'.join([para.get_text() for para in paragraphs])

        if not article_text:
            return None

        return article_text
    except Exception as e:
        print(f"Error extracting article text from {url}: {e}")
        return None

# Read the Excel file
input_file = 'input.xlsx'
df = pd.read_excel(input_file)

# Directory to save the extracted articles
output_dir = 'extracted_articles'
os.makedirs(output_dir, exist_ok=True)

# Loop through each URL and extract content
for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    try:
        print(f"Extracting content from URL: {url}")
        text = extract_article_text(url)

        if text is None:
            raise ValueError("Extracted text is None")

        # Save content to a text file
        output_file = os.path.join(output_dir, f"{url_id}.txt")
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(text)

        print(f"Successfully extracted and saved content for {url_id}")
    except Exception as e:
        print(f"Failed to extract content for {url_id}: {e}")

!pip install textstat

import os
import csv
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import re
import textstat

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Define positive and negative dictionaries (assuming you have these)
positive_words = {'good', 'happy', 'excellent'}  # Example positive words
negative_words = {'bad', 'sad', 'poor'}           # Example negative words

# Function to read text from a file
def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Function to clean text and remove stopwords and punctuation
def clean_text(text):
    # Tokenize text into words
    words = word_tokenize(text)

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    cleaned_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

    return cleaned_words

# Function to calculate derived variables
def calculate_derived_variables(text):
    if not text:
        return None

    # Clean text
    cleaned_words = clean_text(text)
    total_words = len(cleaned_words)

    # Calculate Positive Score and Negative Score
    positive_score = sum(1 for word in cleaned_words if word in positive_words)
    negative_score = sum(1 for word in cleaned_words if word in negative_words) * -1

    # Calculate Polarity Score
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

    # Calculate Subjectivity Score
    subjectivity_score = (positive_score + negative_score) / (total_words + 0.000001)

    return {
        'positive_score': positive_score,
        'negative_score': negative_score,
        'polarity_score': polarity_score,
        'subjectivity_score': subjectivity_score
    }

# Function to calculate readability metrics
def calculate_readability_metrics(text):
    if not text:
        return None

    # Tokenize sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    # Calculate metrics
    avg_sentence_length = len(words) / len(sentences)

    # Calculate percentage of complex words
    complex_word_count = 0
    for word in words:
        syllables = textstat.syllable_count(word)
        if syllables > 2:  # Adjust this threshold as needed
            complex_word_count += 1

    percentage_complex_words = complex_word_count / len(words) * 100

    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = len(words) / len(sentences)
    word_count = len(words)
    syllable_per_word = textstat.syllable_count(text) / len(words)

    return {
        'avg_sentence_length': avg_sentence_length,
        'percentage_complex_words': percentage_complex_words,
        'fog_index': fog_index,
        'avg_words_per_sentence': avg_words_per_sentence,
        'word_count': word_count,
        'syllable_per_word': syllable_per_word
    }

# Function to count personal pronouns
def count_personal_pronouns(text):
    if not text:
        return None

    # Define personal pronouns
    personal_pronouns = ['i', 'we', 'my', 'ours', 'us']

    # Count occurrences of personal pronouns
    count = sum(1 for word in clean_text(text) if word.lower() in personal_pronouns)

    return count

# Function to calculate average word length
def calculate_avg_word_length(text):
    if not text:
        return None

    words = clean_text(text)
    total_chars = sum(len(word) for word in words)
    avg_word_length = total_chars / len(words) if len(words) > 0 else 0

    return avg_word_length

# Function to process all text files in a directory
def process_text_files(directory_path, output_csv):
    results = []

    # Iterate through each file in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(directory_path, file_name)

            # Read text from file
            text = read_text_from_file(file_path)

            if text:
                # Calculate derived variables
                derived_variables = calculate_derived_variables(text)

                # Calculate readability metrics
                readability_metrics = calculate_readability_metrics(text)

                # Count personal pronouns
                personal_pronoun_count = count_personal_pronouns(text)

                # Calculate average word length
                avg_word_length = calculate_avg_word_length(text)

                # Prepare result dictionary
                result = {
                    'File_Name': file_name,
                    **derived_variables,
                    **readability_metrics,
                    'personal_pronoun_count': personal_pronoun_count,
                    'avg_word_length': avg_word_length
                }
                results.append(result)

    # Write results to output CSV
    if results:
        fieldnames = ['File_Name', 'positive_score', 'negative_score', 'polarity_score',
                      'subjectivity_score', 'avg_sentence_length', 'percentage_complex_words',
                      'fog_index', 'avg_words_per_sentence', 'word_count', 'syllable_per_word',
                      'personal_pronoun_count', 'avg_word_length']
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"Processed {len(results)} text files. Results saved to {output_csv}")

# Example usage
if __name__ == "__main__":
    directory_path = '/content/extracted_articles'
    output_csv = 'article_metrics.csv'
    process_text_files(directory_path, output_csv)



