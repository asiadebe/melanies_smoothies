import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Tytuł aplikacji
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Pole na imię w zamówieniu
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", name_on_order)

# Połączenie z Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Pobranie danych z tabeli
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()

# Lista składników do wyboru
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'].tolist(),  # ✅ poprawione
    max_selections=5
)

# Obsługa wybranych składników
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)  # ✅ prostsze łączenie

    for fruit_chosen in ingredients_list:
        # Pobranie wartości SEARCH_ON
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write(f"The search value for {fruit_chosen} is {search_on}.")

        # Pobranie informacji o wartości odżywczej z API
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        if smoothiefroot_response.status_code == 200:
            nutrition_data = pd.DataFrame([smoothiefroot_response.json()])  # ✅ konwersja na DataFrame
            st.subheader(f"{fruit_chosen} Nutrition Information")
            st.dataframe(nutrition_data, use_container_width=True)
        else:
            st.error(f"Could not fetch data for {fruit_chosen}. API returned {smoothiefroot_response.status_code}")

    # Zabezpieczenie przed SQL Injection
    safe_name = name_on_order.replace("'", "''")

    # Tworzenie zapytania SQL
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{safe_name}')
    """

    # Przycisk do wysłania zamówienia
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}", icon="✅")
