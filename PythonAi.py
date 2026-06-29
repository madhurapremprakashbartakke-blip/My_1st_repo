import streamlit as st
from google import genai
from google.genai import types 

# 1. Clean App Header (Native Streamlit elements - No custom HTML)
st.title("Python AI Assistant 🤖")
st.caption("Ask me any question strictly about Python programming.")

# 2. Configure Guardrails (Forcing Python only)
config_settings = types.GenerateContentConfig(
    system_instruction=(
        "You are an expert Python developer. You must ONLY answer questions, "
        "provide explanations, or write code related to Python programming. "
        "If the user asks a question about any other topic (including other programming "
        "languages, general knowledge, or creative writing), politely refuse by saying: "
        "'Please ask a Python-related question. I do not answer questions outside the Python domain.'"
    )
)

# 3. Initialize Gemini Client (Replace with your active API key)
robo= genai.Client(api_key=st.secrets["MY_API"])
# 4. Input Box Layout
user_question = st.text_input("Message Python Assistant:", placeholder="Type your question here...")

# 5. Simple Action Button
col1, col2, col3 = st.columns(3)
with col2:
    send_clicked = st.button("Ask Gemini ✨", use_container_width=True)

# 6. Response processing area
if send_clicked:
    if user_question.strip():
        with st.spinner("Thinking..."):
            try:
                # Call the API with the strict system configuration attached
                response = robo.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_question,
                    config=config_settings  
                )
                
                st.write("---")
                # Using Streamlit's native chat container layout (Guarantees perfect background/text contrast)
                with st.chat_message("assistant"):
                    st.write(response.text)
                
            except Exception as e:
                st.error(f"API Error. Details: {e}")
    else:
        st.warning("Please type a question first!")
