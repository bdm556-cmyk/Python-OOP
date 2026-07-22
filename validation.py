from constants import RECIPE_CATEGORIES


# Convert one value into a positive integer.
def parse_positive_integer(value, field_name):
    clean_value = value.strip()

    if clean_value == "":
        raise ValueError(field_name + " is required.")

    try:
        number = int(clean_value)
    except ValueError as error:
        raise ValueError(field_name + " must be a whole number.") from error

    if number <= 0:
        raise ValueError(field_name + " must be greater than zero.")

    return number


# Convert ingredient text into a clean list.
def parse_ingredient_input(ingredients_text):
    clean_text = ingredients_text.replace("\n", ",").replace(";", ",")
    ingredients = []
    used_names = set()

    for item in clean_text.split(","):
        ingredient = item.strip()
        ingredient_key = ingredient.casefold()

        if ingredient != "" and ingredient_key not in used_names:
            ingredients.append(ingredient)
            used_names.add(ingredient_key)

    if len(ingredients) == 0:
        raise ValueError("At least one ingredient is required.")

    return ingredients


# Check whether a recipe name already exists.
def recipe_name_exists(recipes, name, excluded_recipe_id=None):
    target_name = name.casefold()

    for recipe in recipes:
        if recipe["recipe_id"] == excluded_recipe_id:
            continue

        if recipe["name"].casefold() == target_name:
            return True

    return False


# Validate recipe form values.
def validate_recipe_input(
    recipes,
    name,
    category,
    prep_time,
    servings,
    calories,
    ingredients_text,
    excluded_recipe_id=None,
):
    clean_name = name.strip()
    clean_category = category.strip()

    if clean_name == "":
        raise ValueError("Recipe name is required.")

    if clean_category not in RECIPE_CATEGORIES:
        raise ValueError("Please select a valid category.")

    if recipe_name_exists(recipes, clean_name, excluded_recipe_id):
        raise ValueError("A recipe with this name already exists.")

    validated_data = {
        "name": clean_name,
        "category": clean_category,
        "prep_time": parse_positive_integer(prep_time, "Preparation time"),
        "servings": parse_positive_integer(servings, "Servings"),
        "calories": parse_positive_integer(calories, "Calories"),
        "ingredients": parse_ingredient_input(ingredients_text),
    }
    return validated_data
