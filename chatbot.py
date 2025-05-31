import streamlit as st
import json

# Define the knowledge base for the chatbot (no changes here)
KNOWLEDGE_BASE = {
    "greeting": {
        "patterns": ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"],
        "responses": ["Hello! I'm your Heart Disease Assistant. How can I help you today?", 
                     "Hi there! I can help you understand heart disease and this dataset. What would you like to know?"]
    },
    "farewell": {
        "patterns": ["bye", "goodbye", "see you", "thank you", "thanks"],
        "responses": ["Goodbye! Take care of your heart!", 
                     "Thank you for chatting! Stay healthy!"]
    },
    "dataset_info": {
        "patterns": ["what is this dataset", "tell me about the data", "what data are you using", "dataset information"],
        "responses": ["This is the Cleveland Heart Disease dataset, containing 303 patient records with 14 features including age, sex, chest pain type, and other medical indicators."]
    },
    "features": {
        "patterns": ["what are the features", "what variables are used", "what data is collected", "what information is in the dataset"],
        "responses": ["The dataset includes these key features:\n"
                     "1. Age\n"
                     "2. Sex (0=Female, 1=Male)\n"
                     "3. Chest Pain Type (0-3)\n"
                     "4. Resting Blood Pressure\n"
                     "5. Cholesterol\n"
                     "6. Fasting Blood Sugar\n"
                     "7. Resting ECG Results\n"
                     "8. Maximum Heart Rate\n"
                     "9. Exercise-Induced Angina\n"
                     "10. ST Depression\n"
                     "11. Slope of Peak Exercise ST\n"
                     "12. Number of Major Vessels\n"
                     "13. Thalassemia"]
    },
    "prediction_info": {
        "patterns": ["how does prediction work", "how do you predict", "what is the model", "how accurate is the prediction"],
        "responses": ["The prediction is made using a Random Forest Classifier, which is a machine learning model that uses multiple decision trees. "
                     "The model is trained on the dataset and can predict the likelihood of heart disease based on the input features. "
                     "The accuracy varies but is typically around 80-85%."]
    },
    "heart_disease_info": {
        "patterns": ["what is heart disease", "tell me about heart disease", "heart disease information"],
        "responses": ["Heart disease refers to several types of heart conditions. The most common is coronary artery disease, "
                     "which can lead to heart attack. Risk factors include high blood pressure, high cholesterol, smoking, "
                     "obesity, and lack of physical activity."]
    },
    "prevention": {
        "patterns": ["how to prevent heart disease", "prevention tips", "how to avoid heart disease"],
        "responses": ["To prevent heart disease:\n"
                     "1. Maintain a healthy diet\n"
                     "2. Exercise regularly\n"
                     "3. Don't smoke\n"
                     "4. Maintain a healthy weight\n"
                     "5. Control blood pressure and cholesterol\n"
                     "6. Get regular check-ups"]
    },
    "default": {
        "patterns": [],
        "responses": ["I'm not sure I understand. Could you please rephrase your question? "
                     "I can help you with information about the dataset, heart disease, or the prediction model."]
    }
}

def get_response(user_input):
    """Get a response from the chatbot based on user input."""
    user_input = user_input.lower().strip()
    
    # Check each category in the knowledge base
    for category, data in KNOWLEDGE_BASE.items():
        if any(pattern in user_input for pattern in data["patterns"]):
            return data["responses"][0]  # Return the first response for simplicity
    
    # If no match is found, return the default response
    return KNOWLEDGE_BASE["default"]["responses"][0]

# --- IMPORTANT: Keep this function if it's called elsewhere in your app.
# If not, and its logic is fully handled by display_fullpage_chat, it can be removed.
def initialize_chat_history():
  """Initialize the chat history in the session state if it doesn't exist."""
  if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --- Corrected Chatbot Display Function ---

def display_fullpage_chat():
    st.title("Heart Disease Assistant Chatbot")
    st.markdown("Ask me anything about heart disease or the dataset.")

    # Initialize chat history with the initial assistant message if it's empty
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Hello! I'm your Heart Disease Assistant. How can I help you today?"}
        ]

    # Use st.columns to push the chat input to the bottom
    # This creates a structure where the input is 'fixed' by design
    # and the content above it scrolls.
    
    # Placeholder for chat messages. This will expand and scroll.
    # No fixed height container here initially to let Streamlit handle the full page scroll naturally.
    # We will let the chat messages occupy the natural height of the page.
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Use a permanent placeholder for the chat input at the very bottom
    # This method is better for sticky inputs in Streamlit
    st.markdown("---") # Optional: A separator line
    chat_input_placeholder = st.empty() # Create an empty slot for the input

    with chat_input_placeholder.container():
        # Accept user input at the bottom
        user_input = st.chat_input("Type your message here...", key="fullpage_chat_input")

        if user_input:
            # Add user message to chat history
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            # Get bot response
            bot_response = get_response(user_input)
            # Add assistant response to chat history
            st.session_state.chat_messages.append({"role": "assistant", "content": bot_response})
            # Rerun the app to display the new messages immediately
            st.rerun()
