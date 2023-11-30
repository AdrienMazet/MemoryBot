import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import os

# TODO :
# faire le prompt en fonction du rôle et du preprompt
# faire pareil sur plusieurs conversations, plusieurs assistants accessibles via le volet

assistants = [
    {'name':'Développeur python','description':'Écris la fonction demandée en python','role':'En tant que développeur confirmé, ','preprompt':'écris moi le code python '},
    {'name':"Vérificateur d'accessibilité",'description':"Vérifie si les bonnes pratiques d'accessibilité sont respectées dans un code html",'role':"En tant que développeur formé à l'accessibilité, ",'preprompt':"dis moi ce qui peut être amélioré en termes d'accessibilité dans le code suivant "},
    {'name':'Testeur JS Jest','description':"Écris le test jest associé à une fonction donnée",'role':"En tant que testeur aggueri, ",'preprompt':"écris le test associé à la fonction suivante, en utilisant le framework de test jest et le language de programmation JavaScript "}
]

currentAssistant = 0

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
if "settings" not in st.session_state:
    st.session_state["settings"] = False

def clear_text():
    st.session_state["temp"] = st.session_state["input"]
    st.session_state["input"] = ""

def get_text():
    if not st.session_state["settings"]:
        input_text = st.text_input("You: ", st.session_state["input"], key="input", 
                            placeholder="Dialoguez avec votre assistant...", 
                            on_change=clear_text,    
                            label_visibility='hidden')
    input_text = st.session_state["temp"]
    return input_text

def toggle_settings():
    st.session_state["settings"] = not st.session_state["settings"]

with st.sidebar:
    for assistant in assistants:
        st.button(assistant["name"], use_container_width= True)

st.title("Challenge IA Générative")

col1, col2 = st.columns([12,1])

with col1:
    if st.session_state["settings"]:
        assistants[currentAssistant]["name"] = st.text_input("",assistants[currentAssistant]["name"],placeholder="Nom de l'assistant")
    else:
        st.subheader(assistants[currentAssistant]["name"])

with col2:
    st.button("⚙️", "settings_button", on_click=toggle_settings)

if st.session_state["settings"]:
   assistants[currentAssistant]["description"] = st.text_area("",assistants[currentAssistant]["description"],placeholder="Description de l'assistant")
else:
    st.text(assistants[currentAssistant]["description"])

if st.session_state["settings"]:
    assistants[currentAssistant]["role"] = st.text_area("",assistants[currentAssistant]["role"],placeholder="Rôle : répond moi en tant que ...")
    assistants[currentAssistant]["preprompt"] = st.text_area("",assistants[currentAssistant]["preprompt"],placeholder="Instructions : donne moi la définition de")


os.environ['OPENAI_API_KEY'] = ''
llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo", verbose=False) 
        
# Create the ConversationChain object with the specified configuration
Conversation = ConversationChain(llm=llm)  

user_input = get_text()

# Generate the output using the ConversationChain object and the user input, and add the input/output to the session
if user_input:
    with get_openai_callback() as cb:
        output = Conversation.run(input=assistants[currentAssistant]["role"] + assistants[currentAssistant]["preprompt"] + user_input)
        st.session_state.past.append(user_input)  
        st.session_state.generated.append(output) 
        

# Display the conversation history using an expander, and allow the user to download it
with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.info(st.session_state["past"][i],icon="🧐")
        st.success(st.session_state["generated"][i], icon="🤖")

# Divide the app page into two columns
col1, col2, col3 = st.columns(3)
