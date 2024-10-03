import re
import pandas as pd
from urllib.parse import urlparse

SUSPICIOUS_KEYWORDS = [
    "money", "win", "free", "offer", "cash", "prize", "bonus", "credit", "loan", "earn", "income", "profits",
    "investment", "bank", "refinance", "withdraw", "transfer", "deposit", "payment", "wallet", "bitcoin",
    "crypto", "forex", "payout", "reward", "check", "funds", "lottery", "jackpot", "porn", "adult", "xxx", "sex"
]


def clean_url(url):
    """Remove protocol (http/https) and www from URL."""
    
    return re.sub(r'^https?:\/\/(www\.)?', '', url.lower())

def flag_suspicious_url(url):
    """Check if a URL contains any suspicious words."""
    cleaned_url = clean_url(url)
    return any(keyword in cleaned_url for keyword in SUSPICIOUS_KEYWORDS)

def extract_features(df):

    
    """Extract relevant features from the URL."""
    df['cleaned_url'] = df['url'].apply(lambda x: re.sub(r'^https?:\/\/(www\.)?', '', x))
    df['url_length'] = df['url'].apply(len)*10
    df['num_dots'] = df['url'].apply(lambda x: x.count('.'))
    df['num_special_chars'] = df['cleaned_url'].apply(lambda x: len(re.findall(r'[@\-_%?]', x)))*5
    df['domain'] = df['cleaned_url'].apply(lambda x: urlparse(x).netloc)
    df['domain_length'] = df['domain'].apply(len)
    df['num_subdomains'] = df['domain'].apply(lambda x: x.count('.'))

    df.drop(columns=['cleaned_url', 'domain'], errors='ignore', inplace=True)
    return df
