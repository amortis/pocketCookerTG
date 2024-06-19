import requests
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import os
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat
from bs4 import BeautifulSoup
import parser
from recipe import Recipe

RQ_ID = os.getenv("GIGACHAT_RQ_ID")
CLIENT_ID = os.getenv("GIGACHAT_CLIENT_ID")
CLIENT_SERVER = os.getenv("GIGACHAT_CLIENT_SERVER")


def get_token() -> str:
    # Отключаем предупреждение
    urllib3.disable_warnings(InsecureRequestWarning)

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload = 'scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': RQ_ID,
        'Authorization': f'Basic {CLIENT_SERVER}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    return response.json()["access_token"]


def get_information_by_link(url: str) -> Recipe:
    recipe_info = parser.get_info_by_link(url)
    translated_title = translate_in_russian(recipe_info.title)
    translated_tutorial = translate_in_russian(recipe_info.tutorial)
    translated_ingredients = []
    for ingr in recipe_info.ingredients:
        translated_ingredients.append(translate_in_russian(ingr['name'] + " " + ingr['amount']))
    return Recipe(recipe_info.id, translated_title, translated_ingredients, translated_tutorial)


def translate(input: str) -> str:
    try:
        chat = GigaChat(credentials=CLIENT_SERVER, verify_ssl_certs=False)
        messages = [
            SystemMessage(
                content="Ты должен перевести заданную тебе строку на английский язык"
            ),
            HumanMessage(
                content=input
            )
        ]

        res = chat(messages)
        return res.content
    except:
        pass


def translate_in_russian(input: str) -> str:
    try:
        chat = GigaChat(credentials=CLIENT_SERVER, verify_ssl_certs=False)
        messages = [
            SystemMessage(
                content="Ты должен перевести заданную тебе строку на русский язык"
            ),
            HumanMessage(
                content=input
            )
        ]

        res = chat(messages)
        return res.content
    except:
        pass