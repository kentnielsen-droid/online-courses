import streamlit as st

st.title("First page")

x1 = st.session_state.get('x1', None)
x2 = st.session_state.get('x2', None)

if x1 is None or x2 is None:
    st.warning("Please visit the Homepage first to choose your numbers.")
else:
    st.subheader(f"You chose to multiply {x1} with {x2} 👍")
    st.markdown("""#### Check the second page for the result!""")

st.write(st.session_state)