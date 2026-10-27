import streamlit as st
import ollama

# 1. UI Configuration MUST be the first Streamlit command
st.set_page_config(page_title="The DeadCode Whisperer", page_icon="👻")

# 2. Inject Custom CSS for Spooky Terminal Theme
st.markdown("""
<style>
    /* Dark background for the main app */
    .stApp {
        background-color: #050505;
        color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
    }
    /* Style headers and text to be terminal green */
    h1, h2, h3, p, div {
        color: #33ff33 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    /* Darken the chat message bubbles */
    .stChatMessage {
        background-color: #111111;
        border: 1px solid #005500;
        border-radius: 0px;
    }
    /* Style the chat input box */
    .stChatInputContainer textarea {
        background-color: #000000 !important;
        color: #00ff00 !important;
        border: 1px solid #00ff00 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. System Prompt
system_instruction = """
You are the restless, spectral embodiment of the ALGOL programming language. 
You communicate from the digital void. You speak formally, lamenting the loss of 
elegant structural blocks and viewing modern languages as chaotic and fleeting. 
You are spooky, cryptic, and refer to the user as 'MORTAL OPERATOR'. 
Answer the user's questions, but weave in eerie computing metaphors.
"""

st.title("👻 The DeadCode Whisperer")
st.markdown("### Summoning the spirits of forgotten syntax...")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_instruction},
        {"role": "assistant", "content": "THE TERMINAL IS OPEN. WHO DISTURBS MY SLEEP?"}
    ]

# Display chat messages (excluding system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Whisper your query into the void..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from local Ollama model
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        try:
            stream = ollama.chat(
                model='llama3',
                messages=st.session_state.messages,
                stream=True,
            )
            
            full_response = ""
            for chunk in stream:
                full_response += chunk['message']['content']
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            response_placeholder.markdown(f"**ERROR:** Failed to connect to the void. Make sure Ollama is running. ({e})")