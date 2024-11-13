import streamlit as st

# Data for the assessments
assessment_data = {
    "RSES": {
        "title": "Rosenberg Self-Esteem Scale (RSES)",
        "questions": [
            "I feel that I am a person of worth, at least on an equal plane with others.",
            "I feel that I have a number of good qualities.",
            "All in all, I am inclined to feel that I am a failure.",
            "I am able to do things as well as most other people.",
            "I feel I do not have much to be proud of.",
            "I take a positive attitude toward myself.",
            "On the whole, I am satisfied with myself.",
            "I wish I could have more respect for myself.",
            "I certainly feel useless at times.",
            "At times I think I am no good at all."
        ],
        "options": ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"]
    },
    "STAI": {
        "title": "State-Trait Anxiety Inventory (STAI-YB)",
        "questions": [
            "I feel nervous and restless.",
            "I feel satisfied with myself.",
            "I feel that difficulties are piling up so that I cannot overcome them.",
            "I feel calm and secure."
        ],
        "options": ["Almost Always", "Often", "Sometimes", "Rarely"]
    },
    "PHQ9": {
        "title": "Patient Health Questionnaire-9 (PHQ-9)",
        "questions": [
            "Little interest or pleasure in doing things?",
            "Feeling down, depressed, or hopeless?",
            "Trouble falling or staying asleep, or sleeping too much?",
            "Feeling tired or having little energy?",
            "Poor appetite or overeating?",
            "Feeling bad about yourself or that you are a failure?",
            "Trouble concentrating on things?",
            "Moving or speaking so slowly that others notice?",
            "Thoughts that you would be better off dead?"
        ],
        "options": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
    },
    "C-SSRS": {
        "title": "Columbia-Suicide Severity Rating Scale (C-SSRS)",
        "questions": [
            "Have you wished you were dead or wished you could go to sleep and not wake up?",
            "Have you had actual thoughts of killing yourself?",
            "Have you been thinking about how you might do this?",
            "Have you had these thoughts and had some intention of acting on them?",
            "Have you started to work out or worked out the details of how to kill yourself?"
        ],
        "options": ["Yes", "No"]
    }
}

# Initialize session state for tracking responses
if 'assessment' not in st.session_state:
    st.session_state.assessment = list(assessment_data.keys())[0]
if 'responses' not in st.session_state:
    st.session_state.responses = {key: [] for key in assessment_data.keys()}
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

def next_question():
    response = st.session_state.response
    if response:
        current_assessment = st.session_state.assessment
        st.session_state.responses[current_assessment].append(response)
        st.session_state.current_question += 1
        if st.session_state.current_question >= len(assessment_data[current_assessment]['questions']):
            # Move to next assessment
            current_index = list(assessment_data.keys()).index(current_assessment)
            if current_index + 1 < len(assessment_data):
                st.session_state.assessment = list(assessment_data.keys())[current_index + 1]
                st.session_state.current_question = 0
            else:
                st.session_state.assessment = None  # Mark completion
        st.session_state.response = None  # Reset response
    else:
        st.warning("Please select an option before proceeding.")

def display_results():
    st.title("Assessment Results")
    for assessment, answers in st.session_state.responses.items():
        st.subheader(assessment_data[assessment]['title'])
        for i, answer in enumerate(answers):
            st.write(f"Q{i+1}: {answer}")

# Main app logic
st.title("Mental Health Assessments")

if st.session_state.assessment:
    assessment = st.session_state.assessment
    data = assessment_data[assessment]
    st.header(data['title'])
    
    question = data['questions'][st.session_state.current_question]
    st.write(f"Question {st.session_state.current_question + 1}: {question}")
    
    st.radio("Select your response:", data['options'], key='response')
    
    st.button("Next", on_click=next_question)
else:
    display_results()
