import streamlit as st
from PIL import Image

from transformers import pipeline
import numpy as np
from transformers import AutoFeatureExtractor
from transformers import AutoModelForImageClassification

st.set_page_config(layout='wide',
                   page_title='Food Category Classification & Recipes'
                   )

# Setting up Sidebar
sidebar_acc = ['App Description', 'About Project']
sidebar_acc_nav = st.sidebar.radio('**INFORMATION SECTION**', sidebar_acc)

if sidebar_acc_nav == 'App Description':
    st.sidebar.markdown("<h2 style='text-align: center;'> Food Category Classification Description </h2> ", unsafe_allow_html=True)
    st.sidebar.markdown("This is a Food Category Image Classifier model that has been trained by [Kaludi](https://huggingface.co/Kaludi) to recognize **12** different categories of foods, which includes **Bread**, **Dairy**, **Dessert**, **Egg**, **Fried Food**, **Fruit**, **Meat**, **Noodles**, **Rice**, **Seafood**, **Soup**, and **Vegetable**. It can accurately classify an image of food into one of these categories by analyzing its visual features. This model can be used by food bloggers, restaurants, and recipe websites to quickly categorize and sort their food images, making it easier to manage their content and provide a better user experience.")

elif sidebar_acc_nav == 'About Project':
    st.sidebar.markdown("<h2 style='text-align: center;'> About Project </h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='text-align: center;'>", unsafe_allow_html=True)
    st.sidebar.markdown("<h3 style='text-align: center;'>Project Location:</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center;'><strong><a href='https://huggingface.co/Kaludi/food-category-classification-v2.0'>Model</a></strong>  |  <strong><a href='https://huggingface.co/datasets/Kaludi/food-category-classification-v2.0'>Dataset</a></strong></p>", unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='text-align: center;'>", unsafe_allow_html=True)
    st.sidebar.markdown("<h3 style='text-align: center;'>Project Creators:</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center;'><a href='https://github.com/Kaludii'><strong>AA</strong></a></p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center;'><a href='https://github.com/Kaludii'><strong>AM</strong></a></p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center;'><a href='https://github.com/Kaludii'><strong>BK</strong></a></p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center;'><a href='https://github.com/Kaludii'><strong>DK</strong></a></p>", unsafe_allow_html=True)
    

def main():
    st.title("Food Category Classification & Recipes")
     
    st.markdown("### Backgroud")  
    st.markdown("This is a Food Category Image Classifier model that has been trained by [Kaludi](https://huggingface.co/Kaludi) to recognize **12** different categories of foods, which includes **Bread**, **Dairy**, **Dessert**, **Egg**, **Fried Food**, **Fruit**, **Meat**, **Noodles**, **Rice**, **Seafood**, **Soup**, and **Vegetable**. It can accurately classify an image of food into one of these categories by analyzing its visual features. This model can be used by food bloggers, restaurants, and recipe websites to quickly categorize and sort their food images, making it easier to manage their content and provide a better user experience.")  
    st.header("Try it out!")

#    images = ["examples/example_0.jpg",
#                    "examples/example_1.jpg",
#                    "examples/example_2.jpg",
#                    "examples/example_3.jpg",
#                    "examples/example_4.jpg",
#                    "examples/example_5.jpg",
#                    "examples/example_6.jpg",
#                    "examples/example_7.jpg"]
#    show_images = False

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

    select_health = st.radio("Select One (Not Functional Yet):", ["Regular", "Low-Calorie"], horizontal=True)
    
    calories = st.slider("Select Max Calories (Per Serving)", 50, 2000)
    
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

    
        if select_health == "Regular":
            st.write("You Selected **_Regular_** With Max", calories, "Calories For", "**Bread**" if label_num==0 else "**Dairy**" if label_num==1 else "**Dessert**" if label_num==2 else "**Egg**" if label_num==3 else "**Fried Food**" if label_num==4 else "**Fruit**" if label_num==5 else "**Meat**" if label_num==6 else "**Noodles**" if label_num==7 else "**Rice**" if label_num==8 else "**Seafood**" if label_num==9 else "**Soup**" if label_num==10 else "**Vegetable**")
            # Add code to fetch healthy recipe here (line #125-138)
        elif select_health == "Low-Calorie":
            st.write("You Selected **_Low-Calorie_** With Max", calories, "Calories For", "**Bread**" if label_num==0 else "**Dairy**" if label_num==1 else "**Dessert**" if label_num==2 else "**Egg**" if label_num==3 else "**Fried Food**" if label_num==4 else "**Fruit**" if label_num==5 else "**Meat**" if label_num==6 else "**Noodles**" if label_num==7 else "**Rice**" if label_num==8 else "**Seafood**" if label_num==9 else "**Soup**" if label_num==10 else "**Vegetable**")
            # Add code to fetch unhealthy recipe here (line #125-138)

        st.image(img, width=260)
        st.markdown("<hr style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center'><a href='https://github.com/Kaludii'>Github</a> | <a href='https://huggingface.co/Kaludi'>HuggingFace</a></p>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()


## Fetch random recipes:
## Fetch the healthy recipe
#response = requests.get("test.org/test.json")
#data = response.json()
#healthy_recipes = [recipe for recipe in data['recipe'] if recipe['calories'] < int(calories)]
#healthy_recipe = random.choice(healthy_recipes)

## Fetch the unhealthy recipe
#unhealthy_recipes = [recipe for recipe in data['recipe'] if recipe['calories'] < int(calories)]
#unhealthy_recipe = random.choice(unhealthy_recipes)

## Add code to display the healthy and unhealthy recipes
#st.write("Healthy Recipe: ", healthy_recipe['name'], "Calories: ", healthy_recipe['calories'])
#st.write("Unhealthy Recipe: ", unhealthy_recipe['name'], "Calories: ", unhealthy_recipe['calories'])