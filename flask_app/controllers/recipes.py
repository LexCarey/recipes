from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template,redirect,request,session,flash
from flask_app.models.recipe import Recipe


#TEMPLATE ROUTES
@app.route('/recipes')
def dashboad():
    if "user_id" in session:
        recipes = Recipe.get_all_recipes()
        return render_template("dashboard.html", recipes = recipes)
    return redirect('/')

@app.route('/recipes/new')
def new_recipe():
    if "user_id" in session:
        return render_template("new_recipe.html")
    return redirect('/')

@app.route('/recipes/<int:id>')
def view_recipe(id):
    if "user_id" in session:
        recipe = Recipe.get_one_recipe({ "id": id })
        return render_template("view_recipe.html", recipe = recipe)
    return redirect('/')

@app.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    if "user_id" in session:
        recipe = Recipe.get_one_recipe({ "id": id })
        return render_template("edit_recipe.html", recipe = recipe)
    return redirect('/')





#ACTION ROUTES
@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if "user_id" in session:
        if Recipe.recipe_validator(request.form):
            Recipe.create_recipe(request.form)
            return redirect('/recipes')
    return redirect('/recipes/new')

@app.route('/recipes/update', methods=['POST'])
def update_recipe():
    if "user_id" in session:
        if Recipe.recipe_validator(request.form):
            Recipe.update_one_recipe(request.form)
            recipe_id = request.form["id"]
            return redirect(f"/recipes/{recipe_id}")
    recipe_id = request.form["id"]
    return redirect(f'/recipes/{recipe_id}/edit')

@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    data = { "id": id }
    recipe = Recipe.get_one_recipe(data)
    if session['user_id'] == recipe["creator_id"]:
        Recipe.delete_one_recipe(data)
    return redirect('/recipes')