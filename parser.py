import requests
from bs4 import BeautifulSoup
from recipe import Recipe


def get_info_by_link(url: str) -> Recipe:
    # Получаем HTML страницу
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Название
    title_element = soup.find('h1',{'itemprop': 'name'}).text
    title = title_element.strip()

    # Ингридиенты
    ingredients = []
    ingredient_containers = soup.find_all('div', class_='spoonacular-ingredient')

    for container in ingredient_containers:
        name_element = container.find('div', class_='spoonacular-name')
        name = name_element.text.strip() if name_element else None

        amount_element = container.find('div', class_='spoonacular-amount', style='display:block;')
        amount = amount_element.text.strip() if amount_element else None

        if name and amount:
            ingredients.append({
                'name': name,
                'amount': amount
            })

    # Туториал

    instructions_container = soup.find('div', class_='recipeInstructions')
    instructions = instructions_container.text
    return Recipe("1", title, ingredients, instructions)

