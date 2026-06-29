import subprocess
import sys

# Force install google-genai right when the app boots up
try:
    from google import genai
    from google.genai import types
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai"])
    from google import genai
    from google.genai import types

import streamlit as st

# --- REST OF YOUR CODE CONTINUES HERE ---
# 1. Clean App Header
st.title("Python AI Assistant 🤖")
st.caption("Ask me any question strictly about Python programming.")

# 2. Configure Guardrails (Forcing Python only)
config_settings = types.GenerateContentConfig(
    system_instruction=(
        "You are an expert Python developer. You must ONLY answer questions, "
        "provide explanations, or write code related to Python programming. "
        "If the user asks a question about any other topic, politely refuse."
    )
)

# 3. Initialize Gemini Client using Secrets
try:
    robo = genai.Client(api_key=st.secrets["MY_API"])
except Exception as e:
    st.error("Missing or incorrect API key in Streamlit Secrets.")

# 4. Input Box Layout
user_question = st.text_input("Message Python Assistant:", placeholder="Type your question here...")

# 5. Simple Action Button
col1, col2, col3 = st.columns()
with col2:
    send_clicked = st.button("Ask Gemini ✨", use_container_width=True)

# 6. Response processing area
if send_clicked:
    if user_question.strip():
        with st.spinner("Thinking..."):
            try:
                response = robo.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_question,
                    config=config_settings  
                )
                st.write("---")
                with st.chat_message("assistant"):
                    st.write(response.text)
            except Exception as e:
                st.error(f"API Error. Details: {e}")
    else:
        st.warning("Please type a question first!")
