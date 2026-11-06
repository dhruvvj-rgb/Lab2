# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "data.csv"

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("Enter a hobby:")
    value_input = st.text_input("Enter weekly minutes spent on that hobby:")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # --- YOUR LOGIC GOES HERE ---
        # TO DO:
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a').
        #    - Don't forget to add a newline character '\n' at the end.
        if category_input.strip() == "" or value_input.strip() == "":
            st.error("Please enter both a hobby and the weekly minutes.")
            st.stop()

        try:
            numeric_value = float(value_input)
        except ValueError:
            st.error("Weekly minutes must be a number.")
            st.stop()

        if numeric_value < 0:
            st.error("Weekly minutes cannot be negative.")
            st.stop()

        new_row = pd.DataFrame({
            "Category": [category_input.strip()],
            "Value": [numeric_value]
        })
        new_row.to_csv(csv_path, mode="a", header=False, index=False)
        
        st.success("Your data has been submitted!")
        st.write(f"You entered: **Hobby:** {category_input}, **Weekly Minutes:** {value_input}")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if csv_path.exists() and csv_path.stat().st_size > 0:
    current_data_df = pd.read_csv(csv_path)
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
