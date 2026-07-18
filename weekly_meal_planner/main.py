from constants import APP_NAME, RECIPES_FILE
from file_manager import read_recipes
from models import create_project_data


# Display all loaded recipes.
def display_recipes(recipes):
    print("=" * 64)
    print(APP_NAME)
    print("=" * 64)

    for recipe in recipes:
        print(
            recipe["recipe_id"],
            "-",
            recipe["name"],
            "|",
            recipe["category"],
            "|",
            str(recipe["calories"]) + " kcal",
        )
        print("Ingredients:", ", ".join(recipe["ingredients"]))
        print("-" * 64)

    print("Recipes loaded:", len(recipes))


# Run the recipe loading version.
def main():
    project_data = create_project_data()
    project_data["recipes"] = read_recipes(RECIPES_FILE)
    display_recipes(project_data["recipes"])


if __name__ == "__main__":
    main()
