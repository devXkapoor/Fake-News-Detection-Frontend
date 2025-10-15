import streamlit as st
import requests

# -------------------------------
# Streamlit UI Setup
# -------------------------------
st.set_page_config(page_title="AI Fake News Detector", layout="wide")
st.title(" AI Fake News Detector")
st.write(
    "Analyze any news headline or article to see if it's **REAL** or **FAKE*,* using an AI-powered backend model."
)

# -------------------------------
# Backend Configuration
# -------------------------------
# BACKEND_URL = "http://127.0.0.1:8000/predict"  # Flask backend URL
BACKEND_URL = st.secrets["general"]["BACKEND_URL"] if "general" in st.secrets else "http://127.0.0.1:8000/predict"
# -------------------------------
# Input Section
# -------------------------------
st.subheader("Enter News Text")
user_input = st.text_area(
    "Paste news headline or paragraph here:",
    height=150,
    placeholder="e.g. Government launches new AI policy for schools",
)

# -------------------------------
# Detect Button
# -------------------------------
if st.button(" Detect Fake News"):
    if not user_input.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing... Please wait..."):
            try:
                # Send text to Flask backend
                response = requests.post(BACKEND_URL, json={"text": user_input})
                
                if response.status_code == 200:
                    result = response.json()
                    label = result.get("label", "Unknown")
                    score = result.get("score", 0.0)

                    # Display results
                    st.success(f"**Prediction:** {label}")
                    st.progress(score)
                    st.write(f"**Confidence:** {score:.2%}")

                    if label.lower() == "fake":
                        st.error(" This content is likely *Fake News*.")
                    else:
                        st.info(" This content appears to be *Real News*.")
                else:
                    st.error(f"Server error: {response.status_code} - {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error(" Unable to connect to backend. Please make sure the Flask server is running.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Developed with  using Streamlit + Flask + Hugging Face Transformers.")
