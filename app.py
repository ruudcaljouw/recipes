import os
import json
from flask import Flask, render_template
from flask import request

app = Flask(__name__)

# Base directory for file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Function to load recipes
def load_recipes():
    recipes = {"breakfast": [], "lunch": [], "dinner": [], "salads": [], "sides": [], "divers": []}
    recipe_dir = os.path.join(BASE_DIR, "recipes")
    
    for category in recipes.keys():
        category_path = os.path.join(recipe_dir, category)
        if not os.path.exists(category_path):
            continue
        
        for file_name in os.listdir(category_path):
            if not file_name.endswith(".json"):
                continue
            
            file_path = os.path.join(category_path, file_name)
            try:
                with open(file_path) as f:
                    recipe = json.load(f)
                    recipe["id"] = os.path.splitext(file_name)[0]
                    recipe["category"] = category
                    recipes[category].append(recipe)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading {file_path}: {e}")
    
    return recipes

# Homepage route
@app.route('/')
def home():
    """
    Renders the homepage with all recipe categories.
    """
    recipes = load_recipes()
    return render_template('home.html', recipes=recipes)

# Individual recipe route
@app.route('/recipe/<category>/<id>')
def recipe(category, id):
    """
    Renders an individual recipe page based on the category and recipe ID.
    """
    recipe_file = os.path.join(BASE_DIR, "recipes", category, f"{id}.json")
    if os.path.exists(recipe_file):
        with open(recipe_file) as f:
            recipe = json.load(f)
        return render_template('recipe.html', recipe=recipe), 200, {"Content-Type": "text/html; charset=utf-8"}
    return "Recipe not found", 404


@app.route('/update_hook', methods=['POST'])
def update_code():
    """
    Webhook endpoint for GitHub. Pulls the latest code when triggered.
    """
    # Verify the request (optional but recommended)
    secret = "testing"  # Use the same secret you set in the webhook
    if not request.headers.get('X-Hub-Signature-256'):
        return "Unauthorized", 403

    # Run the update script
    os.system("/home/roadrunner38/update_recipes_app.sh")
    return "Code updated", 200



if __name__ == '__main__':
    app.run(debug=True)
