from flask_sqlalchemy import SQLAlchemy
#from app import db

db = SQLAlchemy()

# Modèle de données pour les utilisateurs
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(225), unique=True, nullable=False)
    password = db.Column(db.String(225), unique=True, nullable=False)
    recipes = db.relationship('Recipe', backref='user', lazy='dynamic')
    favorite_recipes = db.relationship('FavoriteRecipe', backref='user', lazy='dynamic')
    ingredient_user = db.relationship('IngredientUser', backref='user', lazy='dynamic')

# Modèle de données pour les ingrédients
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

# Modèle de données pour les recettes de repas
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))

# Modèle de données pour les menus
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))

# Modèle de données pour les recettes préférées des utilisateurs
class FavoriteRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

menu_recipe = db.Table('menu_recipe',
    db.Column('menu_id', db.Integer, db.ForeignKey('menu.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)