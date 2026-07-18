from constants import APP_NAME, RECIPES_FILE
from file_manager import append_recipe, read_recipes
from models import create_project_data
from recipe_service import collect_new_recipe


# Display all recipes.
def display_recipes(recipes):
    print("\n" + "=" * 64)
    print("Recipe collection")
    print("=" * 64)

    for recipe in recipes:
        print(
            recipe["recipe_id"],
            "-",
            recipe["name"],
            "|",
            recipe["category"],
            "|",
            str(recipe["prep_time"]) + " minutes",
            "|",
            str(recipe["calories"]) + " kcal",
        )
        print("Ingredients:", ", ".join(recipe["ingredients"]))
        print("-" * 64)

    print("Total recipes:", len(recipes))


# Display the main menu.
def display_menu():
    print("\n" + APP_NAME)
    print("1. View recipes")
    print("2. Add recipe")
    print("3. Exit")


# Add and save one recipe.
def add_recipe(recipes):
    print("\nAdd a new recipe")
    new_recipe = collect_new_recipe(recipes)
    append_recipe(RECIPES_FILE, new_recipe)
    recipes.append(new_recipe)
    print(new_recipe["name"], "was saved with ID", new_recipe["recipe_id"])


# Run the console menu.
def main():
    project_data = create_project_data()
    project_data["recipes"] = read_recipes(RECIPES_FILE)

    choice = ""

    while choice != "3":
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_recipes(project_data["recipes"])
        elif choice == "2":
            add_recipe(project_data["recipes"])
        elif choice == "3":
            print("Program closed.")
        else:
            print("Please choose 1, 2 or 3.")


if __name__ == "__main__":
    main()
