# Streamlit Authentication App

This Streamlit application use the 'Streamlit-Authentictor' module to create a template that provides authentication capabilities, allowing users to register, login, reset passwords, and retrieve forgotten usernames.

## Acknowledgments

- A special thanks to [mkhorasani](https://github.com/mkhorasani) and contributors for their amazing work on this module!
- Check out the full github repo [here](https://github.com/mkhorasani/Streamlit-Authenticator) and go support all the contributors!


## Prerequisites
- Python (>= 3.7)
- pip
- A Gmail account (for SMTP setup)

## Setup

## Setup

1. **Clone the Repository**:
   
   `git clone https://github.com/kyle-mirich/st-authenticator-login-template.git`

2. **Navigate to Project Directory**:

   `cd streamlit-authenticator-login-template`

3. **Install Requirements**:
   
   Navigate to the project directory and run:

   `pip install -r requirements.txt`


4. **Setup Gmail SMTP**:

Before using the email functionalities (e.g., sending reset password emails), you need to set up Gmail's SMTP service:

a. Make sure you have 2-Step Verification enabled for your Google Account.

b. Generate an App Password:
   - Visit [Google Account Settings](https://myaccount.google.com/security).
   - Under "Signing in to Google", select "App Passwords".
   - From the drop-down menu, select "Mail" and generate your App Password.

c. Update `config.yaml`:
   Replace the SMTP section with your Gmail email and the generated App Password:
   ```
   smtp:
      server: smtp.gmail.com
      port: 587
      use_tls: true
      username: your_email@gmail.com
      password: YOUR_APP_PASSWORD
   ```


5. **Run the Streamlit App**:

   `streamlit run login.py`



## Configuration File

The config.yaml file contains configuration details essential for the app. It stores user credentials (hashed) and SMTP details for email notifications. It's crucial to ensure this file is kept secure, especially when working with real credentials.
## Features
- **User Authentication** Securely log in with bycrpty-hased pashwords
- **Password Reset** Allows users to reset their passwords
- **Username Retrieval** In case a user forgets their username, the app orvides a retrieval mechanism
- **User Registration** New users can register and thier details are securely stored
## Usage

- **Login/Register**: Use the provided interface on the app's homepage.
- **Forgot Password**: If you forget your password, use the "Forgot Password" option. Your new password will be emailed to you.
- **Forgot Username**: If you forget your username, use the "Forgot Username" option. Your username will be emailed to you.
## Security

**Warning** Never use your main Gmail password in the 'config.yaml'. Always use the app password generated from Google. Though each password is encrypted, it is still hackable. Warn users to be careful with what passwords they are using!


## Contributing

Feel free to fork this repository, make changes, and submit pull requests. Any contributions are welcome!


