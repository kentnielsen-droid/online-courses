import streamlit as st
import pandas as pd
import numpy as np

URL = "https://raw.githubusercontent.com/marcopeix/MachineLearningModelDeploymentwithStreamlit/master/12_dashboard_capstone/data/quarterly_canada_population.csv"

df = pd.read_csv(
    "/Users/dkengineer/Code/online-courses/udemy-deploy-ml-models-with-streamlit/data/quarterly_population_canada.csv",
    dtype={
        "Quarter": str,
        "Canada": np.int32,
        "Newfoundland and Labrador": np.int32,
        "Prince Edward Island": np.int32,
        "Nova Scotia": np.int32,
        "New Brunswick": np.int32,
        "Quebec": np.int32,
        "Ontario": np.int32,
        "Manitoba": np.int32,
        "Saskatchewan": np.int32,
        "Alberta": np.int32,
        "British Columbia": np.int32,
        "Yukon": np.int32,
        "Northwest Territories": np.int32,
        "Nunavut": np.int32,
    },
)
df[["Q", "Year"]] = df["Quarter"].str.extract(r"(Q[1-4])\s+(\d{4})")
df["Year"] = df["Year"].astype(int)
df["Q"] = pd.Categorical(df["Q"], categories=["Q1", "Q2", "Q3", "Q4"], ordered=True)
df = df.sort_values(["Year", "Q"])

st.title("Population of Canada")
st.markdown(f"Source table can be found [here]({URL})")
with st.expander("See data table"):
    st.dataframe(df)

with st.form("form_data"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Select start date")
        start_quarter = st.selectbox(
            "Quarter",
            options=df["Q"].unique().sort_values().tolist(),
            index=0,
        )
        start_year = st.slider(
            "Year",
            min_value=int(df["Year"].min()),
            max_value=int(df["Year"].max()),
            value=int(df["Year"].min()),
        )
        submitted = st.form_submit_button("Analyze", type="primary")
    with col2:
        st.write("Select end date")
        end_quarter = st.selectbox(
            "Quarter",
            options=df["Q"].unique().sort_values().tolist(),
            index=len(df["Q"].unique()) - 1,
        )
        end_year = st.slider(
            "Year",
            min_value=int(df["Year"].min()),
            max_value=int(df["Year"].max()),
            value=int(df["Year"].max()),
        )
    with col3:
        st.write("Select region")
        region = st.selectbox("Region", options=df.columns[1:-2].tolist(), index=0)

if submitted:
    temp_df = df.copy()

    start_exists = any((temp_df["Year"] == start_year) & (temp_df["Q"] == start_quarter))
    end_exists = any((temp_df["Year"] == end_year) & (temp_df["Q"] == end_quarter))

    if not start_exists:
        st.error(
            f"Error: The start date {start_year}-{start_quarter} is not available in the data. Please adjust your selection."
        )
    elif not end_exists:
        st.error(
            f"Error: The end date {end_year}-{end_quarter} is not available in the data. Please adjust your selection."
        )
    elif ((start_year > end_year) | (start_year >= end_year & int(start_quarter.replace("Q", "")) >= int(end_quarter.replace("Q", "")))):
        st.error("the start date cannot be greater than end date. Please adjust your selection.")
    else:
        mask = ((temp_df["Year"] >= start_year) & (temp_df["Q"] >= start_quarter)) & (
            ((temp_df["Year"] <= end_year) & (temp_df["Q"] <= end_quarter))
        )
        temp_df["Qn"] = temp_df["Q"].str.extract(r"Q([1-4])").astype(int)
        temp_df["quarter_start"] = pd.PeriodIndex(
            year=temp_df["Year"], quarter=temp_df["Qn"], freq="Q"
        ).start_time

        population_tab, compare_tab = st.tabs(["Population over time", "Compare regions"])
        with population_tab:
            pop_change_col1, pop_change_col2 = st.columns(2)
            with pop_change_col1:
                start_pop = temp_df.loc[mask, region].iloc[0]
                end_pop = temp_df.loc[mask, region].iloc[-1]
                abs_change = end_pop - start_pop
                perc_change = (end_pop - start_pop) / start_pop * 100
                st.metric(
                    label=f"Population of {region} in {start_quarter} {start_year}",
                    value=f"{start_pop:,}",
                )
                st.metric(
                    label=f"Absolute change in population of {region} in {end_quarter} {end_year}",
                    value=f"{abs_change:,}",
                    delta=f"{perc_change:.2f}%",
                )

            with pop_change_col2:
                filtered = temp_df.loc[
                    mask, ["quarter_start", "Quarter", region]
                ].sort_values("quarter_start")
                st.line_chart(filtered.set_index("quarter_start")[region])
        with compare_tab:
            st.write("Compare population of all regions")
            regions = st.multiselect(
                "Select regions to compare",
                options=df.columns[1:-2].tolist(),
                default=df.columns[1],
            )
            filtered_data = temp_df.loc[mask, ["quarter_start"] + regions].sort_values(
                "quarter_start"
            )
            st.line_chart(filtered_data.set_index("quarter_start"))
else:
    st.info("Please select the start and end date, then click on Analyze")
