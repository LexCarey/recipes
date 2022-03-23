from operator import is_
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask import flash, session
from flask_app.models import user

class Recipe():
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.half_hour = data["half_hour"]
        self.instructions = data["instructions"]
        self.date_made = data["date_made"]
        self.creator_id = data["creator_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create_recipe(cls, data):
        data = {
        "name": data['name'],
        "description": data['description'],
        "half_hour": data['half_hour'],
        "instructions" : data["instructions"],
        "date_made": data["date_made"],
        "creator_id": session["user_id"]
    }
        mysql = connectToMySQL("recipes_schema")
        query = "INSERT INTO recipes (name, description, half_hour, instructions, date_made, creator_id) VALUES (%(name)s, %(description)s, %(half_hour)s, %(instructions)s, %(date_made)s, %(creator_id)s);"
        return mysql.query_db(query, data)

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.creator_id = users.id;"
        results = connectToMySQL("recipes_schema").query_db(query)
        recipes = []
        if results:
            for row in results:
                temp_results = cls(row)
                creator_data = {
                    "id": row["id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "password": row["password"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"]
                }
                temp_results.creator = user.User(creator_data)
                recipes.append(temp_results)
        return recipes

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.creator_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL("recipes_schema").query_db(query, data)
        if results:
            temp_recipe = cls(results[0])
            temp_recipe.creator = user.User(results[0])
            return temp_recipe

    @classmethod
    def update_one_recipe(cls, data):
        mysql = connectToMySQL("recipes_schema")
        query ="UPDATE recipes SET name=%(name)s, description=%(description)s, half_hour=%(half_hour)s, instructions=%(instructions)s, date_made=%(date_made)s WHERE id = %(id)s;"
        mysql.query_db(query, data)

    @classmethod
    def delete_one_recipe(cls, data):
        mysql = connectToMySQL("recipes_schema")
        query ="DELETE FROM recipes WHERE id = %(id)s;"
        mysql.query_db(query, data)

    @classmethod
    def recipe_validator(cls, recipe):
        print(recipe["half_hour"])
        is_valid = True
        if len(recipe['name']) <= 2:
            flash("Name must be longer than 2 characters.")
            is_valid = False
        if len(recipe['description']) <= 2:
            flash("Description must be longer than 2 characters.")
            is_valid = False
        if len(recipe['instructions']) <= 2:
            flash("Instructions must be longer than 2 characters.")
            is_valid = False
        if recipe["half_hour"] != "Yes":
            if recipe["half_hour"] != "No":
                flash("Must choose if recipe takes under 30 minutes.")
                is_valid = False
        if len(recipe['date_made']) < 1:
            flash("Date can not be empty.")
            is_valid = False
        return is_valid