import streamlit as st
import requests
import json
import random
import re

def main():
    st.title("Food Recipes")
    st.markdown("Food Recipe recommendation system based on user input for any food and maximum calories.")  
    # Textbox for Food Type Input
    food_type = st.text_input('Enter Any Food')

    # Slider for Calories
    calories = st.slider("Select Max Calories", 25, 1000, 500)
    st.write("Selected: **{}** Max Calories.".format(calories))
    if st.button("Submit"):
        url = "https://alcksyjrmd.execute-api.us-east-2.amazonaws.com/default/nutrients_response"

        params = {"f": food_type.capitalize(), "k": str(calories)}

        response = requests.get(url, params=params)
        response_json = json.loads(response.content)

        # Convert response_json to a list
        response_json = list(response_json)

        # Randomly select a recipe
        st.markdown("## Recommended Recipe")
        if len(response_json) > 0:
            random_recipe = random.choice(response_json)
            recipe_calories = random_recipe['Calories']
            st.write("**Title:** ", random_recipe['Title'])
            st.write("**Calories:** ", recipe_calories)
            st.write("**Total Fat:** ", random_recipe['Total Fat'])
            st.write("**Total Carbohydrate:** ", random_recipe['Total Carbohydrate'])
            st.write("**Protein:** ", random_recipe['Protein'])
            st.write("**Tags:** ", random_recipe['Tags'])
            if random_recipe['Image Link'].endswith(".jpg") or random_recipe['Image Link'].endswith(".jpeg") or random_recipe['Image Link'].endswith(".png"):
                st.image(random_recipe['Image Link'], width=300)
            else:
                st.write("**Image Link:** ", random_recipe['Image Link'])            
            st.write("**Recipe URL:** ", random_recipe['Recipe URLs']) 
            st.write("*To download this recipe as a PDF, open the hamburger menu on the top right and click on Print.*")
        else:
            st.markdown("### No Recipes Found:")
            st.write("**No recipes found that match your search criteria. Please try a different food type.**")

if __name__ == '__main__':
    main()
