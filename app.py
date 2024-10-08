from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os, re
import pandas as pd
from src.model import load_model, predict_single_url, predict_multiple_urls  # Import your prediction functions
from src.sreenshot import screehotter

app = Flask(__name__)

# Set up the folder for storing uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model, scaler = load_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url_type = request.form.get('url_type')
    
    if url_type == 'single':
        url = request.form.get('url')

        #clean url
        url = re.sub(r'^https?:\/\/(www\.)?', '', url.lower())
        url = re.sub(r'(www\.)?', '', url.lower())

        result, proba = predict_single_url(url,model,scaler)
        screenshotpath = None
        if result == "Scammy":
            screenshotpath = screehotter(url)

        if result:
            return jsonify({
                "url": url,
                "result": result,
                "scammy_probability": proba,
                "screenshot_path": screenshotpath
            })
        else:
            return jsonify({"error": "Prediction failed"}), 500
    
    elif url_type == 'multiple':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Read the CSV file and get URLs
            try:
                df = pd.read_csv(filepath)
                df = df['Domain']
                df = pd.DataFrame(df)
                df.rename(columns = {"Domain" : "url"}, inplace=True)

                if 'url' not in df.columns:
                    return jsonify({"error": "CSV file must contain a 'url' column"}), 400
                
                # urls = df['url'].tolist()
                results = predict_multiple_urls(df,model,scaler)
                formatted_results = [{
                    "url": res.get("url"),
                    "result": res.get("result"),
                    "scammy_probability": res.get("scammy_probability"),
                    "screenshot_path": res.get("screenshot_path")
                } for res in results]

                return jsonify({"results": formatted_results})
            
            except Exception as e:
                return jsonify({"error": str(e)}), 400
    
    return jsonify({"error": "Invalid URL input"}), 400

if __name__ == '__main__':
    app.run(debug=True)
