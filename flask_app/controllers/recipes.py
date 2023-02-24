from flask_app import app, render_template, request, redirect, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_app.models.like import Like


@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template("all_recipes.html", all_recipes=Recipe.get_all())

@app.route('/recipe/new')
def create_recipe():
    return render_template('create_recipes.html')

@app.route('/process/recipe', methods=['POST'])
def process_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')
    Recipe.save_recipe(request.form)
    print(request.form)
    return redirect('/recipes')

# Renders page with an edit option and gets 
@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/login')
    data = {
        'id': id
    }
    return render_template('edit_recipe.html', recipe = Recipe.get_one(data))

# Update recipe from form
@app.route('/update/recipe', methods=['POST'])
def process_update():
    Recipe.update(request.form)
    print(request.form)
    return redirect('/recipes')

@app.route('/recipe/<int:id>')
def display_one_recipes(id):
    data = {
        'id': id
    }
    return render_template('show.html', recipe = Recipe.get_one(data))

@app.route('/delete/<int:id>')
def delete_recipe(id):
    data = {
        'id': id
    }
    Recipe.delete(data)
    return redirect('/recipes')
