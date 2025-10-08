import streamlit as st

# Form
with st.form("form_order"):
    st.write("What would you like to order?")
    appetizer = st.selectbox("Appetizers", ["Salad", "Soup", "Nachos"], index=None, placeholder="Select an appetizer")
    main_course = st.selectbox("Main Course", ["Steak", "Pasta", "Fish"], index=None, placeholder="Select a main course")
    dessert = st.selectbox("Dessert", ["Ice Cream", "Cake", "Pie"], index=None, placeholder="Select a dessert")
    is_over_21 = st.checkbox("I am over 21 years old")
    arrival_date = st.date_input("When are you comming?")
    arrival_time = st.time_input("At what time are you comming?")
    allergies = st.text_area("Please list any allergies you have")
    submit = st.form_submit_button("Submit order")
if submit:
    st.write("Your order:")
    st.write(f"- Appetizer: {appetizer}")
    st.write(f"- Main Course: {main_course}")
    st.write(f"- Dessert: {dessert}")
    st.write(f"- Over 21: {'Yes' if is_over_21 else 'No'}")
    st.write(f"- Arrival Date: {arrival_date}")
    st.write(f"- Arrival Time: {arrival_time}")
    st.write(f"- Allergies: {allergies}")
