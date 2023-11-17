import unittest
from flask import Flask, current_app, json
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db
from models import User, Ingredient, Recipe, Menu, FavoriteRecipe

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        # Configurer l'application pour le test
        self.app = create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Client pour effectuer des requêtes HTTP
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        # Nettoyer après les tests
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        # Test de la création d'un utilisateur
        response = self.client.post('/api/create_users', data=json.dumps({'username': 'test_user', 'email': 'test@example.com'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.query.count(), 1)
        db.session.commit()# Committre les modifications dans la base de données

    def test_create_ingredient(self):
        # Test de la création d'un ingrédient
        response = self.client.post('/api/ingredients', data=json.dumps({'name': 'test_ingredient'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ingredient.query.count(), 1)
        db.session.commit()# Committre les modifications dans la base de données

    def test_get_ingredients(self):
        # Test de la récupération de la liste des ingrédients
        response = self.client.get('/api/ingredients')
        self.assertEqual(response.status_code, 200)
        # Possibilités d'ajouter des assertions supplémentaires en fonction de la logique d'application
        db.session.commit()# Committre les modifications dans la base de données

    def test_create_recipe(self):
        # Test de la création d'une recette
        ingredient = Ingredient(name='Test Ingredient')
        db.session.add(ingredient)
        db.session.commit()# Committre les modifications dans la base de données

        data = {
            'name': 'Test Recipe',
            'type': 'Entrée',
            'ingredients': [ingredient.id]
        }

        response = self.client.post('/api/recipes', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Recipe.query.count(), 1)
        db.session.commit()# Committre les modifications dans la base de données

    def test_get_recipe(self):
        # Test de la récupération d'une recette spécifique
        ingredient = Ingredient(name='Test Ingredient')
        db.session.add(ingredient)
        db.session.commit()# Committre les modifications dans la base de données

        recipe = Recipe(name='Test Recipe', type='Entrée')
        recipe.ingredients.append(ingredient)
        db.session.add(recipe)
        db.session.commit()# Committre les modifications dans la base de données

        response = self.client.get(f'/api/recipes/{recipe.id}')
        self.assertEqual(response.status_code, 200)
        # Possibilités d'ajouter des assertions supplémentaires en fonction de la logique d'application
        db.session.commit()# Committre les modifications dans la base de données

    def test_create_menu(self):
        # Test de la création d'un menu
        recipe = Recipe(name='Test Recipe', type='Entrée')
        db.session.add(recipe)
        db.session.commit()# Committre les modifications dans la base de données

        data = {
            'name': 'Test Menu',
            'entries': [recipe.id]
        }

        response = self.client.post('/api/menus', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Menu.query.count(), 1)
        db.session.commit()# Committre les modifications dans la base de données

    def test_get_menus(self):
        # Test de la récupération de la liste des menus
        response = self.client.get('/api/menus')
        self.assertEqual(response.status_code, 200)
        # Possibilités d'ajouter des assertions supplémentaires en fonction de la logique d'application
        db.session.commit()# Committre les modifications dans la base de données

    def test_mark_favorite(self):
        # Test de la marque comme favori
        user = User(username='test_user', email='test@example.com')
        db.session.add(user)
        db.session.commit()# Committre les modifications dans la base de données

        recipe = Recipe(name='Test Recipe', type='Entrée')
        db.session.add(recipe)
        db.session.commit()# Committre les modifications dans la base de données

        data = {'user_id': user.id, 'recipe_id': recipe.id}

        response = self.client.post('/api/mark_favorite', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # Possibilités d'ajouter des assertions supplémentaires en fonction de la logique d'application
        db.session.commit()# Committre les modifications dans la base de données

    def test_get_favorite_recipes(self):
        # Test de la récupération des recettes favorites d'un utilisateur
        user = User(username='test_user', email='test@example.com')
        db.session.add(user)
        db.session.commit()# Committre les modifications dans la base de données

        recipe = Recipe(name='Test Recipe', type='Entrée')
        db.session.add(recipe)
        db.session.commit()# Committre les modifications dans la base de données

        user.favorite_recipes.append(recipe)
        db.session.commit()# Committre les modifications dans la base de données

        response = self.client.get(f'/api/favorite_recipes/{user.id}')
        self.assertEqual(response.status_code, 200)
        # Possibilités d'ajouter des assertions supplémentaires en fonction de la logique d'application
        db.session.commit()# Committre les modifications dans la base de données

if __name__ == '__main__':
    unittest.main()

