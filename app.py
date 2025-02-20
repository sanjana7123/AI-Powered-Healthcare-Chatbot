import streamlit as st
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import time

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load a pre-trained Hugging Face model
chatbot = pipeline("text-generation", model="gpt2", device=-1)

# Define healthcare-specific response logic
def healthcare_chatbot(user_input):
    if "symptom" in user_input:
        return "It seems like you're experiencing symptoms. Please consult a doctor for accurate advice."
    elif "appointment" in user_input:
        return "Would you like me to schedule an appointment with a doctor?"
    elif "medication" in user_input:
        return "It's important to take your prescribed medications regularly. If you have concerns, consult your doctor."
    elif "diet" in user_input:
        return "A balanced diet is essential for good health. Consider consulting a nutritionist for personalized advice."
    elif "exercise" in user_input:
        return "Regular exercise is important for maintaining health. Aim for at least 30 minutes of physical activity most days."
    else:
        response = chatbot(user_input, max_length=300, num_return_sequences=1)
        return response[0]['generated_text']

# Streamlit web app interface
def main():
    # AI Disclaimer with styling
    st.markdown(
        """
        <div style='background-color:#e3f2fd; padding:10px; padding-bottom:3px; border-radius:10px;'>
            <p><span style='color:#1E88E5; font-style:italic; text-decoration:underline;'>Note:</span> 
            This is an AI-powered chatbot. Please consult a healthcare professional for medical advice.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.title("Healthcare Assistant Chatbot")

    # Initialize session state
    if "chat_started" not in st.session_state:
        st.session_state.chat_started = False
    if "messages" not in st.session_state:
        st.session_state.messages = []  # Store chat history
    if "end_chat" not in st.session_state:
        st.session_state.end_chat = False  
    if st.session_state.end_chat:
        st.write("Thank you for using the Healthcare Assistant Chatbot! ")
        feedback_text = st.text_area("Any suggestions to improve?", "")

        if st.button("Submit Feedback"):
            if feedback_text:
                st.success("Thank you for your feedback! 😊")
            else:
                st.warning("Please provide feedback before submitting.")
        return  

    # If chat is not ended, show chat UI
    user_input = st.text_input("How can I assist you today?", "")

    if st.button("Submit"):
        if user_input:
            with st.spinner("Processing your query, please wait..."):
                time.sleep(2)  
                response = healthcare_chatbot(user_input)

            st.session_state.messages.append(("User", user_input))
            st.session_state.messages.append(("Healthcare Assistant", response))

            st.session_state.chat_started = True

    # Display chat history
    for role, msg in st.session_state.messages:
        st.write(f"**{role}:** {msg}")

    if st.session_state.chat_started:
        if st.button("End Chat"):
            st.session_state.end_chat = True  
            st.session_state.messages = []  
            st.rerun()  
if __name__ == "__main__":
    main()
