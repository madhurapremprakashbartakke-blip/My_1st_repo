import streamlit as st
from google import genai
from google.genai import types  # Imported to pass system instructions

# Custom HTML Heading
st.markdown(
    """
    <h1 style='text-align: center;'> Python AI Assistant</h1>
    <p style='text-align: center; font-size:18px;'>
        Ask any Python programming question.
    </p>
    """,
    unsafe_allow_html=True,
)

# 1. Define strict Python-only guardrails
config_settings = types.GenerateContentConfig(
    system_instruction=(
        "You are an exclusive Python Programming Assistant. "
        "You must ONLY answer questions directly related to Python syntax, libraries, or logic. "
        "If a user asks about, uses syntax from, or types commands belonging to other programming languages "
        "(for example: 'printf()' from C, 'cout' from C++, 'console.log' from JavaScript, 'System.out.println' from Java), "
        "or asks any non-Python question, you must immediately reject it. "
        "In your rejection, output this exact message: "
        "'Error: Please ask a Python-related question. I do not answer questions outside the Python domain.'"
    )
)

# Initialize Client
robo = genai.Client(api_key="YOUR_GEMINI_API_KEY")

# 2. Attach the config settings to your chat architecture
if "chat" not in st.session_state:
    st.session_state.chat = robo.chats.create(
        model="gemini-2.5-flash", # Using the stable generation model
        config=config_settings    # Injects the system guardrails permanently
    )

# Placeholder for the response
response_placeholder = st.empty()

question = st.text_input("", placeholder="Enter your Python question here...")

col1, col2, col3 = st.columns(3, gap="medium", vertical_alignment="center")
with col2:
    send = st.button("Send")

if send:
    if question.strip():
        # Call the session state chat to preserve instructions and history
        response = st.session_state.chat.send_message(question)
        response_placeholder.write(response.text)
    else:
        st.warning("Please enter a question first.")
