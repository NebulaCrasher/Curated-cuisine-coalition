import streamlit as st
import random
import pandas as pd
from PIL import Image
import requests
import json
from transformers import pipeline
import numpy as np
from transformers import AutoFeatureExtractor
from transformers import AutoModelForImageClassification
import plotly.graph_objects as go
import plotly
import re


st.set_page_config(layout='wide',
                   page_title='Food Category Classification & Recipes Recommender'
                   )

st.sidebar.markdown("<h3 style='text-align: center;'>Project Location:</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center;'><strong><a href='https://huggingface.co/Kaludi/food-category-classification-v2.0'>Model</a></strong>  |  <strong><a href='https://huggingface.co/datasets/Kaludi/food-category-classification-v2.0'>Dataset</a></strong>  |  <strong><a href='https://github.com/NebulaCrasher/curated-cuisine-coalition'>GitHub</a></strong></p>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='text-align: center;'>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='text-align: center;'>Project Creators:</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center;'><a href='https://github.com/Alhamzahalabboodi'><strong>Alhamzah Alabboodi</strong></a></p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center;'><a href='https://github.com/amoonguaklang12'><strong>Anderson Moonguaklang</strong></a></p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center;'><a href='https://github.com/Kaludii'><strong>Bilal Kaludi</strong></a></p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center;'><a href='https://github.com/NebulaCrasher'><strong>Davit Ksor</strong></a></p>", unsafe_allow_html=True)
    

def main():
    st.title("Food Category Classification & Recipes")
    st.markdown("This app is using a Food Category Image Classifier model that has been trained by [Kaludi](https://huggingface.co/Kaludi) to recognize **12** different categories of foods, which includes **Bread**, **Dairy**, **Dessert**, **Egg**, **Fried Food**, **Fruit**, **Meat**, **Noodles**, **Rice**, **Seafood**, **Soup**, and **Vegetable**. After classifying the category, it provides a personalized recipe recommendations based on user preferences for diet and cuisine. With its easy-to-use interface and integration with recipe databases, the app is perfect for food lovers looking for personalized recipe suggestions.")  
    st.header("Try it out!")

    if st.checkbox("Show/Hide Examples"):
        st.header("Example Images")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.image("examples/example_0.jpg", width=260)
            st.image("examples/example_1.jpg", width=260)

        with col2:
            st.image("examples/example_2.jpg", width=260)
            st.image("examples/example_3.jpg", width=260)

        with col3:
            st.image("examples/example_4.jpg", width=260)
            st.image("examples/example_5.jpg", width=260)

        with col4:
            st.image("examples/example_6.jpg", width=260)
            st.image("examples/example_7.jpg", width=260)
 
#    # display the text if the checkbox returns True value
#        show_images = not show_images
#        if show_images:
#            st.header("Example Images")
#            for image in images:
#                st.image(image, width=260)

#    select_health = st.radio("Select One (Not Functional Yet):", ["Regular", "Low-Calorie"], horizontal=True)

    # Dropdown for Diet
    diet_options = ['All', 'Gluten-Free', 'Vegan', 'Vegetarian', 'Dairy-Free']
    diet = st.selectbox('Diet', diet_options)

    # Dropdown for Cuisine
    cuisine_options = ['All', 'African', 'Asian', 'Caribbean', 'Central American', 'Europe', 'Middle Eastern', 'North American', 'Oceanic', 'South American']

    cuisine = st.selectbox('Cuisine', cuisine_options)

    # Slider for Calories
    calories = st.slider("Select Max Calories (Per Serving)", 25, 1000, 500)
    
    # print the calories
    st.write("Selected: **{}** Max Calories.".format(calories))

    uploaded_file = st.file_uploader("Upload Files", type=['png','jpeg','jpg'])

    loading_text = st.empty()

    if uploaded_file != None:
        loading_text.markdown("Loading...")
        img = Image.open(uploaded_file)
        extractor = AutoFeatureExtractor.from_pretrained("Kaludi/food-category-classification-v2.0")
        model = AutoModelForImageClassification.from_pretrained("Kaludi/food-category-classification-v2.0")
        inputs = extractor(img, return_tensors="pt")
        outputs = model(**inputs)
        # ...
        loading_text.empty()
        label_num=outputs.logits.softmax(1).argmax(1)
        label_num=label_num.item()
        

        probs = outputs.logits.softmax(dim=1)
        percentage = round(probs[0, label_num].item() * 100, 2)

        st.markdown("### Your Image:")
        st.image(img, width=260)

        st.write("The Predicted Classification is:")

        if label_num==0:
            st.write("**Bread** (" + f"{percentage}%)")
        elif label_num==1:
            st.write("**Dairy** (" + f"{percentage}%)")
        elif label_num==2:
            st.write("**Dessert** (" + f"{percentage}%)")
        elif label_num==3:
            st.write("**Egg** (" + f"{percentage}%)")
        elif label_num==4:
            st.write("**Fried Food** (" + f"{percentage}%)")
        elif label_num==5:
            st.write("**Fruit** (" + f"{percentage}%)")
        elif label_num==6:
            st.write("**Meat** (" + f"{percentage}%)")
        elif label_num==7:
            st.write("**Noodles** (" + f"{percentage}%)")
        elif label_num==8:
            st.write("**Rice** (" + f"{percentage}%)")
        elif label_num==9:
            st.write("**Seafood** (" + f"{percentage}%)")
        elif label_num==10:
            st.write("**Soup** (" + f"{percentage}%)")
        else:
            st.write("**Vegetable** (" + f"{percentage}%)")
    
        st.write("You Selected **{}** For Diet and **{}** For Cuisine with Max".format(diet, cuisine), calories, "Calories For", ( "**Bread**" if label_num==0 else "**Dairy**" if label_num==1 else "**Dessert**" if label_num==2 else "**Egg**" if label_num==3 else "**Fried Food**" if label_num==4 else "**Fruit**" if label_num==5 else "**Meat**" if label_num==6 else "**Noodles**" if label_num==7 else "**Rice**" if label_num==8 else "**Seafood**" if label_num==9 else "**Soup**" if label_num==10 else "**Vegetable**"))

        url = "https://alcksyjrmd.execute-api.us-east-2.amazonaws.com/default/nutrients_response"

        category = ("Bread" if label_num==0 else "Dairy" if label_num==1 else "Dessert" if label_num==2 else "Egg" if label_num==3 else "Fried" if label_num==4 else "Fruit" if label_num==5 else "Meat" if label_num==6 else "Noodles" if label_num==7 else "Rice" if label_num==8 else "Seafood" if label_num==9 else "**Soup**" if label_num==10 else "Vegetable")

        params = {"f": category, "k": str(calories)}

        if diet != "All":
            params["d"] = diet

        if cuisine != "All":
            params["c"] = cuisine

        response = requests.get(url, params=params)
        response_json = json.loads(response.content)
        # Convert response_json to a list
        response_json = list(response_json)

        if len(response_json) == 0:
            st.markdown("### No Recipe Found:")
            st.write("**No recipes found. Please adjust your search criteria.**")
        else:
            if len(response_json) > 1:
                random_recipe = random.choice(response_json)
                if st.button("Get Another Recipe"):
                    response_json.remove(random_recipe)
                    if len(response_json) == 0:
                        st.write("No more recipes. Please adjust your search criteria.")
                    else:
                        random_recipe = random.choice(response_json)                 
                st.markdown("### Recommended Recipe:")             
                st.write("**Title:** ", random_recipe['Title'])
                if random_recipe['Image Link'].endswith(".jpg") or random_recipe['Image Link'].endswith(".jpeg") or random_recipe['Image Link'].endswith(".png"):
                    st.image(random_recipe['Image Link'], width=300)
                else:
                    st.write("**Image Link:** ", random_recipe['Image Link'])
                st.write("**Rating:** ", random_recipe['Rating'])
                if random_recipe['Description'] != "Description not found":
                    st.write("**Description:** ", random_recipe['Description'])
                st.write("**Ingredients:**<br>", random_recipe['Ingredients'].replace('\n', '<br>'), unsafe_allow_html=True)
                st.write("**Recipe Facts:**<br>", random_recipe['Recipe Facts'].replace('\n', '<br>'), unsafe_allow_html=True)
                st.write("**Directions:**<br>", random_recipe['Directions'].replace('\n', '<br>'), unsafe_allow_html=True)                  
                # extract only numeric values and convert mg to g
                values = [
                    float(re.sub(r'[^\d.]+', '', random_recipe['Total Fat'])), 
                    float(re.sub(r'[^\d.]+', '', random_recipe['Saturated Fat'])), 
                    float(re.sub(r'[^\d.]+', '', random_recipe['Cholesterol'])) / 1000, 
                    float(re.sub(r'[^\d.]+', '', random_recipe['Sodium'])) / 1000, 
                    float(re.sub(r'[^\d.]+', '', random_recipe['Total Carbohydrate'])), 
                    float(re.sub(r'[^\d.]+', '', random_recipe['Dietary Fiber'])), 
                    float(re.sub(r'[^\d.]+', '', random_recipe['Total Sugars'])), 
                    float(re.sub(r'[^\d.]+', '', random_recipe['Protein'])),
                    float(re.sub(r'[^\d.]+', '', random_recipe['Vitamin C'])) / 1000,
                    float(re.sub(r'[^\d.]+', '', random_recipe['Calcium'])) / 1000,
                    float(re.sub(r'[^\d.]+', '', random_recipe['Iron'])) / 1000,
                    float(re.sub(r'[^\d.]+', '', random_recipe['Potassium'])) / 1000
                ]
                # Create a list of daily values (DV) for each nutrient based on a 2000 calorie per day diet, all are in grams
                dv = [65, 20, 0.3, 2.3, 300, 28, 50, 50, 0.09, 1, 0.018, 4.7]

                # Calculate the percentage of DV for each nutrient
                dv_percent = [round(value * 100 / dv[i]) for i, value in enumerate(values)]                
                nutrition_html = """
                <div id="nutrition-info_6-0" class="comp nutrition-info">
                    <table class="nutrition-info__table">
                        <thead>
                            <tr>
                                <th class="nutrition-info__heading" colspan="3">Number of Servings: <span class="nutrition-info__heading-aside">{servings}</span></th>
                            </tr>                            
                        </thead>
                        <tbody class="nutrition-info__table--body">
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Calories</td>
                                <td class="nutrition-info__table--cell">{calories}</td>
                                <td class="nutrition-info__table--cell"></td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Total Fat</td>
                                <td class="nutrition-info__table--cell">{total_fat}</td>
                                <td class="nutrition-info__table--cell">{fat_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Saturated Fat</td>
                                <td class="nutrition-info__table--cell">{saturated_fat}</td>
                                <td class="nutrition-info__table--cell">{sat_fat_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Cholesterol</td>
                                <td class="nutrition-info__table--cell">{cholesterol}</td>
                                <td class="nutrition-info__table--cell">{chol_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Sodium</td>
                                <td class="nutrition-info__table--cell">{sodium}</td>
                                <td class="nutrition-info__table--cell">{sodium_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Total Carbohydrate</td>
                                <td class="nutrition-info__table--cell">{total_carbohydrate}</td>
                                <td class="nutrition-info__table--cell">{carb_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Dietary Fiber</td>
                                <td class="nutrition-info__table--cell">{dietary_fiber}</td>
                                <td class="nutrition-info__table--cell">{diet_fibe_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Total Sugars</td>
                                <td class="nutrition-info__table--cell">{total_sugars}</td>
                                <td class="nutrition-info__table--cell">{tot_sugars_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Protein</td>
                                <td class="nutrition-info__table--cell">{protein}</td>
                                <td class="nutrition-info__table--cell">{protein_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Vitamin C</td>
                                <td class="nutrition-info__table--cell">{vitc}</td>
                                <td class="nutrition-info__table--cell">{vitc_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Calcium</td>
                                <td class="nutrition-info__table--cell">{calc}</td>
                                <td class="nutrition-info__table--cell">{calc_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Iron</td>
                                <td class="nutrition-info__table--cell">{iron}</td>
                                <td class="nutrition-info__table--cell">{iron_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Potassium</td>
                                <td class="nutrition-info__table--cell">{pota}</td>
                                <td class="nutrition-info__table--cell">{pota_percent}% DV</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                """
                # Use the nutrition HTML and format it with the values
                formatted_html = nutrition_html.format(
                    calories=random_recipe['Calories'],
                    total_fat=random_recipe['Total Fat'],
                    saturated_fat=random_recipe['Saturated Fat'],
                    cholesterol=random_recipe['Cholesterol'],
                    sodium=random_recipe['Sodium'],
                    total_carbohydrate=random_recipe['Total Carbohydrate'],
                    dietary_fiber=random_recipe['Dietary Fiber'],
                    total_sugars=random_recipe['Total Sugars'],
                    servings=random_recipe['Number of Servings'],
                    vitc=random_recipe['Vitamin C'],
                    calc=random_recipe['Calcium'],
                    iron=random_recipe['Iron'],
                    pota=random_recipe['Potassium'],
                    protein=random_recipe['Protein'],
                    fat_percent=dv_percent[0],
                    sat_fat_percent=dv_percent[1],
                    chol_percent=dv_percent[2],
                    sodium_percent=dv_percent[3],
                    carb_percent=dv_percent[4],
                    diet_fibe_percent=dv_percent[5],
                    tot_sugars_percent=dv_percent[6],
                    protein_percent=dv_percent[7],
                    vitc_percent=dv_percent[8],
                    calc_percent=dv_percent[9],
                    iron_percent=dv_percent[10],
                    pota_percent=dv_percent[11]

                )

                # Define a function to apply the CSS styles to the table cells
                def format_table(val):
                    return f"background-color: #133350; color: #fff; border: 1px solid #ddd; border-radius: .25rem; padding: .625rem .625rem 0; font-family: Helvetica; font-size: 1rem;"
                
                with st.container():
                    # Add the nutrition table to the Streamlit app
                    st.write("<h2 style='text-align:left;'>Nutrition Facts (per serving)</h2>", unsafe_allow_html=True)
                    st.write(f"<div style='max-height:none; overflow:auto'>{formatted_html}</div>", unsafe_allow_html=True)  
                    st.write("<p style='text-align:left;'>*The % Daily Value (DV) tells you how much a nutrient in a food serving contributes to a daily diet. 2,000 calories a day is used for general nutrition advice.</p>", unsafe_allow_html=True)                
                # create pie chart
                labels = ['Total Fat', 'Saturated Fat', 'Cholesterol', 'Sodium', 'Total Carbohydrate', 'Dietary Fiber', 'Total Sugars', 'Protein', 'Vitamin C', 'Calcium', 'Iron', 'Potassium']
                fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                st.markdown("### Macronutrients Pie Chart ;) (In Grams)")
                st.plotly_chart(fig)  
                st.write("**Tags:** ", random_recipe['Tags'])
                st.write("**Recipe URL:** ", random_recipe['Recipe URLs'])     
                st.write("*To download this recipe as a PDF, open the hamburger menu on the top right and click on Print.*")              
                st.markdown("### JSON Response:")
                st.write(response_json) 
                    
            else:
                st.markdown("### Recommended Recipe:")
                st.write("**Title:** ", response_json[0]['Title'])
                if response_json[0]['Image Link'].endswith(".jpg") or response_json[0]['Image Link'].endswith(".jpeg") or response_json[0]['Image Link'].endswith(".png"):
                    st.image(response_json[0]['Image Link'], width=300)
                else:
                    st.write("**Image Link:** ", response_json[0]['Image Link'])
                st.write("**Rating:** ", response_json[0]['Rating'])
                if response_json[0]['Description'] != "Description not found":
                    st.write("**Description:** ", response_json[0]['Description'])
                st.write("**Ingredients:**<br>", response_json[0]['Ingredients'].replace('\n', '<br>'), unsafe_allow_html=True)
                st.write("**Recipe Facts:**<br>", response_json[0]['Recipe Facts'].replace('\n', '<br>'), unsafe_allow_html=True)
                st.write("**Directions:**<br>", response_json[0]['Directions'].replace('\n', '<br>'), unsafe_allow_html=True) 
                # extract only numeric values and convert mg to g
                values = [
                    float(re.sub(r'[^\d.]+', '', response_json[0]['Total Fat'])), 
                    float(re.sub(r'[^\d.]+', '', response_json[0]['Saturated Fat'])), 
                    float(re.sub(r'[^\d.]+', '', response_json[0]['Cholesterol'])) / 1000, 
                    float(re.sub(r'[^\d.]+', '', response_json[0]['Sodium'])) / 1000, 
                    float(re.sub(r'[^\d.]+', '', response_json[0]['Total Carbohydrate'])), 
                    float(re.sub(r'[^\d.]+', '', response_json[0]['Dietary Fiber'])), 
                    float(re.sub(r'[^\d.]+', '', response_json[0]['Total Sugars'])), 
                    float(re.sub(r'[^\d.]+', '', response_json[0]['Protein'])),
                    float(re.sub(r'[^\d.]+', '', response_json[0]['Vitamin C'])) / 1000,
                    float(re.sub(r'[^\d.]+', '', response_json[0]['Calcium'])) / 1000,
                    float(re.sub(r'[^\d.]+', '', response_json[0]['Iron'])) / 1000,
                    float(re.sub(r'[^\d.]+', '', response_json[0]['Potassium'])) / 1000
                ]
                # Create a list of daily values (DV) for each nutrient based on a 2000 calorie per day diet, all are in grams
                dv = [65, 20, 0.3, 2.3, 300, 28, 50, 50, 0.09, 1, 0.018, 4.7]

                # Calculate the percentage of DV for each nutrient
                dv_percent = [round(value * 100 / dv[i]) for i, value in enumerate(values)]                
                nutrition_html = """
                <div id="nutrition-info_6-0" class="comp nutrition-info">
                    <table class="nutrition-info__table">
                        <thead>
                            <tr>
                                <th class="nutrition-info__heading" colspan="3">Number of Servings: <span class="nutrition-info__heading-aside">{servings}</span></th>
                            </tr>                            
                        </thead>
                        <tbody class="nutrition-info__table--body">
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Calories</td>
                                <td class="nutrition-info__table--cell">{calories}</td>
                                <td class="nutrition-info__table--cell"></td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Total Fat</td>
                                <td class="nutrition-info__table--cell">{total_fat}</td>
                                <td class="nutrition-info__table--cell">{fat_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Saturated Fat</td>
                                <td class="nutrition-info__table--cell">{saturated_fat}</td>
                                <td class="nutrition-info__table--cell">{sat_fat_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Cholesterol</td>
                                <td class="nutrition-info__table--cell">{cholesterol}</td>
                                <td class="nutrition-info__table--cell">{chol_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Sodium</td>
                                <td class="nutrition-info__table--cell">{sodium}</td>
                                <td class="nutrition-info__table--cell">{sodium_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Total Carbohydrate</td>
                                <td class="nutrition-info__table--cell">{total_carbohydrate}</td>
                                <td class="nutrition-info__table--cell">{carb_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Dietary Fiber</td>
                                <td class="nutrition-info__table--cell">{dietary_fiber}</td>
                                <td class="nutrition-info__table--cell">{diet_fibe_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Total Sugars</td>
                                <td class="nutrition-info__table--cell">{total_sugars}</td>
                                <td class="nutrition-info__table--cell">{tot_sugars_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Protein</td>
                                <td class="nutrition-info__table--cell">{protein}</td>
                                <td class="nutrition-info__table--cell">{protein_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Vitamin C</td>
                                <td class="nutrition-info__table--cell">{vitc}</td>
                                <td class="nutrition-info__table--cell">{vitc_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Calcium</td>
                                <td class="nutrition-info__table--cell">{calc}</td>
                                <td class="nutrition-info__table--cell">{calc_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Iron</td>
                                <td class="nutrition-info__table--cell">{iron}</td>
                                <td class="nutrition-info__table--cell">{iron_percent}% DV</td>
                            </tr>
                            <tr class="nutrition-info__table--row">
                                <td class="nutrition-info__table--cell">Potassium</td>
                                <td class="nutrition-info__table--cell">{pota}</td>
                                <td class="nutrition-info__table--cell">{pota_percent}% DV</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                """
                # Use the nutrition HTML and format it with the values
                formatted_html = nutrition_html.format(
                    calories=response_json[0]['Calories'],
                    total_fat=response_json[0]['Total Fat'],
                    saturated_fat=response_json[0]['Saturated Fat'],
                    cholesterol=response_json[0]['Cholesterol'],
                    sodium=response_json[0]['Sodium'],
                    total_carbohydrate=response_json[0]['Total Carbohydrate'],
                    dietary_fiber=response_json[0]['Dietary Fiber'],
                    total_sugars=response_json[0]['Total Sugars'],
                    servings=response_json[0]['Number of Servings'],
                    vitc=response_json[0]['Vitamin C'],
                    calc=response_json[0]['Calcium'],
                    iron=response_json[0]['Iron'],
                    pota=response_json[0]['Potassium'],
                    protein=response_json[0]['Protein'],
                    fat_percent=dv_percent[0],
                    sat_fat_percent=dv_percent[1],
                    chol_percent=dv_percent[2],
                    sodium_percent=dv_percent[3],
                    carb_percent=dv_percent[4],
                    diet_fibe_percent=dv_percent[5],
                    tot_sugars_percent=dv_percent[6],
                    protein_percent=dv_percent[7],
                    vitc_percent=dv_percent[8],
                    calc_percent=dv_percent[9],
                    iron_percent=dv_percent[10],
                    pota_percent=dv_percent[11]

                )

                # Define a function to apply the CSS styles to the table cells
                def format_table(val):
                    return f"background-color: #133350; color: #fff; border: 1px solid #ddd; border-radius: .25rem; padding: .625rem .625rem 0; font-family: Helvetica; font-size: 1rem;"
                
                with st.container():
                    # Add the nutrition table to the Streamlit app
                    st.write("<h2 style='text-align:left;'>Nutrition Facts (per serving)</h2>", unsafe_allow_html=True)
                    st.write(f"<div style='max-height:none; overflow:auto'>{formatted_html}</div>", unsafe_allow_html=True)  
                    st.write("<p style='text-align:left;'>*The % Daily Value (DV) tells you how much a nutrient in a food serving contributes to a daily diet. 2,000 calories a day is used for general nutrition advice.</p>", unsafe_allow_html=True)                
                # create pie chart
                labels = ['Total Fat', 'Saturated Fat', 'Cholesterol', 'Sodium', 'Total Carbohydrate', 'Dietary Fiber', 'Total Sugars', 'Protein', 'Vitamin C', 'Calcium', 'Iron', 'Potassium']
                fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                st.markdown("### Macronutrients Pie Chart ;) (In Grams)")
                st.plotly_chart(fig)  
                st.write("**Tags:** ", response_json[0]['Tags'])
                st.write("**Recipe URL:** ", response_json[0]['Recipe URLs'])  
                st.write("*To download this recipe as a PDF, open the hamburger menu on the top right and click on Print.*")                  
                st.markdown("### JSON Response:")
                st.write(response_json)      

        st.markdown("<hr style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center'><a href='https://github.com/Kaludii'>Github</a> | <a href='https://huggingface.co/Kaludi'>HuggingFace</a></p>", unsafe_allow_html=True)        

if __name__ == '__main__':
    main()
