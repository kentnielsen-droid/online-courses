import streamlit as st
import pandas as pd

# Buttons
primary_button = st.button(label="Primary Button", type="primary")
secondary_button = st.button(label="Secondary Button", type="secondary")
if primary_button:
    st.write("Primary button clicked!")
if secondary_button:
    st.write("Secondary button clicked!")
st.divider()

# Checkboxes
checkbox = st.checkbox(label="Check me!")
if checkbox:
    st.write("Checkbox is checked!")
st.divider()

# Radio Buttons
df = pd.read_csv(
    "/Users/dkengineer/Code/online-courses/udemy-deploy-ml-models-with-streamlit/data/sample_data.csv"
)
radio = st.radio(
    label="Select an option:", options=df.product_category.unique(), horizontal=True
)
st.write(f"You selected: {radio}")
st.divider()

# Selectbox
selectbox = st.selectbox(
    label="Choose a product category:", options=df.product_category.unique()
)
st.write(f"You selected: {selectbox}")
st.divider()

# Multiselect
multiselect = st.multiselect(
    label="Select multiple categories:", options=df.product_category.unique()
)
st.write(f"You selected: {multiselect}")
multiselect_limit = st.multiselect(
    label="Select multiple categories (MAX 3):",
    options=df.product_category.unique(),
    max_selections=3,
)
st.write(multiselect_limit)
st.divider()

# Slider
slider = st.slider(label="Select a value:", min_value=0, max_value=100, value=0)
st.write(f"You selected: {slider}")

slider = st.slider(label="Select a value:", min_value=0.0, max_value=10.0, value=0., step=0.5)
st.write(f"You selected: {slider}")
st.divider()

# Text Input
text_input = st.text_input(label="Enter some text:", placeholder="Type here...")
st.write(f"You entered: {text_input}")
st.divider()

# Text Area
text_area = st.text_area(label="Enter a longer text:", placeholder="Type here...")
st.write(f"You entered: {text_area}")
st.divider()

# Number Input
number_input = st.number_input(label="Enter a number:", min_value=0, max_value=10, value=0)
st.write(f"You entered: {number_input}")
st.divider()