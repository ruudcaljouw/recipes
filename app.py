import os
import json
from flask import Flask, render_template

app = Flask(__name__)

# Absolute base directory for proper path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Function to load recipes from all categories
def load_recipes():
    recipes = {"breakfast": [], "dinner": [], "salads": [], "sides": []}  # Include categories
    recipe_dir = os.path.join(BASE_DIR, "recipes")
    for category in recipes.keys():
        category_path = os.path.join(recipe_dir, category)
        if os.path.exists(category_path):
            for file_name in os.listdir(category_path):
                if file_name.endswith(".json"):
                    file_path = os.path.join(category_path, file_name)
                    with open(file_path) as f:
                        recipe = json.load(f)
                        # Add the filename (without extension) as an identifier
                        recipe["id"] = os.path.splitext(file_name)[0]
                        recipe["category"] = category  # Add category for easier navigation
                        recipes[category].append(recipe)
    return recipes

# Route for the homepage
@app.route('/')
def home():
    """
    The home route ('/') serves the homepage of the app.
    It dynamically loads and displays all available recipes categorized as breakfast, dinner, salads, or sides.
    """
    recipes = load_recipes()
    return render_template('home.html', recipes=recipes)

# Route for individual recipe pages
@app.route('/recipe/<category>/<id>')
def recipe(category, id):
    """
    The dynamic route serves individual recipe pages based on the URL.
    It uses 'category' and 'id' (filename) to find and load the appropriate recipe file.
    """
    recipe_file = os.path.join(BASE_DIR, "recipes", category, f"{id}.json")
    if os.path.exists(recipe_file):
        with open(recipe_file) as f:
            recipe = json.load(f)
            recipe["id"] = id  # Ensure the recipe has its ID for template rendering
        return render_template('recipe.html', recipe=recipe)
    return "Recipe not found", 404

if __name__ == '__main__':
    app.run(debug=True)
