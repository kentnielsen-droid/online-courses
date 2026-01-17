import streamlit as st
from yaml import dump, load
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

#hashed_pwd = stauth.Hasher(['12345']).generate()

with open('config.yaml') as file:
    config = load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login('Login', 'main')
if st.session_state['authentication_status']:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome {st.session_state["name"]}')
    st.title('Some content')
elif not st.session_state['authentication_status']:
    st.error('Username/Password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')


# Password reset widget
if authentication_status:
    try:
        if authenticator.reset_password(username, 'Reset password'):
            with open('config.yaml', 'w') as file:
                dump(config, file, default_flow_style=False)
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)

# Register new user
try:
    if authenticator.register_user('Register user', preauthorization=False):
        with open('config.yaml', 'w') as file:
            dump(config, file, default_flow_style=False)
        st.success('User registered successfully')
except Exception as e:
    st.error(e)

# Forgot password widget
try:
    username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password(
        'Forgot password')
    if username_of_forgotten_password:
        st.success('New password sent securely')
        # Random password to be transferred to user securely
    else:
        st.error('Username not found')
except Exception as e:
    st.error(e)

# Forgot username
try:
    username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username(
        'Forgot username')
    if username_of_forgotten_username:
        st.success('Username sent securely')
        # Username to be transferred to user securely
    else:
        st.error('Email not found')
except Exception as e:
    st.error(e)

# Update user details
if authentication_status:
    try:
        if authenticator.update_user_details(username, 'Update user details'):
            with open('config.yaml', 'w') as file:
                dump(config, file, default_flow_style=False)
            st.success('Entries updated successfully')
    except Exception as e:
        st.error(e)


st.write(st.session_state)