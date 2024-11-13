import streamlit as st

# Initialize session state
if 'page' not in st.session_state:
    st.session_state['page'] = 1
    st.session_state['results'] = {}

# Function to navigate to the next page
def next_page():
    st.session_state['page'] += 1

# Function to store results
def store_results(test_name, result):
    st.session_state['results'][test_name] = result
    next_page()

# Test 1: PHQ-9
def phq9_page():
    st.title("PHQ-9: Depression Assessment")
    st.write("Answer the following questions based on how you've felt over the past 2 weeks.")
    
    scores = []
    questions = [
        "Little interest or pleasure in doing things.",
        "Feeling down, depressed, or hopeless.",
        "Trouble falling or staying asleep, or sleeping too much.",
        "Feeling tired or having little energy.",
        "Poor appetite or overeating.",
        "Feeling bad about yourself — or that you are a failure.",
        "Trouble concentrating on things, such as reading or watching television.",
        "Moving or speaking slowly, or being fidgety or restless.",
        "Thoughts of being better off dead or self-harm."
    ]
    
    for question in questions:
        scores.append(st.radio(question, ["Not at all", "Several days", "More than half the days", "Nearly every day"], index=0))
    
    if st.button("Next"):
        numeric_scores = [scores.index(choice) for choice in scores]
        store_results("PHQ-9", sum(numeric_scores))

# Test 2: Rosenberg Self-Esteem Scale
def rosenberg_page():
    st.title("Rosenberg Self-Esteem Scale")
    st.write("Rate the following statements.")
    
    scores = []
    questions = [
        "I am satisfied with myself.",
        "At times, I think I am no good at all.",
        "I have a number of good qualities.",
        "I can do things as well as most people.",
        "I feel I do not have much to be proud of.",
        "I feel useless at times.",
        "I feel that I’m a person of worth.",
        "I wish I could have more respect for myself.",
        "I feel like a failure.",
        "I take a positive attitude toward myself."
    ]
    
    for question in questions:
        scores.append(st.radio(question, ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"], index=0))
    
    if st.button("Next"):
        numeric_scores = [(1 if i in [1, 4, 5, 7, 8] else 0) + scores.index(choice) for i, choice in enumerate(scores)]
        store_results("Rosenberg", sum(numeric_scores))

# Test 3: STAI-5
def stai5_page():
    st.title("STAI-5: Anxiety Assessment")
    st.write("Answer the following questions about how you generally feel.")
    
    scores = []
    questions = [
        "I feel calm.",
        "I feel secure.",
        "I feel tense.",
        "I feel upset.",
        "I feel worried."
    ]
    
    for question in questions:
        scores.append(st.radio(question, ["Almost Never", "Sometimes", "Often", "Almost Always"], index=0))
    
    if st.button("Next"):
        numeric_scores = [4 - scores.index(choice) if i in [0, 1] else scores.index(choice) + 1 for i, choice in enumerate(scores)]
        store_results("STAI-5", sum(numeric_scores))

# Test 4: C-SSRS
def cssrs_page():
    st.title("Columbia Suicide Severity Rating Scale (C-SSRS)")
    st.write("Answer Yes or No for the following questions.")
    
    scores = []
    questions = [
        "Have you wished you were dead?",
        "Have you had thoughts about killing yourself?",
        "Have you thought about how you might do this?",
        "Have you had these thoughts with intention?",
        "Have you started to work out the details?",
        "Have you done anything to end your life?"
    ]
    
    for question in questions:
        scores.append(st.radio(question, ["No", "Yes"], index=0))
    
    if st.button("Next"):
        numeric_scores = [1 if choice == "Yes" else 0 for choice in scores]
        store_results("C-SSRS", sum(numeric_scores))

# Feedback and Interpretation Page
def feedback_page():
    st.title("Feedback and Interpretation")
    
    results = st.session_state['results']
    
    st.subheader("PHQ-9 Results")
    st.write(f"Score: {results['PHQ-9']}")
    # Provide feedback interpretation...
    
    st.subheader("Rosenberg Self-Esteem Scale Results")
    st.write(f"Score: {results['Rosenberg']}")
    # Provide feedback interpretation...
    
    st.subheader("STAI-5 Results")
    st.write(f"Score: {results['STAI-5']}")
    # Provide feedback interpretation...
    
    st.subheader("C-SSRS Results")
    st.write(f"Score: {results['C-SSRS']}")
    # Provide feedback interpretation...

# Page navigation
if st.session_state['page'] == 1:
    phq9_page()
elif st.session_state['page'] == 2:
    rosenberg_page()
elif st.session_state['page'] == 3:
    stai5_page()
elif st.session_state['page'] == 4:
    cssrs_page()
else:
    feedback_page()
