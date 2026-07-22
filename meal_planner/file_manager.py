import csv
from pathlib import Path

from constants import (
    DATA_DIR,
    DAYS,
    MEAL_PLAN_FIELDS,
    MEAL_PLAN_FILE,
    MEAL_TYPES,
    RECIPE_FIELDS,
    RECIPES_FILE,
)
from models import create_empty_weekly_plan, create_recipe


# Create the data folder when it is missing.
def ensure_data_directory():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


# Create an empty recipe file when it is missing.
def ensure_recipe_file(filename=RECIPES_FILE):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as recipe_file:
            writer = csv.DictWriter(recipe_file, fieldnames=RECIPE_FIELDS)
            writer.writeheader()
        return True

    return False


# Create an empty meal plan file when it is missing.
def ensure_meal_plan_file(filename=MEAL_PLAN_FILE):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        save_meal_plan(create_empty_weekly_plan(), path)
        return True

    return False


# Prepare the project data files.
def ensure_data_files():
    ensure_data_directory()
    created_recipe_file = ensure_recipe_file()
    created_plan_file = ensure_meal_plan_file()
    messages = []

    if created_recipe_file:
        messages.append("The missing recipe file was recreated.")

    if created_plan_file:
        messages.append("The missing meal plan file was recreated.")

    return messages


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


# Read recipes and skip invalid rows.
def load_recipes(filename=RECIPES_FILE):
    path = Path(filename)
    warnings = []
    recipes = []

    if ensure_recipe_file(path):
        warnings.append("The missing recipe file was recreated.")

    try:
        with path.open("r", newline="", encoding="utf-8") as recipe_file:
            reader = csv.DictReader(recipe_file)
            headings = reader.fieldnames or []

            if not set(RECIPE_FIELDS).issubset(set(headings)):
                warnings.append("The recipe file headings are invalid.")
                return recipes, warnings

            for row_number, row in enumerate(reader, start=2):
                try:
                    recipe_id = row["recipe_id"].strip()
                    name = row["name"].strip()
                    category = row["category"].strip()
                    prep_time = int(row["prep_time"])
                    servings = int(row["servings"])
                    calories = int(row["calories"])
                    ingredients = parse_ingredients(row["ingredients"])

                    if recipe_id == "" or name == "" or category == "":
                        raise ValueError

                    if prep_time <= 0 or servings <= 0 or calories <= 0:
                        raise ValueError

                    if len(ingredients) == 0:
                        raise ValueError

                    recipe = create_recipe(
                        recipe_id,
                        name,
                        category,
                        prep_time,
                        servings,
                        calories,
                        ingredients,
                    )
                    recipes.append(recipe)
                except (KeyError, TypeError, ValueError):
                    warnings.append(
                        "Skipped invalid recipe row " + str(row_number) + "."
                    )
    except (OSError, csv.Error) as error:
        warnings.append("The recipe file could not be read: " + str(error))

    return recipes, warnings


# Save recipes using a temporary file.
def save_recipes(recipes, filename=RECIPES_FILE):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")

    try:
        with temporary_path.open("w", newline="", encoding="utf-8") as recipe_file:
            writer = csv.DictWriter(recipe_file, fieldnames=RECIPE_FIELDS)
            writer.writeheader()

            for recipe in recipes:
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

        temporary_path.replace(path)
    except OSError:
        if temporary_path.exists():
            temporary_path.unlink()
        raise


# Read the weekly meal plan.
def load_meal_plan(recipes, filename=MEAL_PLAN_FILE):
    path = Path(filename)
    warnings = []
    weekly_plan = create_empty_weekly_plan()
    valid_recipe_ids = {recipe["recipe_id"] for recipe in recipes}

    if ensure_meal_plan_file(path):
        warnings.append("The missing meal plan file was recreated.")

    try:
        with path.open("r", newline="", encoding="utf-8") as meal_plan_file:
            reader = csv.DictReader(meal_plan_file)
            headings = reader.fieldnames or []

            if not set(MEAL_PLAN_FIELDS).issubset(set(headings)):
                warnings.append("The meal plan file headings are invalid.")
                return weekly_plan, warnings

            for row_number, row in enumerate(reader, start=2):
                day = row.get("day", "").strip()
                meal_type = row.get("meal_type", "").strip()
                recipe_id = row.get("recipe_id", "").strip()

                if day not in DAYS or meal_type not in MEAL_TYPES:
                    warnings.append(
                        "Skipped invalid meal plan row " + str(row_number) + "."
                    )
                    continue

                if recipe_id == "":
                    weekly_plan[day][meal_type] = None
                elif recipe_id in valid_recipe_ids:
                    weekly_plan[day][meal_type] = recipe_id
                else:
                    warnings.append(
                        "Cleared an unknown recipe in meal plan row "
                        + str(row_number)
                        + "."
                    )
    except (OSError, csv.Error) as error:
        warnings.append("The meal plan file could not be read: " + str(error))

    return weekly_plan, warnings


# Save all weekly meal slots.
def save_meal_plan(weekly_plan, filename=MEAL_PLAN_FILE):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")

    try:
        with temporary_path.open("w", newline="", encoding="utf-8") as meal_plan_file:
            writer = csv.DictWriter(meal_plan_file, fieldnames=MEAL_PLAN_FIELDS)
            writer.writeheader()

            for day in DAYS:
                for meal_type in MEAL_TYPES:
                    recipe_id = weekly_plan[day][meal_type]
                    writer.writerow(
                        {
                            "day": day,
                            "meal_type": meal_type,
                            "recipe_id": recipe_id or "",
                        }
                    )

        temporary_path.replace(path)
    except OSError:
        if temporary_path.exists():
            temporary_path.unlink()
        raise


# Save the generated shopping list.
def save_shopping_list(items, filename):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as shopping_file:
        shopping_file.write("Shopping List\n")
        shopping_file.write("=" * 30 + "\n")

        for item in items:
            shopping_file.write("- " + item + "\n")
