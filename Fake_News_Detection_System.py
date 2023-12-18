from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import spacy

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

nlp = spacy.load("en_core_web_sm")

csv_file_path = 'preprocessed_dataset.csv'  
df = pd.read_csv(csv_file_path)
dataset = df['Headline'].tolist()

dummy_user = {'username': 'pratik@123', 'password': 'dkte123'}

def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def extract_features(input_text, dataset):
    dataset_preprocessed = [preprocess_text(headline) for headline in dataset]
    input_text_preprocessed = preprocess_text(input_text)

    input_doc = nlp(input_text_preprocessed)
    dataset_docs = [nlp(headline) for headline in dataset_preprocessed]

    similarity_scores = [input_doc.similarity(doc) for doc in dataset_docs]

    return max(similarity_scores)  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']

        if username == dummy_user['username'] and password == dummy_user['password']:
            session['username'] = username
            return render_template('index.html')  
        else:
            error_message = 'Invalid username or password'
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('login.html')

@app.route('/analyse', methods=['POST'])
def analyse():
    user_input = request.form['user_input']

    if len(user_input.split()) > 15:
        error_message = 'Please enter a headline with 15 words or less.'
        return render_template('index.html', error_message=error_message)

    predicted_label = detect_fake_news(user_input, dataset)
    data = {
        'res': {
            'input': user_input,
            'predicted_label': predicted_label
        }
    }
    return render_template('index.html', data=data)

@app.route('/', methods=['GET', 'POST'])
def index():
    if dummy_user["username"] not in session:
        return render_template('login.html')
    else:
        return render_template('index.html')

def detect_fake_news(line, dataset, similarity_threshold=0.7):
    similarity_score = extract_features(line, dataset)
    if similarity_score >= similarity_threshold:
        return "Real"
    else:
        return "Fake"  

if __name__ == '__main__':
    app.run(debug=True)
