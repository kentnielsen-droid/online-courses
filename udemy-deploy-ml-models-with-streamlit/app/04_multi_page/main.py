import streamlit as st
import pandas as pd

# Set page config:
# The title is "Homepage"
# Choose an icon for the page
# The layout is centered
# The sidebar is set to "auto"

st.set_page_config(
    page_title="Homepage",
    page_icon="💻",
    layout="centered",
    initial_sidebar_state="auto",
)

# Initialize the state with the keys: [model, num_features, score]
# This is where we store the info to display the ranking

if all(
    key not in st.session_state.keys() for key in ("model", "num_features", "score")
):
    st.session_state["model"] = []
    st.session_state["num_features"] = []
    st.session_state["score"] = []

# Write a function to display a DataFrame ranked in descending order of F1-Score
# The DataFrame has 3 columns: Model, Number of Features, F1-Score


def display_df():
    df = pd.DataFrame(
        {
            "Model": st.session_state["model"],
            "Number of features": st.session_state["num_features"],
            "F1-Score": st.session_state["score"],
        }
    )
    sorted_df = df.sort_values(by=['F1-Score'], ascending=False).reset_index(drop=True)
    st.dataframe(sorted_df)


if __name__ == "__main__":
    st.title("🏆 Model ranking")

    if len(st.session_state["model"]) == 0:
        st.subheader("Train a model in the next page to see the results 👉")
    else:
        # Function that display the DataFrame runs here
        display_df()

    st.write(st.session_state)
