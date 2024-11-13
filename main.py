import streamlit as st

def main():
    st.title("Mental Health Assessment App")
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Baseline Suicidal Thoughts (C-SSRS)", "Trait Anxiety (STAI-YB)", 
                                      "Depression Symptoms (PHQ-9, BDI)", "Self-Esteem (RSES)", "Results"])
    
    if page == "Home":
        st.header("Welcome")
        st.write("This app will guide you through mental health assessments:")
        st.markdown("""
        1. **Baseline Suicidal Thoughts** (Columbia-Suicide Severity Rating Scale)
        2. **Trait Anxiety** (Spielberger State-Trait Anxiety Inventory)
        3. **Depression Symptoms** (PHQ-9, Beck Depression Inventory)
        4. **Self-Esteem** (Rosenberg Self-Esteem Scale)
        """)
    
    elif page == "Baseline Suicidal Thoughts (C-SSRS)":
        st.header("Baseline Suicidal Thoughts")
        q1 = st.radio("1) Have you wished you were dead or wished you could go to sleep and not wake up?", ["Yes", "No"])
        q2 = st.radio("2) Have you actually had any thoughts about killing yourself?", ["Yes", "No"])
        
        if q2 == "Yes":
            q3 = st.radio("3) Have you been thinking about how you might do this?", ["Yes", "No"])
            q4 = st.radio("4) Have you had these thoughts and had some intention of acting on them?", ["Yes", "No"])
            q5 = st.radio("5) Have you started to work out or worked out the details of how to kill yourself? Did you intend to carry out this plan?", ["Yes", "No"])
        
        q6 = st.radio("6) Have you done anything, started to do anything, or prepared to do anything to end your life?", ["Yes", "No"])
    
    elif page == "Trait Anxiety (STAI-YB)":
        st.header("Trait Anxiety")
        st.write("Please answer the following questions using the provided scale:")
        st.write("1 = Not at all, 2 = Somewhat, 3 = Moderately, 4 = Very much")
        anxiety_scores = []
        for i in range(1, 21):
            anxiety_scores.append(st.slider(f"Question {i}", 1, 4, 2))
    
    elif page == "Depression Symptoms (PHQ-9, BDI)":
        st.header("Depression Symptoms")
        st.subheader("PHQ-9")
        phq_scores = []
        for i in range(1, 10):
            phq_scores.append(st.slider(f"Question {i}", 0, 3, 1, format="%d"))
        
        st.subheader("Beck Depression Inventory")
        bdi_scores = []
        for i in range(1, 22):
            bdi_scores.append(st.slider(f"Question {i}", 0, 3, 1))
    
    elif page == "Self-Esteem (RSES)":
        st.header("Self-Esteem")
        st.write("Please answer the following using the scale: 1 = Strongly Agree, 2 = Agree, 3 = Disagree, 4 = Strongly Disagree")
        self_esteem_scores = []
        for i in range(1, 11):
            self_esteem_scores.append(st.slider(f"Question {i}", 1, 4, 2))
    
    elif page == "Results":
        st.header("Results")
        st.write("Results will be calculated based on your responses. This section will display a summary.")
        st.write("**Note**: For actual use, consult a professional for accurate interpretation.")

if __name__ == "__main__":
    main()
