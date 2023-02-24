# Are you a food lover always looking for new recipe ideas?

This app uses a Food Category Image Classifier model that has been trained to recognize 12 different categories of foods: Bread, Dairy, Dessert, Egg, Fried Food, Fruit, Meat, Noodles, Rice, Seafood, Soup, and Vegetable. After classifying the category, it provides personalized recipe recommendations based on user preferences for diet and cuisine. With its easy-to-use interface and integration with recipe databases, the app is perfect for food lovers looking for personalized recipe suggestions.

# Web App
Click [Here](https://huggingface.co/spaces/Kaludi/Food-Category-Classification-And-Recipes-Recommender_App "Here") To View This App Online!

![Image](https://user-images.githubusercontent.com/63890666/220527352-d0c91d29-e0de-4e0d-9b68-dfaa00b4b6e4.png)

# Architecture

![Project 3 (2)](https://user-images.githubusercontent.com/111074755/220503596-36f2d9b6-4459-4c22-a037-fea40a98c855.png)

## Web Scraping:

The website used is https://www.seriouseats.com/, and the data obtained for each recipe is as follows:

- Name of Recipe
- Rating (out of 5)
- Description
- Ingredients 
- Recipe Facts
- Directions
- Number of Servings 
- Nutrition Label
- Images of the Recipes 
- Descriptive Tags

## Image Scraping:

Scraped the images of the 12 food categories for the image classification model using a software called Bulk Image Downloader from Google Images

![Blank diagram (1)](https://user-images.githubusercontent.com/111074755/220501181-f60d9cab-5932-4c8d-b7fe-7e5eafbe3c4d.png)

## Transformation

- Data cleaning and formatting was done in Python using Pandas.
- The AI was then trained with food images from Google.
- 1500 total images were downloaded across the 12 different categories.
- 80% of the images were used for training and the other 20% were used for testing/validation.

## Loading

Cloud storage with AWS S3 bucket stored a json file of our recipe dataset.

## The Backend

AWS Lambda and AWS API Gateway were used to interact with the frontend according to user input in the front end.

## The User Interface

- Streamlit was used for the user interface, which included everything from the diet and cuisine dropdown menus to working with the fine-tuned image classifier model.

## Interface Hosting

Hugging Face Spaces was used to host our final trained model as well as our web interface code.

## Image Classification Model Metrics

| Metric             | Score |
| ------------------ | ----- |
| Accuracy           | 96%   |
| Loss               | 0.1443|
| Precision_macro    | 0.9621|
| Precision_micro    | 0.96  |
| Precision_weighted | 0.9621|
| Recall_macro       | 0.96  |
| Recall_micro       | 0.96  |
| Recall_weighted    | 0.96  |
| F1_macro           | 0.9595|
| F1_micro           | 0.96  |
| F1_weighted        | 0.9595|

## Usage

To use our app, simply click on [this link](https://huggingface.co/spaces/Kaludi/Food-Category-Classification-And-Recipes-Recommender_App) to access the web app. Once you're on the app, select your preferences for diet and cuisine from the dropdown menus, and click the "Get Recipe" button. Our image classification model will identify the food category and provide personalized recipe recommendations based on your preferences. You can also view recipe details, ratings, nutrition facts, and more.

## Requirements

-   Python 3.6 or higher
-   Streamlit
-   Requests
-   plotly

## Installation (To Run Locally)

1.  Clone the repository:

`git clone https://github.com/NebulaCrasher/curated-cuisine-coalition.git` 

2.  Install the required packages:

`pip install streamlit requests` 

3.  Run the app:

`streamlit run Classification_And_Recipes.py`

# We hope you enjoy using our app and discover new recipes that you love!
