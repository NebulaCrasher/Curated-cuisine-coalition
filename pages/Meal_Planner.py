import streamlit as st
import requests
import json
import random
import re

def main():
    st.title("Meal Planner")
    st.markdown("The Meal Planner app helps users plan a meal with three recipes that fit their dietary needs, cuisine preferences, specific ingredients, and calorie limits. After submitting their choices, the app retrieves recipe options from an API and randomly selects one recipe from each of the following categories: breakfast, lunch, and dinner. The app also displays the selected recipes' nutrition information and calculates the total nutrition of all three recipes combined.")
    
    # Dropdown for Diet
    diet_options = ['All', 'Gluten-Free', 'Vegan', 'Vegetarian', 'Dairy-Free']
    diet = st.selectbox('Diet', diet_options)

    # Dropdown for Cuisine
    cuisine_options = ['All', 'African', 'Asian', 'Caribbean', 'Central American', 'Europe', 'Middle Eastern', 'North American', 'Oceanic', 'South American']
    cuisine = st.selectbox('Cuisine', cuisine_options)

    # Text input for ingredients
    ingredients = st.text_input("Enter ingredients (Separated By Commas)", placeholder="Enter Atleast One Ingredient", value="")    

    # Slider for Calories
    calories = st.slider("Select Max Calories for All Three Recipes", 25, 2500, 1500)
    st.write("Selected: **{}** Max Calories.".format(calories))
    
    # Submit button
    if st.button("Submit"):
        if not ingredients:  # Check if ingredients text input field is empty
            st.error("Please enter at least one ingredient.")
            return
        url = "https://alcksyjrmd.execute-api.us-east-2.amazonaws.com/default/nutrients_response"

        params = {"k": str(calories)}

        if diet != "All":
            params["d"] = diet

        if cuisine != "All":
            params["c"] = cuisine

        if ingredients:
            params["i"] = ingredients

        response = requests.get(url, params=params)
        if len(response.content) < 180:
            st.error("The query was too large, please decrease the calories or fine-tune your search.")
            return
        response_json = json.loads(response.content)


        

        # Convert response_json to a list
        response_json = list(response_json)

        # Find 3 recipes that add up to the target calorie limit
        recipes = []
        total_calories = 0

        # Breakfast Section
        st.markdown("## Breakfast Recipe")
        breakfast_recipes = [recipe for recipe in response_json if "breakfast" in recipe['Course Keywords']]
        if len(breakfast_recipes) > 0:
            random_recipe = random.choice(breakfast_recipes)
            recipe_calories = random_recipe['Calories']
            if total_calories + recipe_calories <= calories:
                total_calories += recipe_calories
                recipes.append(random_recipe)
                st.write("**Title:** ", random_recipe['Title'])
                st.write("**Calories:** ", recipe_calories)
                st.write("**Total Fat:** ", random_recipe['Total Fat'])
                st.write("**Total Carbohydrate:** ", random_recipe['Total Carbohydrate'])
                st.write("**Protein:** ", random_recipe['Protein'])
                if random_recipe['Image Link'].endswith(".jpg") or random_recipe['Image Link'].endswith(".jpeg") or random_recipe['Image Link'].endswith(".png"):
                    st.image(random_recipe['Image Link'], width=300)
                else:
                    st.write("**Image Link:** ", random_recipe['Image Link'])            
                st.write("**Recipe URL:** ", random_recipe['Recipe URLs']) 
                st.markdown("---")

        # Brunch Section
        st.markdown("## Lunch Recipe")
        brunch_recipes = [recipe for recipe in response_json if "main" in recipe['Course Keywords']]
        if len(brunch_recipes) > 0:
            random_recipe = random.choice(brunch_recipes)
            recipe_calories = random_recipe['Calories']
            if total_calories + recipe_calories <= calories:
                total_calories += recipe_calories
                recipes.append(random_recipe)
                st.write("**Title:** ", random_recipe['Title'])
                st.write("**Calories:** ", recipe_calories)
                st.write("**Total Fat:** ", random_recipe['Total Fat'])
                st.write("**Total Carbohydrate:** ", random_recipe['Total Carbohydrate'])
                st.write("**Protein:** ", random_recipe['Protein'])
                if random_recipe['Image Link'].endswith(".jpg") or random_recipe['Image Link'].endswith(".jpeg") or random_recipe['Image Link'].endswith(".png"):
                    st.image(random_recipe['Image Link'], width=300)
                else:
                    st.write("**Image Link:** ", random_recipe['Image Link'])            
                st.write("**Recipe URL:** ", random_recipe['Recipe URLs']) 
                st.markdown("---")

        # Main Section
        st.markdown("## Dinner Recipe")
        main_recipes = [recipe for recipe in response_json if "main" in recipe['Course Keywords']]
        if len(main_recipes) > 0:
            random_recipe = random.choice(main_recipes)
            recipe_calories = random_recipe['Calories']
            if total_calories + recipe_calories <= calories:
                total_calories += recipe_calories
                recipes.append(random_recipe)
                st.write("**Title:** ", random_recipe['Title'])
                st.write("**Calories:** ", recipe_calories)
                st.write("**Total Fat:** ", random_recipe['Total Fat'])
                st.write("**Total Carbohydrate:** ", random_recipe['Total Carbohydrate'])
                st.write("**Protein:** ", random_recipe['Protein'])
                if random_recipe['Image Link'].endswith(".jpg") or random_recipe['Image Link'].endswith(".jpeg") or random_recipe['Image Link'].endswith(".png"):
                    st.image(random_recipe['Image Link'], width=300)
                else:
                    st.write("**Image Link:** ", random_recipe['Image Link'])            
                st.write("**Recipe URL:** ", random_recipe['Recipe URLs']) 
        else:
            st.markdown("### Not Enough Recipes Found:")
            st.write("**Not enough recipes found that match your search criteria. Please adjust your search criteria.**")

        if len(recipes) < 3:
            st.markdown("### Not Enough Recipes Found:")
            st.write("**Not enough recipes found that match your search criteria. Please adjust your search criteria.**")
        else:
            st.markdown("---")

            # Calculate total Calories, Total Fat, Total Carbohydrate, and Protein of all three recipes
            total_calories = 0
            total_fat = 0
            total_carbs = 0
            total_protein = 0
            for recipe in recipes:
                total_calories += recipe['Calories']
                total_fat += float(re.sub(r'[^\d.]+', '', recipe['Total Fat']))
                total_carbs += float(re.sub(r'[^\d.]+', '', recipe['Total Carbohydrate']))
                total_protein += float(re.sub(r'[^\d.]+', '', recipe['Protein']))

            st.markdown("## Total Nutrition of All Three Recipes")
            st.write("Total Calories:", total_calories)
            st.write("Total Fat:", total_fat, "g")
            st.write("Total Carbohydrate:", total_carbs, "g")
            st.write("Total Protein:", total_protein, "g")
            st.write("") 
            st.write("*To download this recipe as a PDF, open the hamburger menu on the top right and click on Print.*") 

if __name__ == '__main__':
    main()
