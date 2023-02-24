from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from pprint import pprint
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

DATABASE = 'recipes_schema'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_user(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = """
        SELECT * FROM users 
        WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return User(results[0])
        return False

    @staticmethod
    def validate_user_info(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("Required field", 'first_name')
            is_valid = False
            flash("Required field")
        if not EMAIL_REGEX.match(data['email']):
            flash("Required field","email")
            is_valid = False
        if data['password'] != data['confirm-password']:
            is_valid = False
            flash("Password doesn't match", 'confirm-password') #setting a catgory "password" and will flash password
        if len(data['password']) < 8:
            is_valid = False
            flash("Create a secure password. Your password must be at least 8 or more characters.", 'password') #setting a catgory "password" and will flash password to short\
        if is_valid:
            existing_user = User.get_by_email({'email': data['email']})
            if existing_user:
                flash('Email Taken', 'existing_email')
                is_valid = False
        return is_valid