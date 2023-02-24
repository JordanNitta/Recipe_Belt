from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models import user
from pprint import pprint

DATABASE = 'recipes_schema'

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM recipes 
        LEFT JOIN users 
        ON users.id = recipes.user_id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        all_recipes = []
        for recipe in results:
            # recipe instance
            recipe_instance = cls(recipe)
            #extracting data
            user_data = {
                **recipe,
                'id': recipe['users.id'],
                'created_at': recipe['users.created_at'],
                'updated_at': recipe['users.updated_at']
            }
            # creating user instance
            user_instance = user.User(user_data)
            # attaching recipe with user 
            recipe_instance.user = user_instance
            # adding them to a list not in get_one 
            all_recipes.append(recipe_instance)
            # Return recipe all_recipes list which contains all the recipe instance with the user instance attached
        return all_recipes

    @classmethod
    def get_one(cls, data):
        query = """
        SELECT * FROM recipes 
        LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        #1. Create recipe instance
        recipe = cls(results[0])
        #2. create user data dict extract user data
        user_data = {
            **results[0],
            'id': results[0]['users.id'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']
        }
        #3. create user instance
        # user_instance = user.User(user_data)
        #4. attach to recipe instance the user instance 
        # recipe_instance.user = user_instance
        recipe.user = user.User(user_data)
        #5. return recipe instance
        return recipe

    @classmethod
    def save_recipe(cls, data):
        query = """ 
        INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id) 
        VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM recipes
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """
        UPDATE recipes
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, 
        date_made = %(date_made)s, under_30 = %(under_30)s, WHERE recipes.id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            flash('Name needs to be longer then three characters', 'error_name')
            is_valid = False
        if len(data['description']) < 10:
            flash('Description needs to be longer then three characters', 'error_description')
            is_valid = False
        if len(data['instructions']) < 3:
            flash('Instructions need to be longer then three characters', 'error_instructions')
            is_valid = False
        return is_valid
        