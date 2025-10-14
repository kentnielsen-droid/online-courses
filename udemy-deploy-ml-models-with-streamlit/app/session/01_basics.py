import streamlit as st

st.title("Stateful apps")

st.write("Here is the session state:")
st.write(st.session_state)
st.button("Update state")

# Set the value
if "key" not in st.session_state:
    st.session_state["key"] = "value"

# Read value
st.write(f"Reading: {st.session_state['key']}")

# Update value
st.session_state["key"] = "new value"

# Remove value
del st.session_state["key"]