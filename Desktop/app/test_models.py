import unittest
from app import create_app, db
from models import User, Ingredient, Recipe, Menu, FavoriteRecipe  

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_user_model(self):
        # Test du modèle User
        user = User(username='test_user', email='test@example.com')
        db.session.add(user)
        db.session.commit()# Committre les modifications dans la base de données

        self.assertEqual(User.query.count(), 1)
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, 'test@example.com')
        db.session.commit()# Committre les modifications dans la base de données

    def test_ingredient_model(self):
        # Test du modèle Ingredient
        ingredient = Ingredient(name='Test Ingredient')
        db.session.add(ingredient)
        db.session.commit()# Committre les modifications dans la base de données

        self.assertEqual(Ingredient.query.count(), 1)
        self.assertEqual(ingredient.name, 'Test Ingredient')
        db.session.commit()# Committre les modifications dans la base de données

    def test_recipe_model(self):
        # Test du modèle Recipe
        recipe = Recipe(name='Test Recipe', description='Entrée')
        db.session.add(recipe)
        db.session.commit()# Committre les modifications dans la base de données

        self.assertEqual(Recipe.query.count(), 1)
        self.assertEqual(recipe.name, 'Test Recipe')
        self.assertEqual(recipe.type, 'Entrée')
        db.session.commit()# Committre les modifications dans la base de données

    def test_menu_model(self):
        # Test du modèle Menu
        menu = Menu(name='Test Menu')
        db.session.add(menu)
        db.session.commit()# Committre les modifications dans la base de données

        self.assertEqual(Menu.query.count(), 1)
        self.assertEqual(menu.name, 'Test Menu')
        db.session.commit()# Committre les modifications dans la base de données

if __name__ == '__main__':
    unittest.main()
