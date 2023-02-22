# Are you a food lover always looking for new recipe ideas?

This app uses a Food Category Image Classifier model that has been trained by to recognize 12 different categories of foods, which includes Bread, Dairy, Dessert, Egg, Fried Food, Fruit, Meat, Noodles, Rice, Seafood, Soup, and Vegetable. After classifying the category, it provides a personalized recipe recommendations based on user preferences for diet and cuisine. With its easy-to-use interface and integration with recipe databases, the app is perfect for food lovers looking for personalized recipe suggestions.

# Web App
Click [Here](https://huggingface.co/spaces/Kaludi/Food-Category-Classification-And-Recipes-Recommender_App "Here") To View This App Online!

![Image](https://user-images.githubusercontent.com/63890666/220527352-d0c91d29-e0de-4e0d-9b68-dfaa00b4b6e4.png)

# Architecture

![Project 3 (2)](https://user-images.githubusercontent.com/111074755/220503596-36f2d9b6-4459-4c22-a037-fea40a98c855.png)

## Web Scraping:

The website used is https://www.seriouseats.com/, and the data obtained as follows:

- The name of the recipe
- Ratings
- Descriptions
- Ingredients 
- Recipe facts
- Directions
- Number of serving 
- Nutrition 
- Images of the recipes 
- Tags to categized food 

## Image Scraping:

Scraped the images of 12 popular food categories for the image classification model using a software called Bulk Image Downloader from Google Images

![Blank diagram (1)](https://user-images.githubusercontent.com/111074755/220501181-f60d9cab-5932-4c8d-b7fe-7e5eafbe3c4d.png)

## Tranformation

- Web scraped data cleaned and tranformed in Python using Pandas. 
- Training the food images scraped off Google 
- 1500 total images were downloaded for 12 different categories
- 80% of the images were used to train, and the other 20% were used to validate

## Loading

AWS S3 bucket was used to load the scraped data in JSON format

## The back end

AWS Lambda and AWS API Gateway were used to interact with the front end accroding to the users criteria in the front end.

## The user interface 

- Plotly was used to create a pychart for the recipe nutritions. For the recipe nutritions, they were all converted to grams. 
- Streamlit was used for the user interface UI, which included everything from the drop downs of the diet and cuisine to work with the fin tuned images classifier model

## Interface Hosting

Hugging Face Spaces was used to host our final trained model as well as our web interface code.


