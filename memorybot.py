import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import os

# TODO :
# faire une popup de configuration (nom du bot, preprompt, ou rôle)
# faire le prompt en fonction du rôle
# faire pareil sur plusieurs conversations, plusieurs assistants accessibles via le volet


# Set Streamlit page configuration
st.set_page_config(page_title='Challenge IA Générative', layout='wide')
# Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "temp" not in st.session_state:
    st.session_state["temp"] = ""

def clear_text():
    st.session_state["temp"] = st.session_state["input"]
    st.session_state["input"] = ""

def get_text():
    input_text = st.text_input("You: ", st.session_state["input"], key="input", 
                            placeholder="Your AI assistant here! Ask me anything ...", 
                            on_change=clear_text,    
                            label_visibility='hidden')
    input_text = st.session_state["temp"]
    return input_text
    
st.title("Challenge IA Générative")

col1, col2 = st.columns([12,1])

with col1:
    st.subheader("AI Assitant A")
with col2:
    st.button("⚙️", "settings_button")

with st.sidebar:
    st.button("AI-ssistant A", use_container_width= True)
    st.button("AI-ssistant B", use_container_width= True)
    st.button("AI-ssistant C", use_container_width= True)

#os.environ['OPENAI_API_KEY'] = 'mykey'
#llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo", verbose=False) 
        
# Create the ConversationChain object with the specified configuration
#Conversation = ConversationChain(
#        llm=llm, 
#        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
#    )  

user_input = get_text()

# Generate the output using the ConversationChain object and the user input, and add the input/output to the session
if user_input:
    with get_openai_callback() as cb:
        #output = Conversation.run(input=user_input)  
        output = "fake output"
        st.session_state.past.append(user_input)  
        st.session_state.generated.append(output) 
        

# Display the conversation history using an expander, and allow the user to download it
with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.info(st.session_state["past"][i],icon="🧐")
        st.success(st.session_state["generated"][i], icon="🤖")

# Divide the app page into two columns
col1, col2, col3 = st.columns(3)
