from models import create_recipe


# Create the next available recipe ID.
def generate_recipe_id(recipes):
    highest_number = 0

    for recipe in recipes:
        recipe_id = recipe["recipe_id"]

        if len(recipe_id) > 1 and recipe_id[0].upper() == "R":
            number_text = recipe_id[1:]

            if number_text.isdigit():
                highest_number = max(highest_number, int(number_text))

    return "R" + str(highest_number + 1).zfill(3)


# Find one recipe by its ID.
def find_recipe_by_id(recipes, recipe_id):
    for recipe in recipes:
        if recipe["recipe_id"] == recipe_id:
            return recipe

    return None


# Add one validated recipe.
def add_recipe(recipes, recipe_data):
    recipe = create_recipe(
        generate_recipe_id(recipes),
        recipe_data["name"],
        recipe_data["category"],
        recipe_data["prep_time"],
        recipe_data["servings"],
        recipe_data["calories"],
        recipe_data["ingredients"],
    )
    recipes.append(recipe)
    return recipe


# Update one recipe by its ID.
def update_recipe(recipes, recipe_id, recipe_data):
    recipe = find_recipe_by_id(recipes, recipe_id)

    if recipe is None:
        return False

    recipe["name"] = recipe_data["name"]
    recipe["category"] = recipe_data["category"]
    recipe["prep_time"] = recipe_data["prep_time"]
    recipe["servings"] = recipe_data["servings"]
    recipe["calories"] = recipe_data["calories"]
    recipe["ingredients"] = recipe_data["ingredients"]
    return True


# Delete one recipe by its ID.
def delete_recipe(recipes, recipe_id):
    for index in range(len(recipes)):
        if recipes[index]["recipe_id"] == recipe_id:
            del recipes[index]
            return True

    return False


# Search recipes one item at a time.
def linear_search(recipes, query, search_mode):
    results = []
    target = query.strip().casefold()

    if target == "":
        return results

    for recipe in recipes:
        name_matches = target in recipe["name"].casefold()
        category_matches = target in recipe["category"].casefold()
        ingredient_matches = False

        for ingredient in recipe["ingredients"]:
            if target in ingredient.casefold():
                ingredient_matches = True
                break

        if search_mode == "Name" and name_matches:
            results.append(recipe)
        elif search_mode == "Category" and category_matches:
            results.append(recipe)
        elif search_mode == "Ingredient" and ingredient_matches:
            results.append(recipe)
        elif search_mode == "All fields":
            if name_matches or category_matches or ingredient_matches:
                results.append(recipe)

    return results


# Get the comparison value for sorting.
def get_sort_value(recipe, sort_field):
    if sort_field == "name":
        return recipe["name"].casefold()

    return recipe[sort_field]


# Sort recipes using insertion sort.
def insertion_sort(recipes, sort_field):
    sorted_recipes = recipes.copy()

    for index in range(1, len(sorted_recipes)):
        current_recipe = sorted_recipes[index]
        current_value = get_sort_value(current_recipe, sort_field)
        position = index - 1

        while position >= 0:
            previous_value = get_sort_value(
                sorted_recipes[position],
                sort_field,
            )

            if previous_value <= current_value:
                break

            sorted_recipes[position + 1] = sorted_recipes[position]
            position -= 1

        sorted_recipes[position + 1] = current_recipe

    return sorted_recipes


# Find an exact recipe name using recursion.
def recursive_binary_search(recipes, target_name, low=0, high=None):
    if high is None:
        high = len(recipes) - 1

    if low > high:
        return None

    middle = (low + high) // 2
    middle_name = recipes[middle]["name"].casefold()
    target = target_name.strip().casefold()

    if middle_name == target:
        return recipes[middle]

    if target < middle_name:
        return recursive_binary_search(recipes, target_name, low, middle - 1)

    return recursive_binary_search(recipes, target_name, middle + 1, high)
