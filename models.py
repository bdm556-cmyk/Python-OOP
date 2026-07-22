from constants import DAYS, MEAL_TYPES


# Create one recipe dictionary.
def create_recipe(
    recipe_id,
    name,
    category,
    prep_time,
    servings,
    calories,
    ingredients,
):
    recipe = {
        "recipe_id": recipe_id,
        "name": name,
        "category": category,
        "prep_time": prep_time,
        "servings": servings,
        "calories": calories,
        "ingredients": ingredients,
    }
    return recipe


# Create an empty weekly plan.
def create_empty_weekly_plan():
    weekly_plan = {}

    for day in DAYS:
        weekly_plan[day] = {}

        for meal_type in MEAL_TYPES:
            weekly_plan[day][meal_type] = None

    return weekly_plan


# Create the main project data.
def create_project_data():
    project_data = {
        "recipes": [],
        "weekly_plan": create_empty_weekly_plan(),
    }
    return project_data
