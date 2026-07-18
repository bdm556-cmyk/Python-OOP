from constants import RECIPE_CATEGORIES
from models import create_recipe


# Create the next recipe ID.
def generate_recipe_id(recipes):
    highest_number = 0

    for recipe in recipes:
        recipe_number = int(recipe["recipe_id"][1:])

        if recipe_number > highest_number:
            highest_number = recipe_number

    return "R" + str(highest_number + 1).zfill(3)


# Ask for ingredient names.
def collect_ingredients():
    ingredients = []
    ingredient_count = int(input("Number of ingredients: "))

    for ingredient_number in range(ingredient_count):
        ingredient = input(
            "Ingredient " + str(ingredient_number + 1) + ": "
        ).strip()
        ingredients.append(ingredient)

    return ingredients


# Ask for a new recipe.
def collect_new_recipe(recipes):
    recipe_id = generate_recipe_id(recipes)
    name = input("Recipe name: ").strip()

    print("Categories:", ", ".join(RECIPE_CATEGORIES))
    category = input("Category: ").strip()

    prep_time = int(input("Preparation time in minutes: "))
    servings = int(input("Number of servings: "))
    calories = int(input("Calories per serving: "))
    ingredients = collect_ingredients()

    recipe = create_recipe(
        recipe_id,
        name,
        category,
        prep_time,
        servings,
        calories,
        ingredients,
    )
    return recipe
