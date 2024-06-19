import requests
import os
from recipe import Recipe

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
NUMBER_OF_RECIPES = 5


def find_by_ingredients(ingredients: str):
    base_url = 'https://api.spoonacular.com/recipes/findByIngredients'

    # Параметры запроса
    params = {
        'apiKey': SPOONACULAR_API_KEY,
        'ingredients': ingredients,  # Список ингредиентов через запятую
        'number': NUMBER_OF_RECIPES  # Количество рецептов для возвращения
    }
    recipes_list = [] # Массив под id рецептов
    # Выполнение запроса
    response = requests.get(base_url, params=params)
    print(response.status_code)
    if response.status_code == 200:
        recipes = response.json()
        for recipe in recipes:
            recipes_list.append(Recipe(recipe['id'], recipe['title'], recipe['missedIngredients']))
    return recipes_list


def get_recipe_information(id: str) -> str:
    base_url = f"https://api.spoonacular.com/recipes/{id}/information"
    response = requests.get(base_url, params={'apiKey':SPOONACULAR_API_KEY})
    if response.status_code == 200:
        print(response.json()["spoonacularSourceUrl"])
        return response.json()["spoonacularSourceUrl"]


