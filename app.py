from flask import Flask, request, jsonify, render_template, url_for
from src.model import load_model, predict_single_url
from src.sreenshot import screehotter

# Initialize Flask app
app = Flask(__name__)

# Load the trained Random Forest model and scaler
model, scaler = load_model()

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML page

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Make prediction using the updated predict_url function
        result, scammy_probability = predict_single_url(url, model, scaler)
        
        screenshot_path = None
        if result == "Scammy":
            screenshot_path = screehotter(url)  # Take a screenshot if classified as scammy
            screenshot_url = url_for('static', filename=f'screenshots/scammy_site.png')

        return jsonify({
            "url": url,
            "result": result,
            "scammy_probability": scammy_probability,
            "screenshot_path": screenshot_path  # Return the screenshot path if available
        })
    # return jsonify({"url": url, "result": result, "scammy_probability": scammy_probability})
    except Exception as e:
        app.logger.error(f"Error in /predict: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)






















# import os
# import re
# from flask import Flask, render_template, request, jsonify
# from joblib import load
# from src.data_processing import extract_features
# import pandas as pd

# # List of suspicious keywords
# SUSPICIOUS_KEYWORDS = [
#     "money", "win", "free", "offer", "cash", "prize", "bonus", "credit", "loan", "earn", "income", "profits", "download",
#     "investment", "bank", "refinance", "withdraw", "transfer", "deposit", "payment", "wallet", "bitcoin",
#     "crypto", "forex", "payout", "reward", "check", "funds", "lottery", "jackpot", "porn", "adult", "xxx", "sex"
# ]

# # Function to check for suspicious words in a URL
# def flag_suspicious_url(url):
#     """Check if a URL contains any suspicious words."""
#     url_cleaned = re.sub(r'^https?:\/\/(www\.)?', '', url.lower())  # Clean the URL
#     return any(keyword in url_cleaned for keyword in SUSPICIOUS_KEYWORDS)

# # Load the Random Forest model and scaler
# MODEL_PATH = os.path.join('models', 'rf_model.joblib')
# SCALER_PATH = os.path.join('models', 'scaler.joblib')

# rf_model = load(MODEL_PATH)
# scaler = load(SCALER_PATH)

# app = Flask(__name__)

# # Serve the HTML front-end
# @app.route('/')
# def index():
#     return render_template('index.html')  # Serve the front-end from templates folder

# # Prediction API endpoint
# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()
#     url = data.get('url')

#     if not url:
#         return jsonify({"error": "No URL provided"}), 400
    
#     df = pd.DataFrame([{'url': url}])

#     # Step 1: Check for suspicious words
#     if flag_suspicious_url(url):
#         return jsonify({"result": "Scammy (Keyword Match)", "scammy_probability": 1.0})

#     # Step 2: If no suspicious words, proceed with model prediction
#     # Extract features
#     df = extract_features([url])  # Assuming extract_features takes a list of URLs and returns a DataFrame
    
#     # Scale features
#     features_to_scale = ['num_dots', 'domain_length', 'num_subdomains']
#     df[features_to_scale] = scaler.transform(df[features_to_scale])
    
#     # Make predictions
#     proba = rf_model.predict_proba(df)[:, 1]
#     threshold = 0.25  # Adjust your threshold if necessary
#     prediction = 'Scammy' if proba > threshold else 'Legitimate'
    
#     return jsonify({"result": prediction, "scammy_probability": float(proba)})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
