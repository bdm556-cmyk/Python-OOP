from constants import DAYS, MEAL_TYPES
from recipe_service import find_recipe_by_id


# Sort ingredient names using insertion sort.
def sort_ingredient_names(ingredients):
    sorted_names = ingredients.copy()

    for index in range(1, len(sorted_names)):
        current_name = sorted_names[index]
        position = index - 1

        while position >= 0:
            if sorted_names[position].casefold() <= current_name.casefold():
                break

            sorted_names[position + 1] = sorted_names[position]
            position -= 1

        sorted_names[position + 1] = current_name

    return sorted_names


# Generate a unique shopping list.
def generate_shopping_list(weekly_plan, recipes):
    shopping_items = []
    used_items = set()

    for day in DAYS:
        for meal_type in MEAL_TYPES:
            recipe_id = weekly_plan[day][meal_type]
            recipe = find_recipe_by_id(recipes, recipe_id)

            if recipe is None:
                continue

            for ingredient in recipe["ingredients"]:
                ingredient_key = ingredient.casefold()

                if ingredient_key not in used_items:
                    shopping_items.append(ingredient)
                    used_items.add(ingredient_key)

    return sort_ingredient_names(shopping_items)
