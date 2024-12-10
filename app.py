import os
import json
from flask import Flask, render_template

app = Flask(__name__)

# Helper function to load recipes
def load_recipes():
    recipes = {"breakfast": [], "dinner": []}
    recipe_dir = "recipes"
    for file_name in os.listdir(recipe_dir):
        if file_name.endswith(".json"):
            with open(os.path.join(recipe_dir, file_name)) as f:
                recipe = json.load(f)
                category = recipe.get("category", "unknown").lower()
                if category in recipes:
                    recipes[category].append(recipe)
    return recipes

@app.route('/')
def home():
    recipes = load_recipes()
    return render_template('home.html', recipes=recipes)

@app.route('/recipe/<name>')
def recipe(name):
    recipe_dir = "recipes"
    recipe_file = os.path.join(recipe_dir, f"{name}.json")
    if os.path.exists(recipe_file):
        with open(recipe_file) as f:
            recipe = json.load(f)
        return render_template('recipe.html', recipe=recipe)
    return "Recipe not found", 404

if __name__ == '__main__':
    app.run(debug=True)
