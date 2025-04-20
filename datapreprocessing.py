import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

# Load the dataset (replace 'your_dataset.csv' with the actual file path)


dataset = pd.read_csv('news_headlines_combined.csv')
# Data Cleaning and Preprocessing
def preprocess_text(text):
    text = re.sub(r'<.*?>', '', text)
    
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    
    text = text.lower()
    
    words = word_tokenize(text)
    
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    text = ' '.join(words)
    
    return text
dataset['Headline'] = dataset['Headline'].apply(preprocess_text)
dataset.to_csv('preprocessed_dataset.csv', index=False)



