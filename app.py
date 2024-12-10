import os
import json
from flask import Flask, render_template

app = Flask(__name__)

# Helper function to load recipes from separate folders
def load_recipes():
    recipes = {"breakfast": [], "dinner": []}
    base_path = "recipes"
    for category in recipes.keys():
        category_path = os.path.join(base_path, category)
        if os.path.exists(category_path):
            for file_name in os.listdir(category_path):
                if file_name.endswith(".json"):
                    with open(os.path.join(category_path, file_name)) as f:
                        recipe = json.load(f)
                        recipes[category].append(recipe)
    return recipes

@app.route('/')
def home():
    recipes = load_recipes()
    return render_template('home.html', recipes=recipes)

@app.route('/recipe/<category>/<name>')
def recipe(category, name):
    recipe_file = os.path.join("recipes", category, f"{name}.json")
    if os.path.exists(recipe_file):
        with open(recipe_file) as f:
            recipe = json.load(f)
        return render_template('recipe.html', recipe=recipe)
    return "Recipe not found", 404

if __name__ == '__main__':
    app.run(debug=True)
