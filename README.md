# Smoothie Customizer App

This Streamlit application allows users to create custom smoothies by selecting ingredients, viewing nutritional information from an external API, and submitting orders to a Snowflake database.

## Features
- Enter a name for your smoothie.
- Select up to 5 ingredients from a list stored in Snowflake.
- Fetch nutritional information for each selected ingredient via an API.
- Submit the order to the `smoothies.public.orders` table in Snowflake.

## Requirements
- Python 3.9+
- Streamlit
- Snowflake Snowpark
- Pandas
- Requests

Install dependencies:
```bash
pip install -r requirements.txt
```

Example `requirements.txt`:
```
streamlit
snowflake-snowpark-python
pandas
requests
```

## How It Works
1. Connects to Snowflake using `st.connection("snowflake")`.
2. Retrieves available fruits from `smoothies.public.fruit_options`.
3. Displays a multiselect widget for choosing ingredients.
4. For each selected ingredient:
   - Calls an external API (`https://my.smoothiefroot.com/api/fruit/{search_on}`) to fetch nutrition data.
   - Displays the data in a table.
5. Inserts the order into Snowflake using a secure SQL statement.

## Usage
Run the app:
```bash
streamlit run app.py
```

Open the URL provided by Streamlit in your browser.

## Example Workflow
- Enter your name in the text input.
- Select up to 5 fruits.
- Review nutritional information.
- Click **Submit Order** to save your smoothie in Snowflake.

## Future Improvements
- Add error handling for API failures.
- Validate user input before inserting into the database.
- Enhance UI with images and better layout.
