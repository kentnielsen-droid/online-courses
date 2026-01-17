import streamlit as st
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.feature_selection import SelectKBest, mutual_info_classif

# Set page config:
# The title is "Experiment"
# Choose an icon for the page
# The layout is centered
# The sidebar is set to "auto"
st.set_page_config(
    page_title="Experiments",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="auto",
)

# Write a function to load the wine dataset from sklearn
# Should you cache it?
@st.cache_data(show_spinner="Loading data...")
def load_data():
    wine_data = load_wine()
    wine_df = pd.DataFrame(data=wine_data.data, columns=wine_data.feature_names)

    wine_df['target'] = wine_data.target

    return wine_df

# Run the function to load the data
wine_df = load_data()

# Write a function for train/test split.
# Use stratification, and keep 30% of the data for the test set
# Should you cache it?
@st.cache_data
def split_data(df: pd.DataFrame):
    X = df.drop(['target'], axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True, stratify=y)
    return X_train, X_test, y_train, y_test


# Run your train/test split function
X_train, X_test, y_train, y_test = split_data(wine_df)

# Write a function to select features using SelectKbest and mutual_info_classif
# Should you cache it?
@st.cache_data
def select_features(X_train, y_train, X_test, k):
    selector = SelectKBest(mutual_info_classif, k=k)
    selector.fit(X_train, y_train)

    sel_X_train = selector.transform(X_train)
    sel_X_test = selector.transform(X_test)

    return sel_X_train, sel_X_test

# Write a function that fits the selected model and computes the F1-score
# The function must return the F1-Score
# Inside this function, you must run feature selection
# Should you cache it?
@st.cache_data(show_spinner="Training and evaluating model")
def fit_and_score(model, k):
    if model == "Baseline":
        clf = DummyClassifier(strategy="stratified")
    elif model == "Decision Tree":
        clf = DecisionTreeClassifier()
    elif model == "Random Forest":
        clf = RandomForestClassifier()
    else:
        clf = GradientBoostingClassifier()

    sel_X_train, sel_X_test = select_features(X_train, y_train, X_test, y_test)
    clf.fit(sel_X_train, y_train)
    preds = clf.predict(sel_X_test)
    score = round(f1_score(y_test, preds, average="weighted"), 3)

    return score

# Write a callback function that runs the model fitting and scoring function
# The callback appends the model, number of features, and score to the state.
# The callback takes 2 arguments: the model and the number of features to keep
def save_performance(model, k):
    score = fit_and_score(model, k)
    st.session_state['model'].append(model)
    st.session_state['num_features'].append(k)
    st.session_state['score'].append(score)

if __name__ == "__main__":
    
    with st.container():
        st.title("🧪 Experiments")

    col1, col2 = st.columns(2)

    with col1:
        model = st.selectbox("Choose a model", ["Baseline", "Decision Tree", "Random Forest", "Gradient Boosted Classifier"])
    with col2:
        k = st.number_input("Choose the number of features to keep", 1, 13)

    # Plug in your callback and define the arguments
    st.button("Train", type="primary", on_click=save_performance, args=(model, k))

    # Display the full dataset inside an expander
    with st.expander("See full dataset"):
        st.write(wine_df)

    if len(st.session_state['score']) != 0:
        st.subheader(f"The model has an F1-Score of: {st.session_state['score'][-1]}")
        