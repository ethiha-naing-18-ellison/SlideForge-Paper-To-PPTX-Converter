# -*- coding: utf-8 -*-
"""Download required NLTK data."""

import nltk

def download_nltk_data():
    """Download all required NLTK data."""
    print("Downloading NLTK data...")
    
    # Download required packages
    packages = [
        'punkt',
        'stopwords', 
        'wordnet',
        'averaged_perceptron_tagger',
        'punkt_tab'
    ]
    
    for package in packages:
        try:
            print(f"Downloading {package}...")
            nltk.download(package)
            print(f"✓ {package} downloaded successfully")
        except Exception as e:
            print(f"✗ Error downloading {package}: {e}")
    
    print("NLTK data download completed!")

if __name__ == "__main__":
    download_nltk_data()
