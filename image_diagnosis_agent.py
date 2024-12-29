import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64

# Function to decode API key
def get_api_key():
    # Encoded API key (encode your key first using base64)
    encoded_key = "QUl6YVN5Q05DdHp5ZFZSVTV0VWNkWl9PaDRVNG5lUFVxenFCZncw"  # This is just an example
    return base64.b64decode(encoded_key).decode('utf-8')

# Function to initialize the model
def initialize_gemini():
    api_key = get_api_key()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

# Configure Streamlit App
st.set_page_config(
    page_title="Medical Image Diagnosis Agent",
    layout="wide"
)
st.title("Medical Image Diagnosis Agent 🩺")
st.caption("Upload medical images for professional AI-powered analysis by Martin Khristi. 🌟")

# Initialize model
model = initialize_gemini()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for image upload
with st.sidebar:
    st.title("Upload Medical Images")
    uploaded_file = st.file_uploader(
        "Upload a medical image (X-ray, MRI, CT scan, etc.)...",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Medical Image', use_column_width=True)
        if st.button("Start Analysis"):
            st.session_state.start_analysis = True

# Main diagnosis interface
chat_placeholder = st.container()

with chat_placeholder:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input handling
prompt = st.chat_input("Describe symptoms or ask for analysis...")

if prompt or (uploaded_file and st.session_state.get("start_analysis")):
    # Ensure there's a text parameter
    if not prompt and uploaded_file:
        prompt = "Analyze the uploaded medical image."

    inputs = [prompt]

    # Add user message to chat history if a prompt is provided
    if prompt:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        # Display user message
        with chat_placeholder:
            with st.chat_message("user"):
                st.markdown(prompt)

    if uploaded_file:
        inputs.append(image)

    # Generate and display diagnosis response
    with st.spinner('Analyzing medical image and symptoms...'):
        try:
            response = model.generate_content(inputs)
            with chat_placeholder:
                with st.chat_message("assistant"):
                    st.markdown(response.text)

            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.text
            })
        except Exception as e:
            st.error(f"An error occurred during diagnosis: {str(e)}")

# Footer with disclaimer
st.markdown("---")
st.markdown(
    "**Disclaimer:** This tool provides AI-generated insights based on the uploaded medical images and described symptoms. "
    "It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.")
