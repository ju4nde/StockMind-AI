import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "data", "company_tickers.json")

def load_tickers():
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Warning: tickers.json not found!")
        return []

ALL_TICKERS = load_tickers()
