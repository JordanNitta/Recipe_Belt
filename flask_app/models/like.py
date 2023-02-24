from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import recipe
from pprint import pprint

DATABASE = 'recipes_schema'

class Like:
    def __init__(self, data):
        self.recipe_id = data['recipe_id']
        self.user_id = data['user_id']
        self.created_at = data['created_at']

    @classmethod
    def get_all_recipe_with_likes(cls, data):
        query = """
        SELECT COUNT(*) TOTAL FROM likes 
        WHERE recipes.id = %(id)s;
        """
        # LEFT JOIN likes ON recipes.recipe_id = recipes.id
        # LEFT JOIN users ON likes.user_id = users.id
        # WHERE recipes.id = %(id)s;
        # results = connectToMySQL(DATABASE).query_db(query, data)
        # likes = cls(results[0])
        # user_likes = []
        # recipes_likes = []
        # all_like = {
        #     'users': [],
        #     'recipes': []
        # }
        # for dict in results:
        #     user_data = {
        #         'id': dict['users.id'],
        #         'first_name': dict['first_name'],
        #         'last_name': dict['last_name'],
        #         'created_at': dict['users.created_at']
        #     }
        #     recipe_data = {
        #         'id': dict['recipes.id'],
        #         'name': dict['recipes.name']
        #     }
        #     user_likes.append(user_data)
        #     recipes_likes.append(recipe_data)
        # all_like['users'] = user_likes
        # all_like['recipes'] = recipes_likes
        # print(all_like['users'])
        # print(all_like['recipes'])
        # return results

    # @classmethod
    # def likes_increase(cls, data):
        # query = """
        # SELECT COUNT(*) FROM likes 
        # WHERE users.id = %(id)s;
        # """
        # return connectToMySQL(DATABASE).query_db(query, data)