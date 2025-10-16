import streamlit as st
import time
import numpy as np
from sklearn.linear_model import LinearRegression

st.title("Caching")

st.header("Cached data")

st.button("Press me")

@st.cache_data
def cached_func():
    time.sleep(2)
    out = "I'm done running…"
    return out

out = cached_func()
st.write(out)

st.divider()

st.header("Cached resource")

@st.cache_resource
def create_lr():
    time.sleep(2)
    X = np.array([1,2,3,4,5,6,7]).reshape(-1, 1)
    y = np.array([1,2,3,4,5,6,7])

    model = LinearRegression().fit(X, y)

    return model

lr = create_lr()
X_pred = np.array([8]).reshape(-1, 1)
pred = lr.predict(X_pred)

st.write(f"The prediction is: {pred[0]}")