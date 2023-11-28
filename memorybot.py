"""
This is a Python script that serves as a frontend for a conversational AI model built with the `langchain` and `llms` libraries.
The code creates a web application using Streamlit, a Python library for building interactive web apps.
"""

# Import necessary libraries
import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import re

def is_four_digit_number(string):
    pattern = r'^\d{4}$'  # Matches exactly four digits
    return bool(re.match(pattern, string))


# Set Streamlit page configuration
st.set_page_config(page_title='Challenge IA Générative', layout='wide')
# Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []
if "just_sent" not in st.session_state:
    st.session_state["just_sent"] = False
if "temp" not in st.session_state:
    st.session_state["temp"] = ""
if "balance" not in st.session_state:
    st.session_state["balance"] = 0.0
if "deposit" not in st.session_state:
    st.session_state["deposit"] = 3.0

def clear_text():
    st.session_state["temp"] = st.session_state["input"]
    st.session_state["input"] = ""


# Define function to get user input
def get_text():
    """
    Get the user input text.

    Returns:
        (str): The text entered by the user
    """
    input_text = st.text_input("You: ", st.session_state["input"], key="input", 
                            placeholder="Your AI assistant here! Ask me anything ...", 
                            on_change=clear_text,    
                            label_visibility='hidden')
    input_text = st.session_state["temp"]
    return input_text


    # Define function to start a new chat
def new_chat():
    """
    Clears session state and starts a new chat.
    """
    save = []
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])        
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state.entity_memory.store = {}
    st.session_state.entity_memory.buffer.clear()

MODEL = "gpt-3.5-turbo-1106"
K = 100

with st.sidebar:
    st.markdown("---")
    st.markdown("# About")
    st.markdown(
       "ChatGPTm is ChatGPT added memory. "
       "It can do anything you asked and also remember you."
            )

    
# Set up the Streamlit app layout
st.title("🤖 ChatGPT with Memory 🧠")
#st.subheader(" Powered by 🦜 LangChain + OpenAI + Streamlit")

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# Let user select version
st.write("GPT4.5 Turbo ！")
version = st.selectbox("Choose ChatGPT version", ("3.5", "4.5"))
if version == "3.5":
    # Use GPT-3.5 model
    MODEL = "gpt-3.5-turbo"
else:
    # USe GPT-4.5 model
    MODEL = "gpt-4"
    
# Ask the user to enter their OpenAI API key
API_O = st.sidebar.text_input("API-KEY", type="password")
# Read API from Streamlit secrets

# Session state storage would be ideal
if API_O:
    # Create an OpenAI instance
    llm = OpenAI(temperature=0,
                openai_api_key=API_O, 
                model_name=MODEL, 
                verbose=False) 


    # Create a ConversationEntityMemory object if not already created
    if 'entity_memory' not in st.session_state:
            st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=K )
        
        # Create the ConversationChain object with the specified configuration
    Conversation = ConversationChain(
            llm=llm, 
            prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
            memory=st.session_state.entity_memory
        )  
else:
    st.sidebar.warning('API key required to try this app.The API key is not stored in any form.')
    # st.stop()


# Add a button to start a new chat
#st.sidebar.button("New Chat", on_click = new_chat, type='primary')

# Get the user input
user_input = get_text()

# Generate the output using the ConversationChain object and the user input, and add the input/output to the session
if user_input:
    if st.session_state["balance"] > -0.03:
        with get_openai_callback() as cb:
            output = Conversation.run(input=user_input)  
            st.session_state.past.append(user_input)  
            st.session_state.generated.append(output) 
            st.session_state["balance"] -= cb.total_cost * 4
    else:
        st.session_state.past.append(user_input)  
        if is_four_digit_number(user_input) :
            st.session_state["balance"] += st.session_state["deposit"]
            st.session_state.generated.append("to replace") 
        else: 
            st.session_state.generated.append("to replace") 
        

# Allow to download as well
download_str = []
# Display the conversation history using an expander, and allow the user to download it
with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.info(st.session_state["past"][i],icon="🧐")
        st.success(st.session_state["generated"][i], icon="🤖")
        download_str.append(st.session_state["past"][i])
        download_str.append(st.session_state["generated"][i])
                            
    # Can throw error - requires fix
    download_str = '\n'.join(download_str)
    
    if download_str:
        st.download_button('Download',download_str)

# Display stored conversation sessions in the sidebar
for i, sublist in enumerate(st.session_state.stored_session):
        with st.sidebar.expander(label= f"Conversation-Session:{i}"):
            st.write(sublist)

# Allow the user to clear all stored conversation sessions
if st.session_state.stored_session:   
    if st.sidebar.checkbox("Clear-all"):
        del st.session_state.stored_session


# Divide the app page into two columns
col1, col2, col3 = st.columns(3)
