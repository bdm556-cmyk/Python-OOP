from constants import DAYS, MEAL_TYPES
from models import create_empty_weekly_plan
from recipe_service import find_recipe_by_id


# Copy the current weekly plan.
def copy_weekly_plan(weekly_plan):
    plan_copy = create_empty_weekly_plan()

    for day in DAYS:
        for meal_type in MEAL_TYPES:
            plan_copy[day][meal_type] = weekly_plan[day][meal_type]

    return plan_copy


# Clear every meal slot.
def clear_weekly_plan():
    return create_empty_weekly_plan()


# Remove all references to one recipe.
def remove_recipe_from_plan(weekly_plan, recipe_id):
    removed_count = 0

    for day in DAYS:
        for meal_type in MEAL_TYPES:
            if weekly_plan[day][meal_type] == recipe_id:
                weekly_plan[day][meal_type] = None
                removed_count += 1

    return removed_count


# Calculate calories for each day.
def calculate_daily_calories(weekly_plan, recipes):
    daily_calories = {}

    for day in DAYS:
        total = 0

        for meal_type in MEAL_TYPES:
            recipe_id = weekly_plan[day][meal_type]
            recipe = find_recipe_by_id(recipes, recipe_id)

            if recipe is not None:
                total += recipe["calories"]

        daily_calories[day] = total

    return daily_calories


# Count all planned meals.
def count_planned_meals(weekly_plan):
    total = 0

    for day in DAYS:
        for meal_type in MEAL_TYPES:
            if weekly_plan[day][meal_type] is not None:
                total += 1

    return total
