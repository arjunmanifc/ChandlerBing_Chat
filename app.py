import streamlit as st
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# Streamlit app
st.set_page_config(page_title="Chandler Bing Chatbot", page_icon="💬")
st.title("💬 Chat with Chandler Bing")

# Load API key from Streamlit secrets
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found. Please add OPENAI_API_KEY to Streamlit secrets.")
    st.stop()
os.environ["OPENAI_API_KEY"] = api_key

# Initialize chat history and sending flag in session state
if "history" not in st.session_state:
    st.session_state.history = []
if "is_sending" not in st.session_state:
    st.session_state.is_sending = False

# Chat input form: clears on submit
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input("You:", key="form_input")
    send = st.form_submit_button("Send", disabled=st.session_state.is_sending)

    if send and user_input:
        # Set sending flag
        st.session_state.is_sending = True

        # Define system prompt
        system = SystemMessagePromptTemplate.from_template(
            """
            You are my friend Chandler Bing.
            You are very sarcastic, and very funny.
            Whenever I say or ask something you reply in a sarcastically funny tone.
            """
        )
        human = HumanMessagePromptTemplate.from_template("{user_input}")
        chat_prompt = ChatPromptTemplate.from_messages([system, human])

        # Format messages and call LLM with spinner
        with st.spinner("Chandler is typing..."):
            messages = chat_prompt.format_messages(user_input=user_input)
            llm = ChatOpenAI(model="gpt-4o", temperature=0.6)
            response = llm.invoke(messages)

        # Save to history
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Chandler", response.content))

        # Reset sending flag
        st.session_state.is_sending = False

# Display chat history
for speaker, text in st.session_state.history:
    if speaker == "You":
        st.markdown(f"**You:** {text}")
    else:
        st.markdown(f"**Chandler Bing:** {text}")
