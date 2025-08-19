# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in the Smoothie!")

Name_on_order = st.text_input('Name on smoothie:')
st.write('The name on your smoothie will be:', Name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.stop()
# Ingredient selection
INGREDIENTS_LIST = st.multiselect('Choose up to 5 ingredients', my_dataframe, max_selections=5)

if INGREDIENTS_LIST:
    ingredients_string = ''
    for fruit_chosen in INGREDIENTS_LIST:
        ingredients_string += fruit_chosen + ' '

        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen.lower()}")
        st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{Name_on_order}')
    """

    # Submit button with unique key
    time_to_insert = st.button('Submit order', key="submit_order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your smoothie is ordered!, {Name_on_order}', icon="✅")
