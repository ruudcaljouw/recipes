from flask import Flask, render_template

app = Flask(__name__)

# Sample recipes data
recipes = {
    "breakfast": [
        {"name": "Pancakes", "url": "/recipe/pancakes", "ingredients": ["Flour", "Milk", "Eggs"], "steps": "Mix ingredients and cook on a hot pan."},
        {"name": "Omelette", "url": "/recipe/omelette", "ingredients": ["Eggs", "Cheese", "Ham"], "steps": "Whisk eggs, add fillings, and cook in a pan."}
    ],
    "dinner": [
        {"name": "Spaghett", "url": "/recipe/spaghetti", "ingredients": ["Pasta", "Tomato Sauce", "Meatballs"], "steps": "Cook pasta, heat sauce, combine with meatballs."},
        {"name": "Grilled Chicken", "url": "/recipe/grilled-chicken", "ingredients": ["Chicken", "Olive Oil", "Spices"], "steps": "Marinate chicken, grill until cooked through."}
    ]
}

@app.route('/')
def home():
    return render_template('home.html', recipes=recipes)

@app.route('/recipe/<name>')
def recipe(name):
    for category in recipes.values():
        for recipe in category:
            if recipe["name"].lower() == name.replace("-", " ").lower():
                return render_template('recipe.html', recipe=recipe)
    return "Recipe not found", 404

if __name__ == '__main__':
    app.run(debug=True)
