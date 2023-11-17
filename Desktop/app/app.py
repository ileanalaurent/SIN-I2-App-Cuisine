# Importation des modules nécessaires
#import unittest
from flask import Flask, request, jsonify#, json, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
#from app import create_app, db
#from app import modele  # Il semble manquer l'importation du module "modele", assurez-vous que ce module existe
#from models import db

# Importation des modèles et routes
from models import User, Ingredient, Recipe, Menu, FavoriteRecipe # ,db
from routes import *  # Importion de toutes les routes Flask

def create_app(testing=False):
    app = Flask(__name__)  # Crée une instance de l'application Flask
    app.config['SECRET_KEY'] = 'Cle_Secret_id'  # Clé secrète pour la session et les cookies
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recettes_base_donnees.db'  # Configuration de la base de données
    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_recettes_base_donnees.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recettes_base_donnees.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Désactive la modification automatique SQLAlchemy
    db = SQLAlchemy(app)  # Crée une instance SQLAlchemy et la lie à Flask
    if 'SQLALCHEMY_DATABASE_URI' not in app.config:  # Vérifiez si l'instance n'est pas déjà configurée
        db.init_app(app)  # Initialisez l'extension SQLAlchemy ici
    return app, db

# Utilisez la fonction create_app pour créer l'application et la base de données
app, db = create_app()

''' Table de liaison pour les relations entre menus et recettes
menu_recipe = db.Table('menu_recipe',
    db.Column('menu_id', db.Integer, db.ForeignKey('menu.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)'''

# Configuration du répertoire des destinations pour les fichiers téléchargés
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Fonction pour vérifier l'extension d'un fichier
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Création de la base de données
with app.app_context():
    db.create_all()
    # Créez la table menu_recipe après que toutes les tables de base ont été créées
    '''menu_recipe =''' 
    db.Table('menu_recipe',
        db.Column('menu_id', db.Integer, db.ForeignKey('menu.id'), primary_key=True),
        db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    )
    #db.metadata.tables['menu_recipe'] = menu_recipe
    #db.session.add(menu_recipe)  # Ajouter cette ligne
    #db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)  # Exécute l'application en mode débogage
    #unittest.main()