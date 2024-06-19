import spoonacular
import gigachat111
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!\n"
                         f"Пропиши свои продукты в произвольном формате (например, 2 картошки, кг курицы)")


@dp.message()
async def input_handler(message: Message) -> None:
    user_input = message.text
    recipes = get_recipes(user_input)
    message_text = ''
    for i in range(len(recipes)):
        recipe = recipes[i]
        await message.answer(f"{i+1}. <b>{html.bold(recipe.title)}\n<b>{html.italic('Ингридиенты')} :{' '.join(recipe.ingredients)}\n"
                         f"<b>{html.italic('Порядок приготовления')}:\n {recipe.tutorial}\n",
                             parse_mode=ParseMode.HTML)


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


def get_recipes(user_input: str):
    """
    Возвращает список рецептов по запросу
    :return:
    """
    translated_user_input = gigachat111.translate(user_input)
    recipe_list = spoonacular.find_by_ingredients(translated_user_input)
    recipes = []
    for recipe in recipe_list:
        recipe_url = spoonacular.get_recipe_information(recipe.id)
        translated_recipe = gigachat111.get_information_by_link(recipe_url)
        recipes.append(translated_recipe)
        # print("----------------------------------------------")
        # print("НАЗВАНИЕ " + translated_recipe.title)
        # print("Список ингридиентов", end=' ')
        # print([ingr for ingr in translated_recipe.ingredients])
        # print("Порядок приготовления\n" + translated_recipe.tutorial)
        # print("----------------------------------------------")
    return recipes


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
