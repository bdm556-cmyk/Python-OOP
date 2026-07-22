from pathlib import Path

# Store shared project values.
APP_NAME = "Weekly Meal Planner & Smart Shopping List"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RECIPES_FILE = DATA_DIR / "recipes.csv"
MEAL_PLAN_FILE = DATA_DIR / "meal_plan.csv"
SHOPPING_LIST_FILE = DATA_DIR / "shopping_list.txt"

DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

MEAL_TYPES = [
    "Breakfast",
    "Lunch",
    "Dinner",
]

RECIPE_CATEGORIES = [
    "Breakfast",
    "Lunch",
    "Dinner",
    "Snack",
]

RECIPE_FIELDS = [
    "recipe_id",
    "name",
    "category",
    "prep_time",
    "servings",
    "calories",
    "ingredients",
]

MEAL_PLAN_FIELDS = [
    "day",
    "meal_type",
    "recipe_id",
]
