import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import yaml
from yaml.loader import SafeLoader
import smtplib
from email.message import EmailMessage


def send_email(subject, body, to_email, config):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = config['smtp']['username']
    msg['To'] = to_email

    with smtplib.SMTP(config['smtp']['server'], config['smtp']['port']) as server:
        if config['smtp']['use_tls']:
            server.starttls()
        server.login(config['smtp']['username'], config['smtp']['password'])
        server.send_message(msg)

def send_reset_password_email(name, new_password, to_email, config):
    subject = "Your New Password"
    body = f"Hey {name},\n\nHere is your new password:\n\n {new_password}\n\nPlease change it once you log in."
    
    send_email(subject, body, to_email, config)


def send_forgot_username_email(name, username, to_email, config):
    subject = "Your Username Reminder"
    body = f"Hey {name},\n\nYour username is: \n\n{username}\n\n"
    
    send_email(subject, body, to_email, config)


# Load the config
def load_config():
    with open('config.yaml') as file:
        return yaml.load(file, Loader=SafeLoader)

# Helper to determine if password is alredy hashed
def is_bcrypt_hash(s):
    return s.startswith(('$2a$', '$2b$', '$2x$', '$2y$')) and len(s) == 60


# Hash new plaintext passwords only
def hash_plaintext_passwords(config):
    plaintext_passwords = {}
    for user, details in config['credentials']['usernames'].items():
        # Check if the password is not a bcrypt hash
        if not is_bcrypt_hash(details['password']):
            plaintext_passwords[user] = details['password']

    if plaintext_passwords:
        hashed_passwords = Hasher(list(plaintext_passwords.values())).generate()
        for user, hashed_pw in zip(plaintext_passwords.keys(), hashed_passwords):
            config['credentials']['usernames'][user]['password'] = hashed_pw

    return config


# Save the config
def save_config(config):
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

config = load_config()

if 'hashed_done' not in st.session_state:
    config = hash_plaintext_passwords(config)
    save_config(config)
    st.session_state.hashed_done = True

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login()

if authentication_status:
    # If the user is authenticated
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{name}*')
    st.title('Some content')  
### FUNCTIONS
    # Reset Password
    if authenticator.reset_password(username):
        save_config(config)
        st.success('Password modified successfully')
    
    # Update User Details
    if authenticator.update_user_details(username):
        save_config(config)
        st.success('Entries updated successfully')

else:
    if st.session_state.get("authentication_status") is False:
        st.error('Username/password is incorrect')
    else:
        st.warning('Please enter your username and password')

    # Register User
    try:
        if authenticator.register_user(pre_authorization=False):
            save_config(config)
            st.success('User registered successfully')  # se queda colgado
    except Exception as e:
        st.error(str(e))

    # Forgot Password
    try:
        username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password()
        if username_forgot_pw:
            user_name = config['credentials']['usernames'][username_forgot_pw]['name']  # Assuming you store the name in the config
            save_config(config)
            # Send the reset password email
            send_reset_password_email(user_name, random_password, email_forgot_password, config)
            st.success('New password sent securely')
        else:
            st.error('Username not found')
    except Exception as e:
        st.error(str(e))


# Forgot Username
try:
    username_forgot_username, email_forgot_username = authenticator.forgot_username()
    if username_forgot_username:
        user_name = config['credentials']['usernames'][username_forgot_username]['name']  # Retrieve the user's name from the config
        save_config(config)
        # Send the email with the username
        send_forgot_username_email(user_name, username_forgot_username, email_forgot_username, config)
        st.success('Username sent securely')
    else:
        st.error('Email not found')
except Exception as e:
    st.error(str(e))

