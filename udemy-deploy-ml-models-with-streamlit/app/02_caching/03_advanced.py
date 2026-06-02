import streamlit as st
import time
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


# Cache the data for ttl seconds
@st.cache_data(ttl=30)
def ttl_func():
    time.sleep(5)
    st.write("Finished running func with time_to_live cache.")


@st.cache_data(max_entries=10)
def max_entries_func():
    df = pd.read_csv(DATA_DIR / "quarterly_population_canada.csv")
    st.write(df)

@st.cache_data(show_spinner="Performing very complex tasks!")
def spinner_func():
    time.sleep(5)
    st.write("Finished spinning.")

if __name__ == "__main__":
    st.title("Advanced Caching")
    st.write("Note that cached functions must have hashable input parameters. Adding the prefix '_' e.g.")
    code = "def my_func(_model, age):\n\tprint(age)"
    st.code(code)
    ttl_func()
    max_entries_func()
    spinner_func()
