import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK data if not already installed
nltk.download('stopwords')
nltk.download('punkt')

# Load the dataset (replace 'your_dataset.csv' with the actual file path)
dataset = pd.read_csv('news_headlines_combined.csv')



# Data Cleaning and Preprocessing
def preprocess_text(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove special characters and numbers, keep only letters
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    
    # Convert text to lowercase
    text = text.lower()
    
    # Tokenize the text
    words = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Join the cleaned words back into a sentence
    text = ' '.join(words)
    
    return text



# Apply the preprocessing function to the 'text' column
dataset['Headline'] = dataset['Headline'].apply(preprocess_text)


# Save the preprocessed dataset to a new CSV file (e.g., 'preprocessed_dataset.csv')
dataset.to_csv('preprocessed_dataset.csv', index=False)



# Display the first few rows of the preprocessed dataset
# print(dataset.head())
