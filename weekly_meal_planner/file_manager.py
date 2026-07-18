import csv

from models import create_recipe


# Split ingredient text into a list.
def parse_ingredients(ingredients_text):
    ingredients = []

    for ingredient in ingredients_text.split(";"):
        clean_ingredient = ingredient.strip()

        if clean_ingredient != "":
            ingredients.append(clean_ingredient)

    return ingredients


# Join ingredient names for CSV storage.
def format_ingredients(ingredients):
    return ";".join(ingredients)


# Read all recipes from the CSV file.
def read_recipes(filename):
    recipes = []

    with open(filename, "r", newline="", encoding="utf-8") as recipe_file:
        reader = csv.DictReader(recipe_file)

        for row in reader:
            recipe = create_recipe(
                row["recipe_id"],
                row["name"],
                row["category"],
                int(row["prep_time"]),
                int(row["servings"]),
                int(row["calories"]),
                parse_ingredients(row["ingredients"]),
            )
            recipes.append(recipe)

    return recipes


# Add one recipe to the CSV file.
def append_recipe(filename, recipe):
    fieldnames = [
        "recipe_id",
        "name",
        "category",
        "prep_time",
        "servings",
        "calories",
        "ingredients",
    ]

    with open(filename, "a", newline="", encoding="utf-8") as recipe_file:
        writer = csv.DictWriter(recipe_file, fieldnames=fieldnames)
        writer.writerow(
            {
                "recipe_id": recipe["recipe_id"],
                "name": recipe["name"],
                "category": recipe["category"],
                "prep_time": recipe["prep_time"],
                "servings": recipe["servings"],
                "calories": recipe["calories"],
                "ingredients": format_ingredients(recipe["ingredients"]),
            }
        )
