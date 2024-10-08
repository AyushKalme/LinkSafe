from joblib import load
import pandas as pd
from src.data_processing import extract_features, flag_suspicious_url
from sklearn.preprocessing import StandardScaler
# from src.sreenshot import screehotter

# Load the pre-trained model and scaler
def load_model():
    model_path = "models/rf_model.joblib"  # Adjust the path if needed
    # scaler_path = "models/scaler.joblib"   # Adjust the scaler path if needed
    rf_model = load(model_path)
    scaler = StandardScaler()
    return rf_model, scaler

# Make predictions using the model
def predict_single_url(url, model, scaler):
    # Create a DataFrame with the URL
    df = pd.DataFrame([{'url': url}])

    # Step 1: Flag if suspicious words are found
    if flag_suspicious_url(url):
        return  "Suspicious (based on suspicious keywords)", 1

    # Step 2: Extract features and scale the necessary ones
    features = extract_features(df)

    

    features.drop(columns=['url'], errors='ignore', inplace=True)

    # Scale features
    features_to_scale = ['num_dots', 'domain_length', 'num_subdomains']
    # features_to_scale = ['num_dots', 'domain_length', 'num_subdomains']
    df[features_to_scale] = scaler.fit_transform(features[features_to_scale])
    df[features_to_scale] = scaler.transform(features[features_to_scale])
    # features[features_to_scale] = scaler.transform(features[features_to_scale])

    # Step 3: Make predictions using the random forest model
    proba = model.predict_proba(features)[:, 1]
    threshold = 0.5  # Adjust your threshold if necessary
    prediction = 'Scammy' if proba > threshold else 'Legitimate'

    # if prediction == 'Scammy':
    #     screehotter(url)

    # Return the prediction and probability
    return prediction, float(proba)

def predict_multiple_urls(df, model, scaler):
    # Assume df contains the URLs in a column named 'url'
    features_df = extract_features(df)  # Extract features for each URL

    X = df.drop(columns=['url'], errors='ignore')

    # Scale the necessary features
    features_to_scale = ['num_dots', 'domain_length', 'num_subdomains']
    X[features_to_scale] = scaler.fit_transform(X[features_to_scale])
    X[features_to_scale] = scaler.transform(X[features_to_scale])
    
    # Make predictions
    probabilities = model.predict_proba(X)[:, 1]
    threshold = 0.5  # Threshold for classification
    predictions = ['Scammy' if proba > threshold else 'Legitimate' for proba in probabilities]

    # Return the results as a list of dictionaries
    return [{"url": url, "result": result, "scammy_probability": float(proba)}
            for url, result, proba in zip(df['url'], predictions, probabilities)]














