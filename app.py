import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from chatbot import initialize_chat_history, display_fullpage_chat

# Set page config
st.set_page_config(
    page_title="Heart Disease Prediction Dashboard",
    page_icon="🫀",
    layout="wide"
)

# Add CSS to hide Streamlit header, footer, main menu, and owner information
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
._profileContainer_gzau3_53 {display: none;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Initialize chat history
initialize_chat_history()

# Title and description
st.title("Heart Disease Prediction Dashboard")
st.markdown("""
This dashboard analyzes the Cleveland Heart Disease dataset and provides predictions using machine learning.
""")

# Load the dataset
@st.cache_data
def load_data():
    # Column names for the dataset
    columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 
              'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
    
    # Load the data
    data = pd.read_csv('Heart_disease_cleveland_new.csv', names=columns)
    
    # Convert columns to numeric types
    numeric_columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 
                      'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
    
    # Handle missing values
    # For numeric columns, fill with median
    for col in numeric_columns:
        data[col] = data[col].fillna(data[col].median())
    
    # Convert target to binary (0 or 1)
    data['target'] = (data['target'] > 0).astype(int)
    
    return data

# Load and display the data
try:
    df = load_data()
    st.subheader("Dataset Overview")
    st.dataframe(df.head())
    
    # Basic statistics
    st.subheader("Basic Statistics")
    st.write(df.describe())
    
    # Data visualization
    st.subheader("Data Visualization")
    
    # Create two columns for plots
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Age Distribution")
        fig, ax = plt.subplots()
        sns.histplot(data=df, x='age', hue='target', bins=30)
        st.pyplot(fig)
        
    with col2:
        st.write("Heart Rate vs Age")
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x='age', y='thalach', hue='target')
        st.pyplot(fig)
    
    # Machine Learning Model
    st.subheader("Heart Disease Prediction")
    
    # Prepare features and target
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Display model performance
    st.write("Model Accuracy:", accuracy_score(y_test, y_pred))
    
    # Feature importance
    st.write("Feature Importance")
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    fig, ax = plt.subplots()
    sns.barplot(data=feature_importance, x='Importance', y='Feature')
    st.pyplot(fig)
    
    # Prediction Interface
    st.subheader("Make a Prediction")
    
    # Create input fields for features
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=0, max_value=100, value=50)
        sex = st.selectbox("Sex", options=[0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
        cp = st.selectbox("Chest Pain Type", options=[0, 1, 2, 3])
        trestbps = st.number_input("Resting Blood Pressure", min_value=0, max_value=300, value=120)
        chol = st.number_input("Cholesterol", min_value=0, max_value=600, value=200)
        fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=[0, 1])
        
    with col2:
        restecg = st.selectbox("Resting ECG Results", options=[0, 1, 2])
        thalach = st.number_input("Maximum Heart Rate", min_value=0, max_value=300, value=150)
        exang = st.selectbox("Exercise Induced Angina", options=[0, 1])
        oldpeak = st.number_input("ST Depression", min_value=0.0, max_value=10.0, value=0.0)
        slope = st.selectbox("Slope of Peak Exercise ST", options=[0, 1, 2])
        ca = st.selectbox("Number of Major Vessels", options=[0, 1, 2, 3])
        thal = st.selectbox("Thalassemia", options=[0, 1, 2, 3])
    
    # Make prediction
    if st.button("Predict"):
        # Get input data from the form
        input_data = {
            'age': age,
            'sex': sex,
            'cp': cp,
            'trestbps': trestbps,
            'chol': chol,
            'fbs': fbs,
            'restecg': restecg,
            'thalach': thalach,
            'exang': exang,
            'oldpeak': oldpeak,
            'slope': slope,
            'ca': ca,
            'thal': thal
        }
        # Convert input data to DataFrame with feature names
        input_df = pd.DataFrame([input_data])
        
        prediction = model.predict(input_df)
        probability = model.predict_proba(input_df)
        
        st.write("Prediction:", "Heart Disease Present" if prediction[0] == 1 else "No Heart Disease")
        st.write("Probability:", f"{probability[0][1]*100:.2f}%")

    # Add the floating chat window at the end
    if __name__ == "__main__":
        display_fullpage_chat()

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please make sure the dataset file 'Heart_disease_cleveland_new.csv' is in the same directory as this script.") 