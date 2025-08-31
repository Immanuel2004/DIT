# app.py
import streamlit as st
import bcrypt
import secrets
import json
import os
from datetime import datetime, timedelta

# -------------------- Config --------------------
USERS_FILE = "users.json"
LOGS_FILE = "logs.json"


# -------------------- Helpers --------------------
def load_json(file, default):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump(default, f)
        return default
    with open(file, "r") as f:
        return json.load(f)


def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4, default=str)


def get_users():
    return load_json(USERS_FILE, [])


def save_users(users):
    save_json(USERS_FILE, users)


def get_logs():
    return load_json(LOGS_FILE, [])


def save_logs(logs):
    save_json(LOGS_FILE, logs)


# -------------------- Default Admin --------------------
def ensure_admin():
    users = get_users()
    if not any(u["role"] == "admin" for u in users):
        hashed_pw = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        users.append({
            "username": "admin",
            "password_hash": hashed_pw,
            "role": "admin",
            "reset_token": None,
            "token_expiry": None
        })
        save_users(users)
        log_event("system", "Created default admin (admin/admin123)")


# -------------------- Logging --------------------
def log_event(username, action):
    logs = get_logs()
    logs.append({
        "username": username,
        "action": action,
        "timestamp": datetime.now().isoformat()
    })
    save_logs(logs)


# -------------------- Auth Functions --------------------
def login():
    st.subheader("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        users = get_users()
        user = next((u for u in users if u["username"] == username), None)

        if user and bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = user["role"]
            st.session_state.email = username  


            st.session_state.email = username  

            log_event(username, "login")
            st.success(f"Welcome, {username} ({user['role']})")
            st.rerun()
        else:
            st.error("Invalid username or password.")



def signup():
    st.subheader("Sign Up")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")

    if st.button("Create Account"):
        users = get_users()
        if any(u["username"] == username for u in users):
            st.warning("Username already exists.")
            return

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        users.append({
            "username": username,
            "password_hash": hashed_pw,
            "role": "user",
            "reset_token": None,
            "token_expiry": None
        })
        save_users(users)

        log_event(username, "signup")
        st.success("Account created. Please log in.")
        st.session_state.page = "login"


def request_password_reset():
    st.subheader("Request Password Reset")
    username = st.text_input("Enter your username")

    if st.button("Generate Reset Token"):
        users = get_users()
        user = next((u for u in users if u["username"] == username), None)

        if user:
            token = secrets.token_urlsafe(16)
            expiry = datetime.now() + timedelta(minutes=15)
            user["reset_token"] = token
            user["token_expiry"] = expiry.isoformat()
            save_users(users)

            st.success("Reset token generated (Dev mode display below)")
            st.code(token)
            log_event(username, "reset token generated")
        else:
            st.error("Username not found.")


def confirm_password_reset():
    st.subheader("Confirm Password Reset")
    username = st.text_input("Username")
    token = st.text_input("Reset Token")
    new_password = st.text_input("New Password", type="password")

    if st.button("Reset Password"):
        users = get_users()
        user = next((u for u in users if u["username"] == username), None)

        if not user:
            st.error("User not found.")
        elif user.get("reset_token") != token:
            st.error("Invalid reset token.")
        elif not user.get("token_expiry") or datetime.now() > datetime.fromisoformat(user["token_expiry"]):
            st.error("Token expired.")
        else:
            new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            user["password_hash"] = new_hash
            user["reset_token"] = None
            user["token_expiry"] = None
            save_users(users)

            st.success("Password reset successful.")
            log_event(username, "password reset")


def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.email = ""   
        st.rerun()


# -------------------- Admin Views --------------------
def view_users():
    st.subheader("Registered Users")
    users = get_users()
    if users:
        st.table([{"username": u["username"], "role": u["role"]} for u in users])
    else:
        st.info("No users found.")


def view_logs():
    st.subheader("Activity Logs")
    logs = get_logs()
    if logs:
        st.table(logs[::-1])  # newest first
    else:
        st.info("No logs available.")


# -------------------- Main App --------------------
def main():
    st.set_page_config(page_title="Auth System", layout="centered")
    ensure_admin()

    # Session init
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
    if "page" not in st.session_state:
        st.session_state.page = "login"

    # Logged-in view
    if st.session_state.logged_in:
        st.sidebar.success(f"Logged in as {st.session_state.username} ({st.session_state.role})")
        logout()

        st.sidebar.header("Navigation")
        choice = st.sidebar.radio("Go to", ["Dashboard", "Users", "Logs"])

        if choice == "Dashboard":
            st.title("Welcome to the Dashboard")
            st.write("This is your app's main page.")
        elif choice == "Users":
            if st.session_state.role == "admin":
                view_users()
            else:
                st.warning("Only admins can view users.")
        elif choice == "Logs":
            if st.session_state.role == "admin":
                view_logs()
            else:
                st.warning("Only admins can view logs.")

    # Not logged-in view
    else:
        st.sidebar.header("Navigation")
        menu = ["Login", "Sign Up", "Request Password Reset", "Confirm Password Reset"]
        choice = st.sidebar.radio("Choose", menu)

        if choice == "Login":
            login()
        elif choice == "Sign Up":
            signup()
        elif choice == "Request Password Reset":
            request_password_reset()
        elif choice == "Confirm Password Reset":
            confirm_password_reset()


if __name__ == "__main__":
    main()
