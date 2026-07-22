import copy
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from constants import (
    APP_NAME,
    DAYS,
    MEAL_TYPES,
    RECIPE_CATEGORIES,
    SHOPPING_LIST_FILE,
)
from file_manager import (
    ensure_data_files,
    load_meal_plan,
    load_recipes,
    save_meal_plan,
    save_recipes,
    save_shopping_list,
)
from meal_plan_service import (
    calculate_daily_calories,
    clear_weekly_plan,
    copy_weekly_plan,
    count_planned_meals,
    remove_recipe_from_plan,
)
from recipe_service import (
    add_recipe,
    delete_recipe,
    find_recipe_by_id,
    insertion_sort,
    linear_search,
    recursive_binary_search,
    update_recipe,
)
from shopping_list_service import generate_shopping_list
from validation import validate_recipe_input


class MealPlannerApp:
    # Build the main application window.
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.geometry("1120x720")
        self.root.minsize(920, 620)

        startup_messages = ensure_data_files()
        self.recipes, recipe_warnings = load_recipes()
        self.weekly_plan, plan_warnings = load_meal_plan(self.recipes)
        self.shopping_items = []
        self.display_to_id = {"": None}
        self.id_to_display = {None: ""}
        self.meal_vars = {}
        self.calorie_labels = {}

        self.create_interface()
        self.refresh_recipe_table(self.recipes)
        self.refresh_recipe_choices()
        self.update_plan_summary()

        all_messages = startup_messages + recipe_warnings + plan_warnings

        if len(all_messages) > 0:
            self.root.after(150, lambda: self.show_startup_warnings(all_messages))

    # Create all application tabs.
    def create_interface(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self.recipe_tab = ttk.Frame(notebook, padding=10)
        self.planner_tab = ttk.Frame(notebook, padding=10)
        self.shopping_tab = ttk.Frame(notebook, padding=10)

        notebook.add(self.recipe_tab, text="Recipe Library")
        notebook.add(self.planner_tab, text="Weekly Planner")
        notebook.add(self.shopping_tab, text="Shopping List")

        self.build_recipe_tab()
        self.build_planner_tab()
        self.build_shopping_tab()

    # Build the recipe library controls.
    def build_recipe_tab(self):
        self.recipe_tab.columnconfigure(0, weight=1)
        self.recipe_tab.rowconfigure(2, weight=1)

        search_frame = ttk.LabelFrame(
            self.recipe_tab,
            text="Search",
            padding=8,
        )
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        search_frame.columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="Search text:").grid(
            row=0,
            column=0,
            padx=(0, 6),
            pady=4,
            sticky="w",
        )

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, padx=4, pady=4, sticky="ew")
        search_entry.bind("<Return>", lambda event: self.search_recipes())

        self.search_mode_var = tk.StringVar(value="All fields")
        search_mode = ttk.Combobox(
            search_frame,
            textvariable=self.search_mode_var,
            values=["All fields", "Name", "Category", "Ingredient"],
            state="readonly",
            width=14,
        )
        search_mode.grid(row=0, column=2, padx=4, pady=4)

        ttk.Button(
            search_frame,
            text="Linear Search",
            command=self.search_recipes,
        ).grid(row=0, column=3, padx=4, pady=4)

        ttk.Button(
            search_frame,
            text="Exact Name Search",
            command=self.exact_name_search,
        ).grid(row=0, column=4, padx=4, pady=4)

        ttk.Button(
            search_frame,
            text="Show All",
            command=self.show_all_recipes,
        ).grid(row=0, column=5, padx=(4, 0), pady=4)

        action_frame = ttk.Frame(self.recipe_tab)
        action_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        action_frame.columnconfigure(5, weight=1)

        ttk.Button(
            action_frame,
            text="Add Recipe",
            command=self.open_add_recipe_form,
        ).grid(row=0, column=0, padx=(0, 5))

        ttk.Button(
            action_frame,
            text="Edit Selected",
            command=self.open_edit_recipe_form,
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            action_frame,
            text="Delete Selected",
            command=self.delete_selected_recipe,
        ).grid(row=0, column=2, padx=5)

        ttk.Label(action_frame, text="Sort by:").grid(
            row=0,
            column=3,
            padx=(20, 5),
        )

        self.sort_var = tk.StringVar(value="Name")
        sort_box = ttk.Combobox(
            action_frame,
            textvariable=self.sort_var,
            values=["Name", "Preparation time", "Calories"],
            state="readonly",
            width=18,
        )
        sort_box.grid(row=0, column=4, padx=5)

        ttk.Button(
            action_frame,
            text="Apply Insertion Sort",
            command=self.sort_recipes,
        ).grid(row=0, column=6, padx=(5, 0))

        table_frame = ttk.Frame(self.recipe_tab)
        table_frame.grid(row=2, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = (
            "recipe_id",
            "name",
            "category",
            "prep_time",
            "servings",
            "calories",
            "ingredients",
        )
        self.recipe_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "recipe_id": "ID",
            "name": "Name",
            "category": "Category",
            "prep_time": "Prep time",
            "servings": "Servings",
            "calories": "Calories",
            "ingredients": "Ingredients",
        }
        widths = {
            "recipe_id": 65,
            "name": 165,
            "category": 100,
            "prep_time": 85,
            "servings": 75,
            "calories": 75,
            "ingredients": 330,
        }

        for column in columns:
            self.recipe_tree.heading(column, text=headings[column])
            self.recipe_tree.column(
                column,
                width=widths[column],
                minwidth=55,
                anchor="w",
            )

        vertical_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.recipe_tree.yview,
        )
        horizontal_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.recipe_tree.xview,
        )
        self.recipe_tree.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set,
        )

        self.recipe_tree.grid(row=0, column=0, sticky="nsew")
        vertical_scroll.grid(row=0, column=1, sticky="ns")
        horizontal_scroll.grid(row=1, column=0, sticky="ew")

        self.recipe_status_var = tk.StringVar()
        ttk.Label(
            self.recipe_tab,
            textvariable=self.recipe_status_var,
        ).grid(row=3, column=0, sticky="w", pady=(8, 0))

    # Build the weekly planner grid.
    def build_planner_tab(self):
        self.planner_tab.columnconfigure(0, weight=1)

        planner_frame = ttk.LabelFrame(
            self.planner_tab,
            text="Seven-day meal plan",
            padding=10,
        )
        planner_frame.grid(row=0, column=0, sticky="nsew")

        for column in range(5):
            planner_frame.columnconfigure(column, weight=1)

        ttk.Label(planner_frame, text="Day").grid(
            row=0,
            column=0,
            padx=5,
            pady=6,
            sticky="w",
        )

        for column, meal_type in enumerate(MEAL_TYPES, start=1):
            ttk.Label(planner_frame, text=meal_type).grid(
                row=0,
                column=column,
                padx=5,
                pady=6,
            )

        ttk.Label(planner_frame, text="Daily calories").grid(
            row=0,
            column=4,
            padx=5,
            pady=6,
        )

        for row, day in enumerate(DAYS, start=1):
            ttk.Label(planner_frame, text=day).grid(
                row=row,
                column=0,
                padx=5,
                pady=6,
                sticky="w",
            )

            for column, meal_type in enumerate(MEAL_TYPES, start=1):
                meal_var = tk.StringVar()
                meal_box = ttk.Combobox(
                    planner_frame,
                    textvariable=meal_var,
                    state="readonly",
                    width=24,
                )
                meal_box.grid(
                    row=row,
                    column=column,
                    padx=5,
                    pady=6,
                    sticky="ew",
                )
                meal_box.bind(
                    "<<ComboboxSelected>>",
                    lambda event: self.update_plan_summary(),
                )
                self.meal_vars[(day, meal_type)] = (meal_var, meal_box)

            calorie_var = tk.StringVar(value="0 kcal")
            ttk.Label(planner_frame, textvariable=calorie_var).grid(
                row=row,
                column=4,
                padx=5,
                pady=6,
            )
            self.calorie_labels[day] = calorie_var

        button_frame = ttk.Frame(self.planner_tab)
        button_frame.grid(row=1, column=0, sticky="ew", pady=12)

        ttk.Button(
            button_frame,
            text="Save Weekly Plan",
            command=self.save_weekly_plan,
        ).pack(side="left", padx=(0, 6))

        ttk.Button(
            button_frame,
            text="Reload Saved Plan",
            command=self.reload_weekly_plan,
        ).pack(side="left", padx=6)

        ttk.Button(
            button_frame,
            text="Clear All Slots",
            command=self.clear_plan_slots,
        ).pack(side="left", padx=6)

        self.plan_status_var = tk.StringVar()
        ttk.Label(
            self.planner_tab,
            textvariable=self.plan_status_var,
        ).grid(row=2, column=0, sticky="w")

    # Build the shopping list controls.
    def build_shopping_tab(self):
        self.shopping_tab.columnconfigure(0, weight=1)
        self.shopping_tab.rowconfigure(1, weight=1)

        button_frame = ttk.Frame(self.shopping_tab)
        button_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        ttk.Button(
            button_frame,
            text="Generate Shopping List",
            command=self.generate_shopping_list_view,
        ).pack(side="left", padx=(0, 6))

        ttk.Button(
            button_frame,
            text="Save as Text File",
            command=self.save_shopping_list_file,
        ).pack(side="left", padx=6)

        ttk.Button(
            button_frame,
            text="Clear Display",
            command=self.clear_shopping_display,
        ).pack(side="left", padx=6)

        text_frame = ttk.Frame(self.shopping_tab)
        text_frame.grid(row=1, column=0, sticky="nsew")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.shopping_text = tk.Text(
            text_frame,
            wrap="word",
            state="disabled",
            padx=10,
            pady=10,
        )
        shopping_scroll = ttk.Scrollbar(
            text_frame,
            orient="vertical",
            command=self.shopping_text.yview,
        )
        self.shopping_text.configure(yscrollcommand=shopping_scroll.set)
        self.shopping_text.grid(row=0, column=0, sticky="nsew")
        shopping_scroll.grid(row=0, column=1, sticky="ns")

        self.shopping_status_var = tk.StringVar(
            value="Generate a list from the current weekly planner selections."
        )
        ttk.Label(
            self.shopping_tab,
            textvariable=self.shopping_status_var,
        ).grid(row=2, column=0, sticky="w", pady=(8, 0))

    # Show warnings found during startup.
    def show_startup_warnings(self, messages):
        unique_messages = []

        for message in messages:
            if message not in unique_messages:
                unique_messages.append(message)

        messagebox.showwarning(
            "Data file notice",
            "\n".join(unique_messages),
            parent=self.root,
        )

    # Display a list of recipes in the table.
    def refresh_recipe_table(self, recipes):
        for item in self.recipe_tree.get_children():
            self.recipe_tree.delete(item)

        for recipe in recipes:
            self.recipe_tree.insert(
                "",
                "end",
                values=(
                    recipe["recipe_id"],
                    recipe["name"],
                    recipe["category"],
                    str(recipe["prep_time"]) + " min",
                    recipe["servings"],
                    recipe["calories"],
                    ", ".join(recipe["ingredients"]),
                ),
            )

        self.recipe_status_var.set(
            "Showing " + str(len(recipes)) + " of " + str(len(self.recipes)) + " recipes."
        )

    # Get the selected recipe.
    def get_selected_recipe(self):
        selected_items = self.recipe_tree.selection()

        if len(selected_items) == 0:
            messagebox.showinfo(
                "Select a recipe",
                "Please select a recipe first.",
                parent=self.root,
            )
            return None

        values = self.recipe_tree.item(selected_items[0], "values")
        return find_recipe_by_id(self.recipes, values[0])

    # Display all recipes.
    def show_all_recipes(self):
        self.search_var.set("")
        self.refresh_recipe_table(self.recipes)

    # Run a linear search.
    def search_recipes(self):
        query = self.search_var.get().strip()

        if query == "":
            messagebox.showinfo(
                "Search",
                "Please enter search text.",
                parent=self.root,
            )
            return

        results = linear_search(
            self.recipes,
            query,
            self.search_mode_var.get(),
        )
        self.refresh_recipe_table(results)

        if len(results) == 0:
            self.recipe_status_var.set("No matching recipes were found.")

    # Run a recursive exact-name search.
    def exact_name_search(self):
        query = self.search_var.get().strip()

        if query == "":
            messagebox.showinfo(
                "Exact name search",
                "Please enter a complete recipe name.",
                parent=self.root,
            )
            return

        sorted_recipes = insertion_sort(self.recipes, "name")
        result = recursive_binary_search(sorted_recipes, query)

        if result is None:
            self.refresh_recipe_table([])
            self.recipe_status_var.set("No exact recipe name was found.")
        else:
            self.refresh_recipe_table([result])
            self.recipe_status_var.set("Exact recipe found using recursive binary search.")

    # Sort recipes using the selected field.
    def sort_recipes(self):
        sort_fields = {
            "Name": "name",
            "Preparation time": "prep_time",
            "Calories": "calories",
        }
        sort_field = sort_fields[self.sort_var.get()]
        sorted_recipes = insertion_sort(self.recipes, sort_field)
        self.refresh_recipe_table(sorted_recipes)
        self.recipe_status_var.set(
            "Recipes sorted by " + self.sort_var.get().lower() + "."
        )

    # Open a blank recipe form.
    def open_add_recipe_form(self):
        self.open_recipe_form()

    # Open the selected recipe form.
    def open_edit_recipe_form(self):
        recipe = self.get_selected_recipe()

        if recipe is not None:
            self.open_recipe_form(recipe)

    # Build the add or edit recipe form.
    def open_recipe_form(self, recipe=None):
        form_window = tk.Toplevel(self.root)
        form_window.title("Edit Recipe" if recipe else "Add Recipe")
        form_window.transient(self.root)
        form_window.grab_set()
        form_window.resizable(False, False)

        form_frame = ttk.Frame(form_window, padding=14)
        form_frame.grid(row=0, column=0, sticky="nsew")
        form_frame.columnconfigure(1, weight=1)

        name_var = tk.StringVar(value=recipe["name"] if recipe else "")
        category_var = tk.StringVar(
            value=recipe["category"] if recipe else RECIPE_CATEGORIES[0]
        )
        prep_time_var = tk.StringVar(
            value=str(recipe["prep_time"]) if recipe else ""
        )
        servings_var = tk.StringVar(
            value=str(recipe["servings"]) if recipe else ""
        )
        calories_var = tk.StringVar(
            value=str(recipe["calories"]) if recipe else ""
        )

        labels = [
            "Recipe name:",
            "Category:",
            "Preparation time:",
            "Servings:",
            "Calories per serving:",
        ]

        for row, label_text in enumerate(labels):
            ttk.Label(form_frame, text=label_text).grid(
                row=row,
                column=0,
                padx=(0, 10),
                pady=6,
                sticky="w",
            )

        ttk.Entry(form_frame, textvariable=name_var, width=38).grid(
            row=0,
            column=1,
            pady=6,
            sticky="ew",
        )
        ttk.Combobox(
            form_frame,
            textvariable=category_var,
            values=RECIPE_CATEGORIES,
            state="readonly",
            width=35,
        ).grid(row=1, column=1, pady=6, sticky="ew")
        ttk.Entry(form_frame, textvariable=prep_time_var).grid(
            row=2,
            column=1,
            pady=6,
            sticky="ew",
        )
        ttk.Entry(form_frame, textvariable=servings_var).grid(
            row=3,
            column=1,
            pady=6,
            sticky="ew",
        )
        ttk.Entry(form_frame, textvariable=calories_var).grid(
            row=4,
            column=1,
            pady=6,
            sticky="ew",
        )

        ttk.Label(
            form_frame,
            text="Ingredients (separate with commas):",
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            pady=(8, 4),
            sticky="w",
        )

        ingredients_text = tk.Text(form_frame, width=48, height=5, wrap="word")
        ingredients_text.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="ew",
        )

        if recipe:
            ingredients_text.insert("1.0", ", ".join(recipe["ingredients"]))

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(
            row=7,
            column=0,
            columnspan=2,
            pady=(12, 0),
            sticky="e",
        )

        def save_form():
            excluded_id = recipe["recipe_id"] if recipe else None

            try:
                recipe_data = validate_recipe_input(
                    self.recipes,
                    name_var.get(),
                    category_var.get(),
                    prep_time_var.get(),
                    servings_var.get(),
                    calories_var.get(),
                    ingredients_text.get("1.0", "end").strip(),
                    excluded_id,
                )
            except ValueError as error:
                messagebox.showerror(
                    "Invalid recipe",
                    str(error),
                    parent=form_window,
                )
                return

            candidate_recipes = copy.deepcopy(self.recipes)

            if recipe is None:
                saved_recipe = add_recipe(candidate_recipes, recipe_data)
                success_message = saved_recipe["name"] + " was added."
            else:
                updated = update_recipe(
                    candidate_recipes,
                    recipe["recipe_id"],
                    recipe_data,
                )

                if not updated:
                    messagebox.showerror(
                        "Edit recipe",
                        "The selected recipe could not be found.",
                        parent=form_window,
                    )
                    return

                success_message = recipe_data["name"] + " was updated."

            try:
                save_recipes(candidate_recipes)
            except OSError as error:
                messagebox.showerror(
                    "Save recipe",
                    "The recipe could not be saved:\n" + str(error),
                    parent=form_window,
                )
                return

            self.recipes = candidate_recipes
            self.refresh_recipe_table(self.recipes)
            self.refresh_recipe_choices()
            self.update_plan_summary()
            form_window.destroy()
            messagebox.showinfo(
                "Recipe saved",
                success_message,
                parent=self.root,
            )

        ttk.Button(
            button_frame,
            text="Cancel",
            command=form_window.destroy,
        ).pack(side="left", padx=(0, 6))

        ttk.Button(
            button_frame,
            text="Save Recipe",
            command=save_form,
        ).pack(side="left")

    # Delete the selected recipe and clear its meal slots.
    def delete_selected_recipe(self):
        recipe = self.get_selected_recipe()

        if recipe is None:
            return

        confirmed = messagebox.askyesno(
            "Delete recipe",
            "Delete "
            + recipe["name"]
            + "? Any weekly plan slots using it will be cleared.",
            parent=self.root,
        )

        if not confirmed:
            return

        candidate_recipes = copy.deepcopy(self.recipes)
        candidate_plan = copy_weekly_plan(self.weekly_plan)
        delete_recipe(candidate_recipes, recipe["recipe_id"])
        removed_slots = remove_recipe_from_plan(
            candidate_plan,
            recipe["recipe_id"],
        )

        try:
            save_meal_plan(candidate_plan)
            save_recipes(candidate_recipes)
        except OSError as error:
            messagebox.showerror(
                "Delete recipe",
                "The changes could not be saved:\n" + str(error),
                parent=self.root,
            )
            return

        self.recipes = candidate_recipes
        self.weekly_plan = candidate_plan
        self.refresh_recipe_table(self.recipes)
        self.refresh_recipe_choices()
        self.update_plan_summary()
        self.clear_shopping_display()

        message = recipe["name"] + " was deleted."

        if removed_slots > 0:
            message += " " + str(removed_slots) + " meal slot(s) were cleared."

        messagebox.showinfo("Recipe deleted", message, parent=self.root)

    # Update planner recipe choices.
    def refresh_recipe_choices(self):
        sorted_recipes = insertion_sort(self.recipes, "name")
        recipe_values = [""]
        self.display_to_id = {"": None}
        self.id_to_display = {None: ""}

        for recipe in sorted_recipes:
            display_name = recipe["recipe_id"] + " - " + recipe["name"]
            recipe_values.append(display_name)
            self.display_to_id[display_name] = recipe["recipe_id"]
            self.id_to_display[recipe["recipe_id"]] = display_name

        for day in DAYS:
            for meal_type in MEAL_TYPES:
                meal_var, meal_box = self.meal_vars[(day, meal_type)]
                meal_box["values"] = recipe_values
                recipe_id = self.weekly_plan[day][meal_type]
                meal_var.set(self.id_to_display.get(recipe_id, ""))

    # Read the meal plan selections from the interface.
    def collect_plan_from_widgets(self):
        weekly_plan = clear_weekly_plan()

        for day in DAYS:
            for meal_type in MEAL_TYPES:
                meal_var, meal_box = self.meal_vars[(day, meal_type)]
                display_name = meal_var.get()

                if display_name not in self.display_to_id:
                    raise ValueError(
                        "One meal selection is no longer available."
                    )

                weekly_plan[day][meal_type] = self.display_to_id[display_name]

        return weekly_plan

    # Save the weekly planner selections.
    def save_weekly_plan(self):
        try:
            candidate_plan = self.collect_plan_from_widgets()
            save_meal_plan(candidate_plan)
        except (OSError, ValueError) as error:
            messagebox.showerror(
                "Save weekly plan",
                "The weekly plan could not be saved:\n" + str(error),
                parent=self.root,
            )
            return

        self.weekly_plan = candidate_plan
        self.update_plan_summary()
        self.clear_shopping_display()
        messagebox.showinfo(
            "Weekly plan",
            "The weekly meal plan was saved.",
            parent=self.root,
        )

    # Reload the saved weekly plan.
    def reload_weekly_plan(self):
        weekly_plan, warnings = load_meal_plan(self.recipes)
        self.weekly_plan = weekly_plan
        self.refresh_recipe_choices()
        self.update_plan_summary()
        self.clear_shopping_display()

        if len(warnings) > 0:
            messagebox.showwarning(
                "Reload weekly plan",
                "\n".join(warnings),
                parent=self.root,
            )
        else:
            messagebox.showinfo(
                "Reload weekly plan",
                "The saved weekly plan was reloaded.",
                parent=self.root,
            )

    # Clear all meal planner selections.
    def clear_plan_slots(self):
        confirmed = messagebox.askyesno(
            "Clear weekly plan",
            "Clear all breakfast, lunch and dinner selections?",
            parent=self.root,
        )

        if not confirmed:
            return

        for meal_var, meal_box in self.meal_vars.values():
            meal_var.set("")

        self.update_plan_summary()
        self.clear_shopping_display()

    # Update daily calorie values and meal count.
    def update_plan_summary(self):
        try:
            current_plan = self.collect_plan_from_widgets()
        except ValueError:
            current_plan = self.weekly_plan

        daily_calories = calculate_daily_calories(
            current_plan,
            self.recipes,
        )

        for day in DAYS:
            self.calorie_labels[day].set(
                str(daily_calories[day]) + " kcal"
            )

        planned_meals = count_planned_meals(current_plan)
        weekly_total = sum(daily_calories.values())
        self.plan_status_var.set(
            str(planned_meals)
            + " meal slots selected | Weekly calories: "
            + str(weekly_total)
            + " kcal"
        )

    # Generate and display shopping items.
    def generate_shopping_list_view(self):
        try:
            current_plan = self.collect_plan_from_widgets()
        except ValueError as error:
            messagebox.showerror(
                "Shopping list",
                str(error),
                parent=self.root,
            )
            return

        self.shopping_items = generate_shopping_list(
            current_plan,
            self.recipes,
        )
        self.shopping_text.configure(state="normal")
        self.shopping_text.delete("1.0", "end")

        if len(self.shopping_items) == 0:
            self.shopping_text.insert(
                "end",
                "No ingredients are available because the weekly plan is empty.",
            )
        else:
            for item in self.shopping_items:
                self.shopping_text.insert("end", "- " + item + "\n")

        self.shopping_text.configure(state="disabled")
        self.shopping_status_var.set(
            str(len(self.shopping_items)) + " unique ingredient(s) generated."
        )

    # Save the current shopping list as text.
    def save_shopping_list_file(self):
        if len(self.shopping_items) == 0:
            self.generate_shopping_list_view()

        if len(self.shopping_items) == 0:
            messagebox.showinfo(
                "Shopping list",
                "There are no shopping items to save.",
                parent=self.root,
            )
            return

        filename = filedialog.asksaveasfilename(
            parent=self.root,
            title="Save shopping list",
            initialdir=str(SHOPPING_LIST_FILE.parent),
            initialfile=SHOPPING_LIST_FILE.name,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )

        if filename == "":
            return

        try:
            save_shopping_list(self.shopping_items, filename)
        except OSError as error:
            messagebox.showerror(
                "Save shopping list",
                "The shopping list could not be saved:\n" + str(error),
                parent=self.root,
            )
            return

        messagebox.showinfo(
            "Shopping list",
            "The shopping list was saved.",
            parent=self.root,
        )

    # Clear the shopping list display.
    def clear_shopping_display(self):
        self.shopping_items = []
        self.shopping_text.configure(state="normal")
        self.shopping_text.delete("1.0", "end")
        self.shopping_text.configure(state="disabled")
        self.shopping_status_var.set(
            "Generate a list from the current weekly planner selections."
        )

    # Start the tkinter event loop.
    def run(self):
        self.root.mainloop()
