# Instagram Unfollowers Checker

This application checks your Instagram account for users you are following but who do not follow you back. It uses the Instagram API to fetch followers and following lists and then compares them to find non-followers.

## Features

- Login to Instagram
- Retrieve followers and following lists
- Identify users who do not follow you back
- Display unfollowers with a link to their Instagram profile

## Security and Privacy

- No shady stuff: This application does not store your username or password anywhere.
- Your credentials are used only to log in to Instagram and are not saved or shared.

## Requirements

- Python 3.6 or higher
- pip (Python package installer)

## Setup

1. **Clone the repository**

2. **Create and activate a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. **Run the `unfollowers.py` script**:
    ```bash
    python unfollowers.py
    ```

2. **Follow the prompts to enter your Instagram username and password**:
    - Enter your Instagram username when prompted.
    - Enter your Instagram password when prompted (input will be hidden for security).

3. **View the output**:
    - The script will display the number of users you are following and the number of followers.
    - It will then list the users who do not follow you back along with a link to their Instagram profile.
