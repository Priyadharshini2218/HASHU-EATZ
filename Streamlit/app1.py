#import libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import json
import matplotlib.patches as mpatches
from matplotlib import cm
from matplotlib.font_manager import FontProperties
import seaborn as sns

from plotly import graph_objs as go
from sklearn.linear_model import LinearRegression

from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

# adding title in streamlit
st.sidebar.markdown(f"<span style='color: black;font-size: 36px;font-weight: bold;'>Hashu Eatz🍲</span>", unsafe_allow_html=True)

st.sidebar.info("Welcome to Hashu Eatz 😋 Data Analytics. Here you can analyse the nutritional value of food and draw some schematics and get the right nutritive choice of recommandation as you like!")
""""""
#read csv file
DATA_URL = ("Streamlit/resources/assets_modified/01.csv")

DATA_URL2 = ("Streamlit/resources/recipe_page/recipe.csv")


#for data caching
#in streamlit the whole code is rerun everytime so cache would be stored and some error might occur in rare cases
@st.cache(persist=True)
#the above line is to clear the cache on every run command execution


#to load the csv file
def load_data():
    data = pd.read_csv(DATA_URL)
    return data

def load_data2():
    data2 = pd.read_csv(DATA_URL2)
    return data2


#to load the csv file and display it
data = load_data()
data2= load_data2()

#global variable/dataframe
#path to the csv file of the ifct database for demographics page
df_demographics = pd.read_csv("Streamlit/resources/assets_modified/01cat.csv")
df_demographics_nonveg= pd.read_csv("Streamlit/resources/assets_modified/02cat.csv")

#drop row/column if all values there are NA
df_demographics.dropna()


#the main function that is called first and foremost with the navigation options in the sidebar
def main():
    # Register your pages
    pages = {
        "About": about_page,
        "Ingredient Information": page_first,
        #"IFCT Demographics": demographic_main,
        #"Medical Condition Demographics":disease_demographics,
        "Search for Recipe": page_second,
        "Calorie Calculator": page_three,
        #"Heart Disease Map": page_fourth,
        "Food Matrix": page_five,
        "Food Recommendation System":page_six
        
    }


    st.sidebar.title("Navigation 🧭")
    # Widget to select your page, you can choose between radio buttons or a selectbox
    page = st.sidebar.radio("(Choose an option to get redirected)", tuple(pages.keys()))
    
    # Display the selected page
    pages[page]()

    

#function for the about page
def about_page():
    st.markdown("<h1 style='text-align: center;'>Hashu Eatz 🍲 🩺</h1>", unsafe_allow_html=True)
    st.image("Streamlit/resources/foood.jpg")
    st.subheader("About Hashu Eatz 🤔")

    

    #all the necessary descriptions
    st.markdown("<h6 style='text-align: justify;font-size:110%;font-family:Arial, sans-serif;line-height: 1.5;'>Food is an essential parameter that plays an important role in the survival of humans. It also plays a major part in depicting a country’s culture. Healthy, nutritious, and high-quality food results in not only a better lifestyle but also develops a person’s immunity and health. Likewise, the consumption of low-quality food which might be deprived of nutritional value impacts a person’s health negatively and makes them susceptible to all types of diseases.  Making sound nourishment choices whereas being a foodie does not come that simple. The present generation of people is very conscious of their food in order to recover from diseases or to avoid upcoming diseases. The stressed and busy life of people causes unable to keep track of the proper food diet, which increases the significance of proper food classification and information about that. In other words, what you wish may be a great nourishment tracker and recommend the best nutrition that helps an individual. Although being healthy and eating better is something the vast majority of the population wants, doing so usually requires great effort and organization. Hashu Eatz performs a complete analysis of the nutritional composition of food item you wish and also gives an amazing recommendation according to your preference.</h6>"
    , unsafe_allow_html=True)
    st.markdown("")
    
    
   
    #this function works on streamlit==0.71.0
    #background image for the webapp
    page_bg_img = '''
    <style>
    body {
    background-image: url("https://cutewallpaper.org/21/website-background-wallpaper/Geometric-abstract-grey-background-for-bussines-templates-.jpg");
    background-size: cover;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

#first page function
def page_first():
    
    st.title("Ingredient Information 🍅 🥕 🥒 ")

    st.markdown("<h6 style='text-align: justify;font-size:100%;font-family:Arial,sans-serif;line-height: 1.2;'>In order to ensure proper development and growth of the body, immunity against diseases, and energy to function throughout the day, it is necessary to consume adequate amounts of all nutrients, including proteins, carbohydrates, fats, vitamins, minerals and water. Therefore, the nutritional value of any food item being consumed is a very important parameter. The content of different nutrients in various foods, consumed either individually or as ingredients in dishes can be found here.</h6>",unsafe_allow_html=True)

    
    food_list = st.selectbox("Search your ingredient here:", data["name"].unique())


    st.markdown(f"<span style='color: #000080;font-size: 24px;font-weight: bold;'>Filter Data Results are :</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: black;font-size: 22px;font-weight: bold;'>You selected- {food_list}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: black;font-size: 22px;font-weight: bold;'>Nutritional Analysis for your selection is as follows-</span>", unsafe_allow_html=True)

    #counts of various nutritional contents of a food item
    count_water = data.loc[(data["name"] == food_list) , 'water'].iloc[0]
    count_protein = data.loc[(data["name"] == food_list) , 'protcnt'].iloc[0]
    count_ash = data.loc[(data["name"] == food_list) , 'ash'].iloc[0]
    count_fat = data.loc[(data["name"] == food_list) , 'fatce'].iloc[0]
    count_fibretotal = data.loc[(data["name"] == food_list) , 'fibtg'].iloc[0]
    count_fibreinsoluble = data.loc[(data["name"] == food_list) , 'fibins'].iloc[0]
    count_fibresoluble = data.loc[(data["name"] == food_list) , 'fibsol'].iloc[0]
    count_carbohydrate = data.loc[(data["name"] == food_list) , 'choavldf'].iloc[0]
    count_energy = data.loc[(data["name"] == food_list) , 'enerc'].iloc[0]

    #displaying the corresponding values to the above parameters
    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Water- {count_water}g</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Protein- {count_protein}g</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Ash- {count_ash}g</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Fat- {count_fat}g</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Total Fibre- {count_fibretotal}g</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Insoluble Fibre- {count_fibreinsoluble}g</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Soluble Fibre- {count_fibresoluble}g</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Carbohydrates- {count_carbohydrate}g</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Energy- {count_energy}kJ</span>", unsafe_allow_html=True)
    
   
def page_second():

    #sidebar title
    st.title("Search for a Recipe 😋")
    st.markdown("<h6 style='text-align: justify;font-size:100%;font-family:Arial,sans-serif;line-height: 1.3;'>All recipes require a variety of ingredients, such as vegetables, flour, spices and milk products. Here, you can search the possible dishes with any desired combination of ingredients. You can also view the calories in the dish and the cuisine. Please enter a minimum of two ingredients to search for dishes.</h6>",unsafe_allow_html=True)
    st.markdown("")

    #st.markdown(f"<span style='color: #000080;font-size: 24px;font-weight: bold;'>Dataset Preview 📋</span>", unsafe_allow_html=True)
    #data2

    #default value is NA for the choice
    all_ingredients1 = ["NA"]
    gg = data2.loc[:, data2.columns != 'Name of Dish'].values.tolist()

    #printed a list first in streamlit of the unique values in the particular choice and then copied it to give the options here
    ingredient_1 = st.selectbox('Search for 1st Ingredient',([
    "NA",
    "Potato",
    "Tomato",
    "Cilantro(Coriander leaves)",
    "Brinjal",
    "Carrot",
    "Coriander",
    "Onion",
    "Drumsticks",
    "Capsicum",
    "None",
    "Cabbage",
    "Peas",
    "Fenugreek",
    "Mushrooms",
    "Spinach",
    "Olives",
    "Sweet corn",
    "Kidney beans(Rajma)",
    "Zucchini",
    "Cauliflower",
    "Bitter Gourd",
    "Cucumber",
    "Beetroot",
    "Garlic",
    "Pumpkin",
    "Beans",
    "Green chilli",
    "Broccoli",
    "Bottle Gourd",
    "Sweet potato",
    "Baby corn",
    "Cluster Beans(Gavar)",
    "Colocasia",
    "Radish",
    "Turnip",
    "Ladyfinger(Okra)",
    "Celery",
    "Soyabean",
    "Mint",
    "Ginger",
    "Black Beans",
    "Lemon juice",
    "Lettuce",
    "Spring Onion",
    "Fennel Bulbs",
    "White Beans",
    "Asparagus",
    "Jalapenos",
    "Leek",
    "Brussels Sprouts",
    "Artichoke",
    "Curry leaves",
    "Ivy Gourd (Tendli)",
    "Yam"
    ]))
    st.write('You selected:', ingredient_1)

    #printed a list first in streamlit of the unique values in the particular choice and then copied it to give the options here
    ingredient_2 = st.selectbox('Search for 2nd Ingredient',([
    "NA",
    "Tomato",
    "Beans",
    "Garlic",
    "Onion",
    "Peas",
    "Capsicum",
    "Baby corn",
    "Carrot",
    "Curry leaves",
    "Coriander",
    "Potato",
    "None",
    "Bottle Gourd",
    "Cabbage",
    "Mint",
    "Jalapenos",
    "Brinjal",
    "Cucumber",
    "Cauliflower",
    "Ginger",
    "Olives",
    "Fenugreek",
    "Green chilli",
    "Spinach",
    "Sweet corn",
    "Lemon juice",
    "Cilantro(Coriander leaves)",
    "Beetroot",
    "Spring Onion",
    "Mustard Greens",
    "Mushrooms",
    "Leek",
    "Fennel Bulbs",
    "Broccoli",
    "Celery",
    "White Beans",
    "Turnip"
    ]))
    st.write('You selected:', ingredient_2)


    #printed a list first in streamlit of the unique values in the particular choice and then copied it to give the options here
    ingredient_3 = st.selectbox('Search for 3rd Ingredient',([
    "NA",
    "Onion",
    "Carrot",
    "Mushrooms",
    "Garlic",
    "Pickles",
    "Cabbage",
    "Capsicum",
    "Ginger",
    "Green chilli",
    "Olives",
    "None",
    "Cauliflower",
    "Coriander",
    "Tomato",
    "Pumpkin",
    "Potato",
    "Jalapenos",
    "Curry leaves",
    "Peas",
    "Fenugreek",
    "Beetroot",
    "Sweet corn",
    "Celery",
    "Lemon juice",
    "Cilantro(Coriander leaves)",
    "Lettuce",
    "Kidney beans(Rajma)",
    "Spring Onion",
    "Mint",
    "Spinach",
    "Artichoke"
    ]))
    st.write('You selected:', ingredient_3)

    ingredient_4 = st.selectbox('Search for 4th Ingredient',([
    "NA",
    "Peas",
    "None",
    "Olives",
    "Lemon juice",
    "Tomato",
    "Green chilli",
    "Jalapenos",
    "Garlic",
    "Capsicum",
    "Beetroot",
    "Ladyfinger(Okra)",
    "Sweet corn",
    "Beans",
    "Coriander",
    "Onion",
    "Ginger",
    "Cauliflower",
    "Mushrooms",
    "Baby corn",
    "Curry leaves",
    "Cabbage",
    "Carrot",
    "Pickles",
    "Kidney beans(Rajma)",
    "Celery",
    "Mint",
    "Potato",
    "White Beans",
    "Cilantro(Coriander leaves)",
    "Broccoli",
    "Spring Onion",
    "Spinach",
    "Soyabean",
    "Radish"
    ]))
    st.write('You selected:', ingredient_4)

    ingredient_5 = st.selectbox('Search for 5th Ingredient',([
    "NA",
    "Moong dal",
    "Whole wheat flour(Atta)",
    "White flour(Maida)",
    "Chickpeas(Chhole)",
    "Rice",
    "Masoor dal",
    "None",
    "Gram(Chana)",
    "Toor dal",
    "Gram flour(Besan)",
    "Urad dal",
    "Chana dal",
    "Oats",
    "Corn flour",
    "Bajra(Millet Flour)",
    "Sabudana",
    "Jowar Flour",
    "Rice Flour",
    "Rawa(Semolina)"
    ]))
    st.write('You selected:', ingredient_5)

    ingredient_6 = st.selectbox('Search for 6th Ingredient',([
    "NA",
    "Red Chilli",
    "Garam Masala",
    "Black Pepper",
    "Turmeric",
    "Cumin",
    "Oregano",
    "Cardamom",
    "None",
    "Mustard",
    "Cinnamon",
    "Bay leaves",
    "Parsley",
    "Garlic Cloves",
    "Basil",
    "Coriander seeds",
    "Thyme",
    "Dill",
    "Onion",
    "Fennel seeds",
    "Coriander",
    "Green Chilli",
    "Asafoetida",
    "Ginger",
    "Vanilla",
    "Rosemary",
    "Sesame seeds",
    "Flax Seeds",
    "Saffron",
    "Quinoa",
    "Nigella Seeds",
    "Nutmeg"
    ]))
    st.write('You selected:', ingredient_6)

    ingredient_7 = st.selectbox('Search for 7th Ingredient',([
    "NA",
    "Turmeric",
    "Paprika",
    "Black Pepper",
    "Cumin",
    "Cinnamon",
    "Garam Masala",
    "Red Chilli",
    "Oregano",
    "Asafoetida",
    "None",
    "Mustard",
    "Nutmeg",
    "Cardamom",
    "Bay leaves",
    "Garlic Cloves",
    "Fennel seeds",
    "Cloves",
    "Basil",
    "Parsley",
    "Onion",
    "Dill",
    "Green Chilli",
    "Coriander",
    "Sesame seeds",
    "Fenugreek seeds",
    "Ginger",
    "Poppy seeds",
    "Thyme",
    "Cayenne Peppers",
    "Sunflower Seeds",
    "Rosemary"
    ]))
    st.write('You selected:', ingredient_7)

    ingredient_8 = st.selectbox('Search for 8th Ingredient',([
    "NA",
    "Asafoetida",
    "None",
    "Oregano",
    "Coriander seeds",
    "Nutmeg",
    "Cinnamon",
    "Fennel seeds",
    "Turmeric",
    "Black Pepper",
    "Garam Masala",
    "Red Chilli",
    "Cumin",
    "Mustard",
    "Saffron",
    "Cloves",
    "Onion",
    "Bay leaves",
    "Paprika",
    "Parsley",
    "Garlic Cloves",
    "Basil",
    "Coriander",
    "Green Chilli",
    "Thyme",
    "Sesame seeds",
    "Dill",
    "Cardamom",
    "Ginger",
    "Kasoori Methi",
    "Flax Seeds",
    "Rosemary",
    "Fenugreek seeds",
    "Sunflower Seeds"
    ]))
    st.write('You selected:', ingredient_8)

    ingredient_9 = st.selectbox('Search for 9th Ingredient',([
    "NA",
    "Garam Masala",
    "None",
    "Parsley",
    "Saffron",
    "Turmeric",
    "Bay leaves",
    "Oregano",
    "Mustard",
    "Cardamom",
    "Black Pepper",
    "Coriander seeds",
    "Red Chilli",
    "Fenugreek seeds",
    "Poppy seeds",
    "Cloves",
    "Cumin",
    "Cinnamon",
    "Asafoetida",
    "Basil",
    "Green Chilli",
    "Thyme",
    "Coriander",
    "Cayenne Peppers",
    "Fennel seeds",
    "Onion",
    "Garlic Cloves",
    "Sesame seeds",
    "Kasoori Methi",
    "Dill",
    "Sunflower Seeds",
    "Flax Seeds"
    ]))
    st.write('You selected:', ingredient_9)

    #printed a list first in streamlit of the unique values in the particular choice and then copied it to give the options here
    ingredient_10 = st.selectbox('Search for 10th Ingredient',([
    "NA",
    "White Bread",
    "None",
    "Pita Bread",
    "Whole Wheat Bread",
    "Baguette",
    "Bun",
    "Papad",
    "French Bread"
    ]))
    st.write('You selected:', ingredient_10)

    


    ingredient_list = [ingredient_1,ingredient_2,ingredient_3,ingredient_4,ingredient_5,ingredient_6,ingredient_7,ingredient_8,ingredient_9,ingredient_10]

    #Remove NA keyword from list
    ingredient_list = set(filter(lambda x: x != 'NA', ingredient_list))
    ingredient_list = list(ingredient_list)

    #get all recipe names
    all_recipes = list(x for x in data2['Name of Dish'])

    #compare ingredients
    def intersection(list1,list2):
        list3 = [value for value in list2 if value in list1]
        return list3

    score = [0]*len(gg)
    for i in range(len(gg)):
        score[i] = len(intersection(gg[i],ingredient_list))

    max_score = max(score) if max(score) > 1 or len(ingredient_list)==1 else -999

    #find the best match
    most_prob = [all_recipes[x] for x in range(len(score)) if score[x] == max_score]
    recipe = []

    #join results with ,
    recipe = ", ".join(most_prob)
    
    st.markdown(f"<span style='color: black;font-size: 22px;font-weight: bold;'>Possible Dishes ⬇️ </span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #000080;font-size: 22px;font-weight: bold;'>{recipe}</span>", unsafe_allow_html=True)
    

    st.title("View calories and cuisine of a dish 🥗 🧑🏾‍🤝‍🧑🏼")

    #take user input to select the dish from the name column (used unique function for non repetition of values)
    dish_name = st.selectbox("Search your dish here:", data2["Name of Dish"].unique())


    st.markdown(f"<span style='color: #000080;font-size: 24px;font-weight: bold;'>Filter Data Results are :</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: black;font-size: 22px;font-weight: bold;'>You selected- {dish_name}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: black;font-size: 22px;font-weight: bold;'>Analysis for your selection is as follows-</span>", unsafe_allow_html=True)

    #counts of various nutritional contents of a food item
    count_calories = data2.loc[(data2["Name of Dish"] == dish_name) , 'Calories'].iloc[0]
    cuisine = data2.loc[(data2["Name of Dish"] == dish_name) , 'Cuisine'].iloc[0]
    
    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Calorie Count - {count_calories} kCal</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Cuisine - {cuisine}</span>", unsafe_allow_html=True)
  
#clorie calculator function
def page_three():
    st.title("Calorie Calculator 🍲 🧮")
    
    st.markdown("<h6 style='text-align: justify;font-size:100%;font-family:Arial,sans-serif;line-height: 1.3;'>Nutrients are classified into two categories, macronutrients and micronutrients. Macronutrients are those nutrients which are required in large quantities, and include carbohydrates, proteins, fats and water. Micronutrients are those which are required in relatively small quantities, and include vitamins and minerals. Adequate amounts of these nutrients are required to maintain good health. The adequate amounts vary from person to person, and also depend on the person’s daily calorie consumption. Moreover, the ideal calorie consumption for a person also depends on various factors, including gender. Here, you can find your ideal consumption of various nutrients depending on your daily calorie consumption, and can also find your ideal daily calorie consumption based on your gender.</h6>",unsafe_allow_html=True)
    st.markdown("")

    st.markdown(f"<span style='color: #000080;font-size: 24px;font-weight: bold;'>Add your total daily intake of calories</span>", unsafe_allow_html=True)

    #slider for user input
    x = st.slider('(in terms of Calories)',0,3000)

    #the generalised ideal percentages considered from various data sources
    fat_value= x*(30/100)
    sat_fat_value= x*(7/100)
    trans_fat_value= x*(1/100)
    total_carbs_value= x*(50/100)
    protein_value= x*(20/100)

    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Total Fat count should be- {fat_value} Cal</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Saturated Fat count should be- {sat_fat_value} Cal</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Trans Fat count should be- {trans_fat_value} Cal</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Total Carbohydrates count should be- {total_carbs_value} Cal</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color: #367588;font-size: 22px;font-weight: bold;'>Protein count should be- {protein_value} Cal</span>", unsafe_allow_html=True)


    st.markdown(f"<span style='color: #000080;font-size: 24px;font-weight: bold;'>Want to know your ideal calorie intake ??</span>", unsafe_allow_html=True)

    st.markdown(f"<span style='color: black;font-size: 20px;font-weight: bold;'>Choose your gender ⚥</span>", unsafe_allow_html=True)
    gender = st.selectbox('*Your calorie intake depends on your gender',('Male', 'Female', 'Other','Rather Not Say'))

    #display selected choice
    st.markdown(f"<span style='color: black;font-size: 20px;font-weight: bold;'>You selected: {gender}</span>", unsafe_allow_html=True)

    #if else use for all the possible variations - hard coded because choice are very few 
    if (gender == 'Male'):
        st.markdown(f"<span style='color: #367588;font-size: 19px;font-weight: bold;'>Your ideal daily calorie intake should be 2500 Cal</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color: #367588;font-size: 19px;font-weight: bold;'>Your ideal daily water intake should be 3.7 L</span>", unsafe_allow_html=True)
    elif (gender == 'Female'):
        st.markdown(f"<span style='color: #367588;font-size: 19px;font-weight: bold;'>Your ideal daily calorie intake should be 2000 Cal</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color: #367588;font-size: 19px;font-weight: bold;'>Your ideal daily water intake should be 2.7 L</span>", unsafe_allow_html=True)
    elif (gender == 'Other'):
        st.markdown(f"<span style='color: #367588;font-size: 19px;font-weight: bold;'>Sorry, info not available :)</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span style='color: #367588;font-size: 19px;font-weight: bold;'>Sorry, info not available :)</span>", unsafe_allow_html=True)
   

  
   
def page_six():
    st.title("Food Recommendation System")
    st.text("Let us refer what you prefer!")
    st.image("Streamlit/resources/f1.jpg")

    ## nav = st.sidebar.radio("Navigation",["Home","IF Necessary 1","If Necessary 2"])

    st.subheader("Whats your preference?")
    vegn = st.radio("Choose your choice",["veg","non-veg"],index = 1) 

    st.subheader("What Cuisine do you prefer?")
    cuisine = st.selectbox("Choose your favourite!",['Healthy Food', 'Snack', 'Dessert', 'Japanese', 'Indian', 'French',
        'Mexican', 'Italian', 'Chinese', 'Beverage', 'Thai'])


    st.subheader("How well do you want the dish to be?")  #RATING
    val = st.slider("Rate from 0-10!",0,10)



    food = pd.read_csv("Streamlit/resources/input/food.csv")
    
    ratings = pd.read_csv("Streamlit/resources/input/ratings.csv")
    combined = pd.merge(ratings, food, on='Food_ID')

    #ans = food.loc[(food.C_Type == cuisine) & (food.Veg_Non == vegn),['Name','C_Type','Veg_Non']]

    ans = combined.loc[(combined.C_Type == cuisine) & (combined.Veg_Non == vegn)& (combined.Rating >= val),['Name','C_Type','Veg_Non']]
    names = ans['Name'].tolist()
    x = np.array(names)
    ans1 = np.unique(x)

    finallist = ""
    bruh = st.checkbox("Choose your Dish")
    if bruh == True:
        finallist = st.selectbox("Our Choices",ans1)


    ##### IMPLEMENTING RECOMMENDER ######
    dataset = ratings.pivot_table(index='Food_ID',columns='User_ID',values='Rating')
    dataset.fillna(0,inplace=True)
    csr_dataset = csr_matrix(dataset.values)
    dataset.reset_index(inplace=True)

    model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
    model.fit(csr_dataset)

    def food_recommendation(Food_Name):
        n = 10
        FoodList = food[food['Name'].str.contains(Food_Name)]  
        if len(FoodList):        
            Foodi= FoodList.iloc[0]['Food_ID']
            Foodi = dataset[dataset['Food_ID'] == Foodi].index[0]
            distances , indices = model.kneighbors(csr_dataset[Foodi],n_neighbors=n+1)    
            Food_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
            Recommendations = []
            for val in Food_indices:
                Foodi = dataset.iloc[val[0]]['Food_ID']
                i = food[food['Food_ID'] == Foodi].index
                Recommendations.append({'Name':food.iloc[i]['Name'].values[0],'Distance':val[1]})
            df = pd.DataFrame(Recommendations,index=range(1,n+1))
            return df['Name']
        else:
            return "No Similar Foods"


    display = food_recommendation(finallist)
    #names1 = display['Name'].tolist()

    #x1 = np.array(names)
    #ans2 = np.unique(x1)
    if bruh == True:
        bruh1 = st.checkbox("We also Recommend : ")
        if bruh1 == True:
            for i in display:
                st.write(i)
            


def page_five():
    df = pd.read_csv("Streamlit/resources/Food_Matrix/Food_Matrix1.csv")  # read a CSV file inside the 'data" folder next to 'app.py'


    st.title("Food Matrix 🍔")  # add a title
    st.markdown("There are many combinations of foods which are harmful to human health, and are still consumed by people due to lack of awareness. These include combinations of generalized food categories and also of specific food items. These combinations can be indicated using a matrix. There are two matrix representations below that indicate harmful combinations of foods. The first one is for generalized food categories while the second one is for specific food items.")

    st.subheader("1. Food Compatibility Matrix (Food Categories)")
    st.markdown("There are certain combinations of foods which are harmful to health when consumed together. They may become difficult to digest, and may cause problems such as acidity. They may even be toxic and lead to diseases. For example, fruits should be consumed separately and not with any meal. It is necessary for people to be aware of such food combinations, so that they do not consume them together, or use them together in cooking. The below data shows various combinations of generalized food categories, and indicates which of these combinations are harmful (toxic) or harmless (non-toxic). ")
    
    df_display1 = pd.read_csv("Streamlit/resources/Food_Matrix/Food_Matrix1.csv")
    
    df = pd.read_csv("Streamlit/resources/Food_Matrix/Food_Matrix1.csv")

    st.subheader("Visualization of the raw data 📈")  # add a title
    data = pd.read_csv('Streamlit/resources/Food_Matrix/Food_Matrix1.csv' , na_values= "NaN")
    data.fillna(0 , inplace = True)


    id_labels = data.columns[1:]
    
    # take the transpose since you want to see id on y-axis
    id_matrix = np.array(data[id_labels].values, dtype=float).T

    fig, ax = plt.subplots(figsize=(8,8))


    mat = ax.imshow(id_matrix, cmap="Reds", interpolation='nearest')

    plt.yticks(range(id_matrix.shape[0]), id_labels)
    plt.xticks(range(id_matrix.shape[1]), id_labels)
    plt.xticks(rotation=25)

    blue_patch = mpatches.Patch(color='maroon', label='Toxic')
    white_patch = mpatches.Patch(color='#FFF5F0', label='Non-Toxic')


    fontP = FontProperties()
    fontP.set_size('xx-small')

    #legend outside
    plt.legend(handles = [blue_patch , white_patch], bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size':15}) 

    plt.xlabel('Food Compatibility Matrix (Food Categories)')


    st.pyplot(plt,dpi=100)

    st.subheader("2. Food compatibility matrix (For harmful combinations of specific food items)")
    st.markdown("Apart from the above generalized categories, there are some specific food items which are harmful when consumed together. Most people are not aware of these combinations. A prominent example is banana milkshake. It is a popular beverage but most people are not aware that milk should not be consumed with bananas as it causes heaviness and may also lead to lethargy. Such combinations of food items are indicated in the below data.")

    df2 = pd.read_csv("Streamlit/resources/Food_Matrix/Food_Matrix2.csv")  # read a CSV file inside the 'data" folder next to 'app.py'

    df21 = pd.read_csv("Streamlit/resources/Food_Matrix/Food_Matrix2.csv")

   


    st.subheader("Visualization of the above given data 📈")  # add a title
    data2 = pd.read_csv('Streamlit/resources/Food_Matrix/Food_Matrix2.csv' , na_values= "NaN")
    data2.fillna(0 , inplace = True)


    id_labels = data2.columns[1:]
    
    # take the transpose since you want to see id on y-axis
    id_matrix = np.array(data2[id_labels].values, dtype=float).T

    fig, ax = plt.subplots(figsize=(8,8))


    mat = ax.imshow(id_matrix, cmap="Blues", interpolation='nearest')

    plt.yticks(range(id_matrix.shape[0]), id_labels)
    plt.xticks(range(id_matrix.shape[1]), id_labels)
    plt.xticks(rotation=25)

    blue_patch = mpatches.Patch(color='#0b306b', label='Toxic')
    white_patch = mpatches.Patch(color='#f7fbff', label='Non-Toxic')


    fontP = FontProperties()
    fontP.set_size('xx-small')

    #legend outside
    plt.legend(handles = [blue_patch , white_patch], bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size':15}) 


    #plt.legend(handles = [blue_patch , white_patch],title='title', bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size':15}) 

    #legend inside
    #plt.legend(handles = [blue_patch , white_patch])

    plt.xlabel('For harmful combinations of specific food items')


    st.pyplot(plt,dpi=100)
   
#calling the main function to basically invoke the whole code 
#https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/
if __name__ == "__main__":
    main()





#code to be used to text display with html properties
#st.markdown("<h6 style='text-align: justify;font-size:100%;font-family:Arial,sans-serif;line-height: 1.3;'>description</h6>",unsafe_allow_html=True)
#st.markdown("")

#blue title
#st.markdown(f"<span style='color: #000080;font-size: 24px;font-weight: bold;'>1</span>", unsafe_allow_html=True)

#units of parameters
#st.markdown(f"<span style='color: #367588;font-size: 12px;font-weight: bold;'>Units: Protein (grams) & Carbohydrates (grams)</span>", unsafe_allow_html=True)
