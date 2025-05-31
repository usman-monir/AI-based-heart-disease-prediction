import streamlit as st
import json
import re # Import the regular expression module

# Define the knowledge base for the chatbot
KNOWLEDGE_BASE = {
    "greeting": {
        "patterns": ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening", 
                    "how are you", "whats up", "howdy", "hi there", "hello there", "hey there", 
                    "good day", "greetings", "hiya", "yo", "sup"],
        "responses": ["Hello! I'm your Heart Disease Assistant. How can I help you today?", 
                     "Hi there! I can help you understand heart disease and this dataset. What would you like to know?"]
    },
    "farewell": {
        "patterns": ["bye", "goodbye", "see you", "later", "thank you", "thanks", "cheers", "exit", "quit", "done",
                    "thank you so much", "thanks a lot", "appreciate it", "goodbye for now", "see you later",
                    "take care", "have a good day", "have a nice day", "bye bye", "see ya"],
        "responses": ["Goodbye! Take care of your heart!", 
                     "Thank you for chatting! Stay healthy!"]
    },
    "dataset_info": {
        "patterns": ["what is this dataset", "tell me about the data", "what data are you using", "dataset information", 
                    "about the dataset", "source of the data", "dataset details", "info about the data", 
                    "where does the data come from", "what is the cleveland dataset", "cleveland heart disease data",
                    "tell me about cleveland dataset", "what is the source", "data source", "data origin",
                    "where is the data from", "what is this data about", "explain the dataset"],
        "responses": ["This is the Cleveland Heart Disease dataset, containing 303 patient records with 14 features including age, sex, chest pain type, and other medical indicators."]
    },
    "features": {
        "patterns": ["what are the features", "what variables are used", "what data is collected", "what information is in the dataset", 
                    "dataset columns", "features in the data", "variables in the dataset", "columns in the data", 
                    "list of features", "what features are used", "what variables are included", "what data points are collected",
                    "tell me about the features", "explain the features", "what information is collected", "what measurements are taken",
                    "what are the input variables", "what are the predictors", "what factors are considered"],
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
        "patterns": ["how does prediction work", "how do you predict", "what is the model", "how accurate is the prediction", 
                    "tell me about prediction", "prediction model", "model accuracy", "how is heart disease predicted", 
                    "what machine learning model is used", "model performance", "how does the model work", "prediction accuracy",
                    "what algorithm is used", "how reliable is the prediction", "prediction reliability", "model reliability",
                    "how good is the model", "prediction quality", "model quality", "what's the prediction method"],
        "responses": ["The prediction is made using a Random Forest Classifier, which is a machine learning model that uses multiple decision trees. "
                     "The model is trained on the dataset and can predict the likelihood of heart disease based on the input features. "
                     "The accuracy varies but is typically around 80-85%."]
    },
    "heart_disease_info": {
        "patterns": ["what is heart disease", "tell me about heart disease", "heart disease information", "about heart disease", 
                    "explain heart disease", "what is coronary artery disease", "risk factors for heart disease",
                    "what causes heart disease", "heart disease causes", "heart disease risk factors", "heart disease symptoms",
                    "what are the symptoms", "how does heart disease develop", "heart disease development", "heart disease types",
                    "different types of heart disease", "heart disease complications", "heart disease effects", "heart disease impact"],
        "responses": ["Heart disease refers to several types of heart conditions. The most common is coronary artery disease, "
                     "which can lead to heart attack. Risk factors include high blood pressure, high cholesterol, smoking, "
                     "obesity, and lack of physical activity."]
    },
    "prevention": {
        "patterns": ["how to prevent heart disease", "prevention tips", "how to avoid heart disease", "preventing heart disease", 
                    "tips to prevent heart disease", "how to reduce risk", "preventative measures", "heart disease prevention",
                    "ways to prevent heart disease", "prevention methods", "how to stay heart healthy", "heart health tips",
                    "maintaining heart health", "heart healthy lifestyle", "heart disease risk reduction", "lower heart disease risk",
                    "heart disease prevention strategies", "preventive care for heart", "heart health maintenance"],
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
        "responses": ["I'm not sure I understand. Could you try rephrasing that? "
                     "I can help you with information about the dataset, heart disease, or the prediction model."]
    }
}

# Add example prompts for the default response
EXAMPLE_PROMPTS = [
    "Tell me about the dataset",
    "What are the features?",
    "How does prediction work?",
    "What is heart disease?",
    "How to prevent heart disease?",
    "What causes heart disease?",
    "What are the risk factors?",
    "How accurate is the model?",
    "What is the data source?",
    "What are the symptoms?",
    "How to maintain heart health?",
    "What is coronary artery disease?",
    "How does the model predict?",
    "What measurements are taken?",
    "How to reduce heart disease risk?"
]

def get_response(user_input):
    """
    Get a response from the chatbot based on user input,
    prioritizing direct matches and then keyword matches.
    """
    user_input_lower = user_input.lower().strip()
    
    # 1. Try to find an exact pattern match first (most specific)
    for category, data in KNOWLEDGE_BASE.items():
        if any(user_input_lower == pattern.lower() for pattern in data["patterns"]):
            return data["responses"][0]
    
    # 2. Try to find a keyword/phrase match within the input
    # First, create a mapping of key terms to categories
    key_terms = {
        "dataset": "dataset_info",
        "data": "dataset_info",
        "features": "features",
        "variables": "features",
        "columns": "features",
        "predict": "prediction_info",
        "model": "prediction_info",
        "accuracy": "prediction_info",
        "heart": "heart_disease_info",
        "disease": "heart_disease_info",
        "coronary": "heart_disease_info",
        "prevent": "prevention",
        "prevention": "prevention",
        "avoid": "prevention",
        "reduce risk": "prevention",
        "hi": "greeting",
        "hello": "greeting",
        "hey": "greeting",
        "bye": "farewell",
        "goodbye": "farewell",
        "thanks": "farewell",
        "thank you": "farewell"
    }
    
    # Check if any key term is in the user input
    for term, category in key_terms.items():
        if term in user_input_lower:
            return KNOWLEDGE_BASE[category]["responses"][0]
    
    # 3. If no key term match, try the original pattern matching as a fallback
    for category, data in KNOWLEDGE_BASE.items():
        if category in ["default", "greeting", "farewell"]:
            continue
        for pattern in data["patterns"]:
            if re.search(r'\b' + re.escape(pattern.lower()) + r'\b', user_input_lower):
                return data["responses"][0]
            if pattern.lower() in user_input_lower:
                return data["responses"][0]

    # If no matches found, return the default response
    default_response_text = KNOWLEDGE_BASE["default"]["responses"][0] + \
                       f"\n\nHere are some FAQ you can ask:\n- { '\n- '.join(EXAMPLE_PROMPTS)}"
                       
    return default_response_text

def initialize_chat_history():
  """Initialize the chat history in the session state if it doesn't exist."""
  if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def display_fullpage_chat():
    st.title("Heart Disease Assistant Chatbot")
    st.markdown("Ask me anything about heart disease or the dataset.")

    # Initialize chat history with the initial assistant message if it's empty
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Hello! I'm your Heart Disease Assistant. How can I help you today?"}
        ]
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