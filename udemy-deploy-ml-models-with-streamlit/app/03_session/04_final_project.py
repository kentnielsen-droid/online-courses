import streamlit as st
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Union
from joblib import load, dump
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

URL = "/Users/dkengineer/Code/online-courses/udemy-deploy-ml-models-with-streamlit/data/car_data.csv"


@st.cache_data
def read_data(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    return df


# Initialize the session state with an empty prediction
if "prediction" not in st.session_state:
    st.session_state["prediction"] = None


# Function to load the model (use caching)
@st.cache_resource
def train_model(df: pd.DataFrame, _pipe: Pipeline):
    file_path = "/Users/dkengineer/Code/online-courses/udemy-deploy-ml-models-with-streamlit/models/car_model.joblib"
    if not Path(file_path).exists():
        encoded_df = df.copy()
        X = encoded_df.drop(["price"], axis=1)
        y = encoded_df["price"]
        model = _pipe.fit(X, y)
        dump(_pipe, file_path)
        return model
    else:
        model = load(file_path)
        return model


def predict(_model: GradientBoostingRegressor):
    X_test = [
        st.session_state["miles"],
        st.session_state["year"],
        st.session_state["make"],
        st.session_state["model"],
        st.session_state["engine_size"],
        st.session_state["province"],
    ]
    formatted_X_test = np.array(X_test).reshape(1, -1)
    prediction = round(_model.predict(formatted_X_test)[0], 2)
    st.session_state["prediction"] = prediction


if __name__ == "__main__":
    st.title("🇨🇦Used car price calculator")

    # Data and Load model
    df = read_data(URL)
    pipe_encoder = Pipeline(
        steps=[
            ("encoder", OneHotEncoder()),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[("transformer", pipe_encoder, [2, 3, 5])]
    )
    pipe = Pipeline(
        steps=[("preprocessor", preprocessor), ("gbr", GradientBoostingRegressor())]
    )
    model = train_model(df, pipe)

    with st.form(key="form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.number_input(
                "Miles", value=86132.0, min_value=0.0, step=0.1, key="miles"
            )
            st.selectbox(
                "Model",
                index=0,
                key="model",
                options=[
                    "Prius",
                    "Highlander",
                    "Civic",
                    "Accord",
                    "Corolla",
                    "Ridgeline",
                    "Odyssey",
                    "CR-V",
                    "Pilot",
                    "Camry Solara",
                    "Matrix",
                    "RAV4",
                    "Rav4",
                    "HR-V",
                    "Fit",
                    "Yaris",
                    "Yaris iA",
                    "Tacoma",
                    "Camry",
                    "Avalon",
                    "Venza",
                    "Sienna",
                    "Passport",
                    "Accord Crosstour",
                    "Crosstour",
                    "Element",
                    "Tundra",
                    "Sequoia",
                    "Corolla Hatchback",
                    "4Runner",
                    "Echo",
                    "Tercel",
                    "MR2 Spyder",
                    "FJ Cruiser",
                    "Corolla iM",
                    "C-HR",
                    "Civic Hatchback",
                    "86",
                    "S2000",
                    "Supra",
                    "Insight",
                    "Clarity",
                    "CR-Z",
                    "Prius Prime",
                    "Prius Plug-In",
                    "Prius c",
                    "Prius C",
                    "Prius v",
                ],
            )
        with col2:
            st.number_input("Year", value=2001, min_value=1886, step=1, key="year")
            st.number_input(
                "Engine size (L)", value=1.5, key="engine_size", min_value=0.9, step=0.1
            )
        with col3:
            st.selectbox("Make", key="make", index=0, options=["toyota", "honda"])
            st.selectbox(
                "Province",
                index=0,
                key="province",
                options=[
                    "NB",
                    "QC",
                    "BC",
                    "ON",
                    "AB",
                    "MB",
                    "SK",
                    "NS",
                    "PE",
                    "NL",
                    "YT",
                    "NC",
                    "OH",
                    "SC",
                ],
            )

        st.form_submit_button(
            "Calculate",
            type="primary",
            on_click=predict,
            kwargs=dict(_model=model),
        )

    # Display the prediction
    # If the value is empty, display a message to click on the button
    # Otherwise, display the prediction
    if st.session_state["prediction"] is None:
        st.write("Press 'Calculate' to estimate car prices")
    else:
        st.write(f"The estimated car price is ${st.session_state["prediction"]}")

    st.write(st.session_state)
