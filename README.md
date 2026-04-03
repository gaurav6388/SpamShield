# SpamShield - Intelligent Spam Email Classification System

## 📧 Description

The **Spam Mail Classification** project is a streamlined, high-performance web application designed to automatically categorize emails and text messages as either **Spam** or **Not Spam (Ham)**. Utilizing advanced machine learning techniques, the app provides real-time detection through a clean and modern user interface.

This version has been optimized for speed and simplicity, removing the need for user accounts or databases to focus purely on the core classification tool.

## ✨ Key Features

- **Real-Time Classification**: Instant detection using an Ajax-based dynamic interface.
- **Premium UI**: Modern design featuring smooth animations, themed result badges, and a custom loading state.
- **Dark & Light Mode**: Seamlessly toggle between themes for the best viewing experience.
- **Text Preprocessing**: Robust data cleaning including tokenization, lowercasing, and stemming (PorterStemmer).
- **Machine Learning Core**: Employs a fitted `TfidfVectorizer` paired with a `MultinomialNB` classifier for high accuracy.

## 👥 Authors

- **Gaurav Singh** — Frontend Development
- **Gyanendra Singh** — Backend & Machine Learning

## 🛠️ Technologies Used

- **Flask** (Python Web Framework): Backend logic and routing.
- **HTML5, CSS3, & JS (ES6+)**: Frontend structure, styling (Bootstrap), and dynamic interactions.
- **Scikit-Learn**: Machine learning model training and vectorization.
- **NLTK**: Natural Language Toolkit for advanced text processing.

## 🚀 Getting Started

Follow these steps to run the application locally:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   ```

2. **Install Dependencies**:
   Ensure you have Python installed, then run:
   ```bash
   pip install flask scikit-learn nltk
   ```

3. **Required NLTK Resources**:
   The app will automatically attempt to download required resources, but you can manually ensure they are present:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('punkt_tab')
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```
   Open your browser and navigate to `http://127.0.0.1:5000/`.

---
*Created as a part of the Advanced Machine Learning & Web Integration project.*