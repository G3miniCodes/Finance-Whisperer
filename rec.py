from flask import Flask, render_template
import json
import os
import random

app = Flask(__name__)

@app.route('/', methods=['GET'])
def rec():
    user_recent_spending = {
        "entertainment": 300,
        "groceries": 500,
        "transport": 150,
        "subscriptions": 100
    }

    recommendations = generate_recommendations(user_recent_spending)
    return render_template('practice_rec.html', recommendations=recommendations)


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

if __name__ == '__main__':
    app.run(debug=True)
