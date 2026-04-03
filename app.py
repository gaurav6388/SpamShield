# Robust SpamShield App
from flask import Flask, render_template, request, jsonify
import pickle
import string
import nltk
from nltk.stem import PorterStemmer
import os

project_root = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'public', 'static')

app = Flask(__name__, template_folder=template_path, static_folder=static_path)
ps = PorterStemmer()

# --- Robust Model Loading ---
try:
    vectorizer_path = os.path.join(project_root, 'vectorizer.pkl')
    model_path = os.path.join(project_root, 'model.pkl')
    
    with open(vectorizer_path, 'rb') as f:
        tfidf = pickle.load(f)
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print(f"CRITICAL ERROR: Could not load model files. Please ensure vectorizer.pkl and model.pkl exist. Error: {e}")
    tfidf = None
    model = None

# --- Optimized NLTK Download for Cloud (Vercel/Render) ---
# On Vercel, /tmp is the only writable directory
nltk_data_path = os.path.join('/tmp', 'nltk_data')
if not os.path.exists(nltk_data_path):
    try:
        os.makedirs(nltk_data_path)
    except:
        pass # Fallback if /tmp is not writable

nltk.data.path.append(nltk_data_path)

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading required NLTK resources...")
    nltk.download('punkt', download_dir=nltk_data_path)
    nltk.download('punkt_tab', download_dir=nltk_data_path)
    nltk.download('stopwords', download_dir=nltk_data_path)

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def transform_text(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    # Optimized: Alphanumeric only, no punctuation, NO STOPWORDS
    y = [ps.stem(i) for i in tokens if i.isalnum() and i not in string.punctuation and i not in stop_words]
    return " ".join(y)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or tfidf is None:
        return jsonify({'error': 'Machine Learning model is not loaded on the server.'}), 500
        
    try:
        input_sms = request.form.get('message', '').strip()
        if not input_sms:
            return jsonify({'error': 'No input message provided.'}), 400
            
        # 1. Transform input
        transformed_sms = transform_text(input_sms)
        
        # 2. Vectorize
        vector_input = tfidf.transform([transformed_sms])
        
        # 3. Predict Probability
        proba = model.predict_proba(vector_input)[0]
        prediction_val = model.predict(vector_input)[0]
        
        # DEBUG LOGGING (Check your terminal)
        print(f"\n--- Prediction Debug ---")
        print(f"Raw Input: {input_sms}")
        print(f"Transformed: {transformed_sms}")
        print(f"Probabilities: Ham={proba[0]:.4f}, Spam={proba[1]:.4f}")
        print(f"Final Prediction: {'Spam' if prediction_val == 1 else 'Not Spam'}")
        print(f"------------------------\n")
        
        # 4. Format Confidence
        confidence = round(proba[prediction_val] * 100, 1)
        prediction = "Spam" if prediction_val == 1 else "Not Spam"
            
        return jsonify({
            'prediction': prediction,
            'confidence': confidence
        })
    except Exception as e:
        return jsonify({'error': f"Internal Analysis Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Local development server
    app.run(host='0.0.0.0', port=5000, debug=True)


