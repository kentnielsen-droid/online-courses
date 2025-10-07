import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "/home/vugs/Codes/Home_Projects/online-courses/udemy-deploy-ml-models-with-streamlit/data/sample_data.csv"
)

# Line Chart
st.line_chart(df, x="purchase_date", y="purchase_amount")

# Bar Chart
st.bar_chart(df, x="purchase_date", y="purchase_amount")

# Matplotlib Chart
fig, ax = plt.subplots()
ax.plot(df.purchase_date, df.purchase_amount)
ax.set_xlabel("Purchase Date")
ax.set_ylabel("Purchase Amount")
ax.set_title("Purchase Date and Purchase Amount Over Time")
ax.legend()
fig.autofmt_xdate()
st.pyplot(fig)

# Area Chart
st.area_chart(df, x="purchase_date", y="purchase_amount")

# Map
map_df = pd.read_csv(
    "/home/vugs/Codes/Home_Projects/online-courses/udemy-deploy-ml-models-with-streamlit/data/sample_map.csv"
)
st.map(map_df)
