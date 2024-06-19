class Recipe:
    def __init__(self, id:str, title:str, missed_ingredients, tutorial=None):
        self.ingredients = missed_ingredients
        self.title = title
        self.id = id
        self.tutorial = tutorial

    def __str__(self):
        return f"{self.id}  {self.title} {str(len(self.ingredients))} {str(self.tutorial)}"

