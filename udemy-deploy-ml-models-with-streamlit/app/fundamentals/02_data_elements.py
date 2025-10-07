import streamlit as st
import pandas as pd

# Loading data
df = pd.read_csv(
    "/home/vugs/Codes/Home_Projects/online-courses/udemy-deploy-ml-models-with-streamlit/data/sample_data.csv"
)

# Displaying data
st.dataframe(df)
# st.write(df)  # Alternative way to display data
st.table(df)  # Static table

# Metrics
st.metric(label="Temperature", value="70 °F", delta="1.2 °F")
st.metric(label="Humidity", value="80 %", delta="-5 %")
