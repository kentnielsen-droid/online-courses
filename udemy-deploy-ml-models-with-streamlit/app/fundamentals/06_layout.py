import streamlit as st
import pandas as pd

# Sidebar
with st.sidebar:
    st.header("Sidebar")
    st.write("This is the sidebar content.")
    st.button("Click Me")

# Columns
col1, col2, col3 = st.columns(3)
with col1:
    st.header("Column 1")
    st.write("This is the content of column 1.")
    st.button("Button 1")
with col2:
    st.header("Column 2")
    st.write("This is the content of column 2.")
    st.button("Button 2")
with col3:
    st.header("Column 3")
    st.write("This is the content of column 3.")
    st.button("Button 3")
st.divider()

# Tabs
df = pd.read_csv("/Users/dkengineer/Code/online-courses/udemy-deploy-ml-models-with-streamlit/data/sample_data.csv")
tab1, tab2 = st.tabs(["Line plot", "Bar plot"])
with tab1:
    st.header("Line plot")
    st.line_chart(df, x="purchase_date", y="purchase_amount")
with tab2:
    st.header("Bar plot")
    st.bar_chart(df, x="product_category", y="purchase_amount")
st.divider()

# Expander
with st.expander("See explanation"):
    st.write("""
        This is an example of an expander. You can put any content you want here,
        and it will be hidden until the user clicks to expand it.
    """)
    st.image("https://static.streamlit.io/examples/dice.jpg", width=200)
st.divider()

# Containers
with st.container():
    st.header("Container 1")
    st.write("This is the content of container 1.")
    st.button("Container Button 1")
st.divider()