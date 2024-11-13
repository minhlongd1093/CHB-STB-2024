import streamlit as st
import sqlite3
import hashlib
import pandas as pd

# Database setup
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT, secret_question TEXT, secret_answer TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS assessments
             (username TEXT, assessment_name TEXT, score INTEGER, date TEXT)''')
conn.commit()

# Hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User registration
def register_user():
    st.subheader("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    secret_question = "What is the name of the first school you attended?"
    secret_answer = st.text_input(secret_question).lower().strip()
    if st.button("Register"):
        if username and password and secret_answer:
            hashed_password = hash_password(password)
            try:
                c.execute("INSERT INTO users (username, password, secret_question, secret_answer) VALUES (?, ?, ?, ?)",
                          (username, hashed_password, secret_question, secret_answer))
                conn.commit()
                st.success("Registration successful! Please log in.")
            except sqlite3.IntegrityError:
                st.error("Username already exists. Please choose a different username.")
        else:
            st.error("Please fill all fields.")

# User login
def login_user():
    st.subheader("Login")
    username = st.text_input("Username", key='login_username')
    password = st.text_input("Password", type='password', key='login_password')
    if st.button("Login"):
        if username and password:
            hashed_password = hash_password(password)
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
            user = c.fetchone()
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success(f"Welcome back, {username}!")
            else:
                st.error("Incorrect username or password.")
        else:
            st.error("Please enter both username and password.")

# Password reset function
def reset_password():
    st.subheader("Reset Password")
    username = st.text_input("Username", key='reset_username')
    secret_answer = st.text_input("Answer to your secret question").lower().strip()
    new_password = st.text_input("New Password", type='password')
    if st.button("Reset Password"):
        c.execute("SELECT secret_answer FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        if result and result[0] == secret_answer:
            hashed_password = hash_password(new_password)
            c.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
            conn.commit()
            st.success("Your password has been reset. Please log in.")
        else:
            st.error("Incorrect username or secret answer.")

# Function to display assessments
def display_assessment(assessment_name, questions, options, scores, interpretation_func):
    st.subheader(f"{assessment_name}")
    responses = {}
    for i, question in enumerate(questions):
        st.write(f"Q{i+1}: {question}")
        response = st.radio("", options, key=f"{assessment_name}_q{i+1}")
        responses[f"Q{i+1}"] = response
    if st.button(f"Submit {assessment_name}"):
        if None in responses.values() or '' in responses.values():
            st.error("Please answer all questions before submitting.")
        else:
            total_score = sum([scores[response] for response in responses.values()])
            interpretation_func(total_score)
            # Save results
            if 'username' in st.session_state:
                c.execute("INSERT INTO assessments (username, assessment_name, score, date) VALUES (?, ?, ?, date('now'))",
                          (st.session_state['username'], assessment_name, total_score))
                conn.commit()

# Interpretation functions (updated to include resources)
def interpret_rses(score):
    st.write(f"Your RSES score is: {score}")
    if score <= 15:
        st.write("Interpretation: Low self-esteem.")
        st.write("Consider speaking with a mental health professional.")
        st.write("[Find a therapist](https://www.psychologytoday.com/)")
    else:
        st.write("Interpretation: Normal self-esteem.")

def interpret_stai(score):
    st.write(f"Your STAI-YB score is: {score}")
    if score >= 60:
        st.write("Interpretation: High anxiety.")
        st.write("Consider techniques for anxiety management or seek professional help.")
        st.write("[Anxiety resources](https://www.mentalhealth.org.uk/a-to-z/a/anxiety)")
    elif 40 <= score < 60:
        st.write("Interpretation: Moderate anxiety.")
        st.write("Consider stress-reduction activities.")
    else:
        st.write("Interpretation: Low anxiety.")

def interpret_phq9(score):
    st.write(f"Your PHQ-9 score is: {score}")
    if score >= 20:
        st.write("Interpretation: Severe depression.")
        st.write("We recommend seeking professional help immediately.")
        st.write("[Find a therapist](https://www.psychologytoday.com/)")
    elif 15 <= score < 20:
        st.write("Interpretation: Moderately severe depression.")
        st.write("Consider speaking with a mental health professional.")
    elif 10 <= score < 15:
        st.write("Interpretation: Moderate depression.")
        st.write("Consider lifestyle changes and monitoring your mood.")
    elif 5 <= score < 10:
        st.write("Interpretation: Mild depression.")
        st.write("Consider self-help strategies.")
    else:
        st.write("Interpretation: Minimal depression.")

def interpret_cssrs(score):
    st.write(f"Your C-SSRS score is: {score}")
    if score >= 4:
        st.write("Interpretation: High risk of suicidal ideation.")
        st.write("Please seek immediate professional help.")
        st.write("[Suicide Prevention Lifeline](https://suicidepreventionlifeline.org/)")
    elif 2 <= score < 4:
        st.write("Interpretation: Moderate risk of suicidal ideation.")
        st.write("Consider speaking with a mental health professional.")
    else:
        st.write("Interpretation: Low risk of suicidal ideation.")

# View assessment history
def view_history():
    st.subheader("Your Assessment History")
    c.execute("SELECT assessment_name, score, date FROM assessments WHERE username = ?", (st.session_state['username'],))
    data = c.fetchall()
    if data:
        df = pd.DataFrame(data, columns=['Assessment', 'Score', 'Date'])
        st.table(df)
    else:
        st.write("You have no assessment history.")

# Update profile function
def update_profile():
    st.subheader("Update Profile")
    new_password = st.text_input("New Password", type='password')
    confirm_password = st.text_input("Confirm New Password", type='password')
    if st.button("Update Password"):
        if new_password and confirm_password:
            if new_password == confirm_password:
                hashed_password = hash_password(new_password)
                c.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, st.session_state['username']))
                conn.commit()
                st.success("Your password has been updated.")
            else:
                st.error("Passwords do not match.")
        else:
            st.error("Please enter and confirm your new password.")

# Main App
def main():
    st.title("Falcon Wellness Check-In Tool")
    st.write("An easy-to-use application designed to help you gain insights into your overall well-being.")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        choice = st.selectbox("Login or Register", ["Login", "Register", "Forgot Password"])
        if choice == "Login":
            login_user()
        elif choice == "Register":
            register_user()
        else:
            reset_password()
    else:
        st.sidebar.title(f"Welcome, {st.session_state['username']}")
        menu_choice = st.sidebar.radio("Navigate", ["Home", "Take Assessment", "View History", "Profile", "Logout"])

        if menu_choice == "Home":
            st.write("Select an option from the sidebar.")
        elif menu_choice == "Take Assessment":
            assessment_choice = st.selectbox("Choose an Assessment", ["RSES", "STAI-YB", "PHQ-9", "C-SSRS"])
            if assessment_choice == "RSES":
                # Note: Replace sample questions with full RSES questions
                RSES_QUESTIONS = [
                    "I feel that I am a person of worth, at least on an equal plane with others.",
                    "I feel that I have a number of good qualities.",
                    "All in all, I am inclined to feel that I am a failure.",
                    "I am able to do things as well as most other people.",
                    "I feel I do not have much to be proud of.",
                    "I take a positive attitude toward myself.",
                    "On the whole, I am satisfied with myself.",
                    "I wish I could have more respect for myself.",
                    "I certainly feel useless at times.",
                    "At times, I think I am no good at all."
                    # ... Add the rest of the RSES questions here
                ]
                OPTIONS = ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"]
                SCORES = {"Strongly Agree": 3, "Agree": 2, "Disagree": 1, "Strongly Disagree": 0}
                display_assessment(
                    "Rosenberg Self-Esteem Scale (RSES)",
                    RSES_QUESTIONS,
                    OPTIONS,
                    SCORES,
                    interpret_rses
                )
            elif assessment_choice == "STAI-YB":
                # Note: Replace sample questions with full STAI-YB questions
                STAI_QUESTIONS = [
                    "I feel calm.",
                    "I feel secure.",
                    "I am tense.",
                    "I feel strained.",
                    "I feel at ease.",
                    "I feel upset.",
                    "I am presently worrying over possible misfortunes.",
                    "I feel satisfied.",
                    "I feel frightened.",
                    "I feel comfortable.",
                    "I feel self-confident.",
                    "I feel nervous.",
                    "I am jittery.",
                    "I feel indecisive.",
                    "I am relaxed.",
                    "I feel content.",
                    "I am worried.",
                    "I feel confused.",
                    "I feel steady.",
                    "I feel pleasant."
                    # ... Add the rest of the STAI-YB questions here
                ]
                OPTIONS = ["Almost Always", "Often", "Sometimes", "Rarely"]
                SCORES = {"Almost Always": 4, "Often": 3, "Sometimes": 2, "Rarely": 1}
                display_assessment(
                    "State-Trait Anxiety Inventory (STAI-YB)",
                    STAI_QUESTIONS,
                    OPTIONS,
                    SCORES,
                    interpret_stai
                )
            elif assessment_choice == "PHQ-9":
                # Note: Replace sample questions with full PHQ-9 questions
                PHQ9_QUESTIONS = [
                    "Little interest or pleasure in doing things?",
                    "Feeling down, depressed, or hopeless?",
                    "Trouble falling or staying asleep, or sleeping too much?",
                    "Feeling tired or having little energy?",
                    "Poor appetite or overeating?",
                    "Feeling bad about yourself – or that you are a failure or have let yourself or your family down?",
                    "Trouble concentrating on things, such as reading the newspaper or watching television?",
                    "Moving or speaking so slowly that other people could have noticed? Or the opposite – being so fidgety or restless that you have been moving around a lot more than usual?",
                    "Thoughts that you would be better off dead or of hurting yourself in some way?"
                    # ... Add the rest of the PHQ-9 questions here
                ]
                OPTIONS = ["Not at all", "Several days", "More than half the days", "Nearly every day"]
                SCORES = {"Not at all": 0, "Several days": 1, "More than half the days": 2, "Nearly every day": 3}
                display_assessment(
                    "Patient Health Questionnaire-9 (PHQ-9)",
                    PHQ9_QUESTIONS,
                    OPTIONS,
                    SCORES,
                    interpret_phq9
                )
            elif assessment_choice == "C-SSRS":
                # Note: Replace sample questions with full C-SSRS questions
                CSSRS_QUESTIONS = [
                    "Have you wished you were dead or wished you could go to sleep and not wake up?",
                    "Have you actually had any thoughts of killing yourself?",
                    "Have you been thinking about how you might kill yourself?",
                    "Have you had these thoughts and had some intention of acting on them?",
                    "Have you started to work out or worked out the details of how to kill yourself?",
                    "Have you done anything, started to do anything, or prepared to do anything to end your life?"
                    # ... Add the rest of the C-SSRS questions here
                ]
                OPTIONS = ["Yes", "No"]
                SCORES = {"Yes": 2, "No": 0}
                display_assessment(
                    "Columbia-Suicide Severity Rating Scale (C-SSRS)",
                    CSSRS_QUESTIONS,
                    OPTIONS,
                    SCORES,
                    interpret_cssrs
                )
        elif menu_choice == "View History":
            view_history()
        elif menu_choice == "Profile":
            update_profile()
        elif menu_choice == "Logout":
            st.session_state['logged_in'] = False
            st.session_state['username'] = ''
            st.success("You have been logged out.")
            st.experimental_rerun()  # Refresh the page

if __name__ == "__main__":
    main()
