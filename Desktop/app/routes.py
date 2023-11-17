from flask import jsonify, request
from app import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Ingredient, Recipe, Menu, FavoriteRecipe

# Route API pour créer un ingrédient
@app.route('/api/create_ingredient', methods=['POST'])
def create_ingredient():
    data = request.get_json()
    
    if 'name' in data:
        name = data['name']

        new_ingredient = Ingredient(name=name)
        #new_ingredient = Ingredient(name=data['name'])
        db.session.add(new_ingredient)
        #db.session.commit()

        try:
            db.session.commit()
            return jsonify({'message': 'Ingrédient créé avec succès'}), 201
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'message': 'Une erreur s\'est produite lors de la création de l\'ingrédient'}), 500

# Route API pour lister les ingrédients
@app.route('/api/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    output = [{'id': ingredient.id, 'name': ingredient.name} for ingredient in ingredients]
    return jsonify({'ingredients': output})

# Route API pour créer un utilisateur
@app.route('/api/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if 'username' in data and 'password' in data:
        username = data['username']
        password = data['password']
        
        hashed_password = generate_password_hash(password, method='sha256')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'Ce nom d\'utilisateur est déjà pris'}), 400

        new_user = User(username=username, password=hashed_password)
        #new_user = User(username=data['username'], password=data['hashed_password'])
        db.session.add(new_user)

        try:
            db.session.commit()
            return jsonify({'message': 'Utilisateur créé avec succès'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Une erreur s\'est produite lors de la création de l\'utilisateur'}), 500

# Route API pour lister les recettes possibles
@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    output = [{'id': recipe.id, 'name': recipe.name, 'description': recipe.description} for recipe in recipes]
    return jsonify({'recipes': output})

# Route API pour créer une recette de repas
@app.route('/api/create_recipe', methods=['POST'])
def create_recipe():
    data = request.get_json()
    
    if 'name' in data and 'description' in data:
        name = data['name']
        description = data['description']

        new_recipe = Recipe(name=name, description=description)
        db.session.add(new_recipe)

        try:
            db.session.commit()
            return jsonify({'message': 'Recette créée avec succès'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Une erreur s\'est produite lors de la création de la recette'}), 500

# Route API pour créer un menu
@app.route('/api/create_menu', methods=['POST'])
def create_menu():
    data = request.get_json()
    
    if 'name' in data and 'description' in data and 'recipe_ids' in data:
        name = data['name']
        description = data['description']
        recipe_ids = data['recipe_ids']

        new_menu = Menu(name=name, description=description)
        db.session.add(new_menu)

        try:
            db.session.commit()

            for recipe_id in recipe_ids:
                recipe = Recipe.query.get(recipe_id)
                if recipe:
                    new_menu.recipes.append(recipe)

            db.session.commit()
            return jsonify({'message': 'Menu créé avec succès'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Une erreur s\'est produite lors de la création du menu'}), 500

# Route API pour lister les menus
@app.route('/api/menus', methods=['GET'])
def get_menus():
    menus = Menu.query.all()
    output = []
    for menu in menus:
        recipes = [{'id': recipe.id, 'name': recipe.name} for recipe in menu.recipes]
        output.append({'id': menu.id, 'name': menu.name, 'description': menu.description, 'recipes': recipes})
    return jsonify({'menus': output})

# Route API pour marquer une recette comme préférée par un utilisateur
@app.route('/api/mark_favorite', methods=['POST'])
def mark_favorite():
    data = request.get_json()
    user_id = data.get('user_id')
    recipe_id = data.get('recipe_id')

    user = User.query.get(user_id)
    recipe = Recipe.query.get(recipe_id)

    if user and recipe:
        user.favorite_recipes.append(recipe)
        db.session.commit()
        return jsonify({'message': 'Recette marquée comme préférée avec succès'}), 200
    else:
        return jsonify({'message': 'Utilisateur ou recette introuvable'}), 404

# Route API pour lister les recettes préférées d'un utilisateur
@app.route('/api/favorite_recipes/<int:user_id>', methods=['GET'])
def get_favorite_recipes(user_id):
    user = User.query.get(user_id)

    if user:
        favorite_recipes = [{'id': recipe.id, 'name': recipe.name} for recipe in user.favorite_recipes]
        return jsonify({'favorite_recipes': favorite_recipes})
    else:
        return jsonify({'message': 'Utilisateur introuvable'}), 404
    