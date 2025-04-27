from flask import Flask, render_template, jsonify, session
import sqlite3
import pandas as pd
import json
import random
import os
from flask_session import Session

app = Flask(__name__)

# Configure Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_user_data():
    conn = sqlite3.connect('user.db')
    user_id = session.get('user_id')

    if not user_id:
        return {}

    df = pd.read_sql_query("SELECT category, amount FROM spending WHERE user_id = ?", conn, params=(user_id,))
    conn.close()

    return dict(zip(df['category'], df['amount'])) if not df.empty else {}


def load_recommendations(file_path, count):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return random.sample(data, min(count, len(data)))

def get_top_categories(spending_dict):
    sorted_categories = sorted(spending_dict.items(), key=lambda x: x[1], reverse=True)
    return [cat for cat, _ in sorted_categories[:2]]

def generate_recommendations(user_spending, folder_path='data'):
    recommendations = []

    new_path = os.path.join(folder_path, 'new.json')
    recommendations += load_recommendations(new_path, 2)

    top_categories = get_top_categories(user_spending)

    for category in top_categories:
        category_file = os.path.join(folder_path, f'{category.lower()}.json')
        if os.path.exists(category_file):
            recommendations += load_recommendations(category_file, 2)
        else:
            print(f"Warning: No data found for category: {category}")

    return recommendations
