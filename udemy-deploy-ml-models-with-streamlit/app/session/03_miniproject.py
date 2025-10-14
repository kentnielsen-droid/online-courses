import streamlit as st

st.title("Exercise: State Management")

st.subheader("Temperature conversion")

# Initialize state with temperatures.
# Use the freezing point of water
if "celsius" not in st.session_state:
    st.session_state["celsius"] = 0.00
if "farenheit" not in st.session_state:
    st.session_state["farenheit"] = 32.00
if "kelvin" not in st.session_state:
    st.session_state["kelvin"] = 273.15

# Write a callback to convert the temperature in Celsius
# to Farenheit and Kelvin. Change the values in the state
# appropriately


def celsius_conversion():
    celsius = st.session_state["celsius"]

    st.session_state["farenheit"] = (celsius * 9 / 5) + 32
    st.session_state["kelvin"] = celsius + 273.15


# Same thing, but converting from Farenheit to Celsius
# and Kelvin
def farenheit_conversion():
    farenheit = st.session_state["farenheit"]

    st.session_state["celsius"] = (farenheit - 32) * 5 / 9
    st.session_state["kelvin"] = (farenheit - 32) * 5 / 9 + 273.15


# Same thing, but converting from Kelvin to Celsius
# and Farenheint
def kelvin_conversion():
    kelvin = st.session_state["kelvin"]

    st.session_state["celsius"] = kelvin - 273.15
    st.session_state["farenheit"] = (kelvin - 273.15) * 9 / 5 + 32


# Write a callback that adds whatever number the user
# inputs to the Celsius box. Use args.
def add_to_celsius(num):
    st.session_state["celsius"] += num
    celsius_conversion()


# Write a callback to sets the temperatures depending on
# which button the user clicks. Use kwargs.
def set_temperatures(celsius, farenheit, kelvin):
    st.session_state["celsius"] = celsius
    st.session_state["farenheit"] = farenheit
    st.session_state["kelvin"] = kelvin


col1, col2, col3 = st.columns(3)

# Hook up the first 3 callbacks to the input widgets
col1.number_input("Celsius", step=0.01, key="celsius", on_change=celsius_conversion)
col2.number_input(
    "Farenheit", step=0.01, key="farenheit", on_change=farenheit_conversion
)
col3.number_input("Kelvin", step=0.01, key="kelvin", on_change=kelvin_conversion)

# Hook up the 4th callback to the button. Use args.
col1, _, _ = st.columns(3)
num = col1.number_input("Add to Celsius", step=1)
col1.button("Add", type="primary", on_click=add_to_celsius, args=(num,))

col1, col2, col3 = st.columns(3)

# Hook up the last callback to each button. Use kwargs.
col1.button("🧊 Freezing point of water", on_click=set_temperatures, kwargs=dict(celsius= 0.00, farenheit=32.00, kelvin=273.15))
col2.button("🔥 Boiling point of water", on_click=set_temperatures, kwargs=dict(celsius= 100.00, farenheit=212.00, kelvin=373.15))
col3.button("🥶 Absolute zero", on_click=set_temperatures, kwargs=dict(celsius= -273.15, farenheit=-459.67, kelvin=0.00))

st.write(st.session_state)
