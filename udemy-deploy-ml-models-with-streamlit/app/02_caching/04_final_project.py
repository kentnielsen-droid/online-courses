import streamlit as st
import pandas as pd
import numpy as np
from joblib import dump, load
from pathlib import Path
from typing import Union, List
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline

URL = "/Users/dkengineer/Code/online-courses/udemy-deploy-ml-models-with-streamlit/data/mushrooms.csv"
COLS = [
    "class",
    "odor",
    "gill-size",
    "gill-color",
    "stalk-surface-above-ring",
    "stalk-surface-below-ring",
    "stalk-color-above-ring",
    "stalk-color-below-ring",
    "ring-type",
    "spore-print-color",
]


@st.cache_data
def read_data(url: str, cols: List[str]) -> pd.DataFrame:
    df = pd.read_csv(url, usecols=cols)
    return df


@st.cache_resource
def train_model(df: pd.DataFrame, _pipe: Pipeline):
    file_path = "/Users/dkengineer/Code/online-courses/udemy-deploy-ml-models-with-streamlit/models/mushroom_model.joblib"
    if not Path(file_path).exists():
        encoded_df = df.copy()
        X = encoded_df.drop(["class"], axis=1)
        y = encoded_df["class"]
        model = _pipe.fit(X, y)
        dump(_pipe, file_path)
        return model
    else:
        model = load(file_path)
        return model


@st.cache_data
def predict(
    _model: GradientBoostingClassifier, X_test: pd.DataFrame
) -> Union[pd.Series, str, np.array]:
    formatted_X_test = np.array(X_test).reshape(1, -1)
    return _model.predict(formatted_X_test)


if __name__ == "__main__":
    st.title("Mushroom classifier 🍄")

    df = read_data(URL, COLS)
    pipe = Pipeline(
        [
            ("encoder", OrdinalEncoder()),
            ("gbc", GradientBoostingClassifier(max_depth=5)),
        ]
    )

    st.subheader("Step 1: Select the values for prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        odor = st.selectbox(
            "Odor",
            (
                "a - almond",
                "l - anisel",
                "c - creosote",
                "y - fishy",
                "f - foul",
                "m - musty",
                "n - none",
                "p - pungent",
                "s - spicy",
            ),
        )
        stalk_surface_above_ring = st.selectbox(
            "Stalk surface above ring",
            ("f - fibrous", "y - scaly", "k - silky", "s - smooth"),
        )
        stalk_color_below_ring = st.selectbox(
            "Stalk color below ring",
            (
                "n - brown",
                "b - buff",
                "c - cinnamon",
                "g - gray",
                "o - orange",
                "p - pink",
                "e - red",
                "w - white",
                "y - yellow",
            ),
        )
    with col2:
        gill_size = st.selectbox("Gill size", ("b - broad", "n - narrow"))
        stalk_surface_below_ring = st.selectbox(
            "Stalk surface below ring",
            ("f - fibrous", "y - scaly", "k - silky", "s - smooth"),
        )
        ring_type = st.selectbox(
            "Ring type",
            (
                "e - evanescente",
                "f - flaring",
                "l - large",
                "n - none",
                "p - pendant",
                "s - sheathing",
                "z - zone",
            ),
        )
    with col3:
        gill_color = st.selectbox(
            "Gill color",
            (
                "k - black",
                "n - brown",
                "b - buff",
                "h - chocolate",
                "g - gray",
                "r - green",
                "o - orange",
                "p - pink",
                "u - purple",
                "e - red",
                "w - white",
                "y - yellow",
            ),
        )
        stalk_color_above_ring = st.selectbox(
            "Stalk color above ring",
            (
                "n - brown",
                "b - buff",
                "c - cinnamon",
                "g - gray",
                "o - orange",
                "p - pink",
                "e - red",
                "w - white",
                "y - yellow",
            ),
        )
        spore_print_color = st.selectbox(
            "Spore print color",
            (
                "k - black",
                "n - brown",
                "b - buff",
                "h - chocolate",
                "r - green",
                "o - orange",
                "u - purple",
                "w - white",
                "y - yellow",
            ),
        )

    st.subheader("Step 2: Ask the model for a prediction")

    pred_btn = st.button("Predict", type="primary")

    if pred_btn:
        model = train_model(df, pipe)
        x_test = [
            odor.split("-")[0].strip(),
            gill_size.split("-")[0].strip(),
            gill_color.split("-")[0].strip(),
            stalk_surface_above_ring.split("-")[0].strip(),
            stalk_surface_below_ring.split("-")[0].strip(),
            stalk_color_above_ring.split("-")[0].strip(),
            stalk_color_below_ring.split("-")[0].strip(),
            ring_type.split("-")[0].strip(),
            spore_print_color.split("-")[0].strip(),
        ]
        pred = predict(model, x_test)
        if pred == "e":
            st.write("The mushroom is edible 👍")
        else:
            st.write("The mushroom is not edible 🙅‍♂️")
