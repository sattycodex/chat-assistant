import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from langchain_core.messages import HumanMessage
from backened.chat_assistant_backened import *
import uuid



#****************utility functions*******************************
def generate_thread_id():
    thread_id=uuid.uuid4()
    st.session_state['current_thread']=thread_id
    st.session_state['threads'].append(thread_id)

def reset_chat():
    st.session_state['chat_history']=[]

def add_chat_history(thread_id):
    state=workflow.get_state(config={'configurable':{'thread_id':thread_id}})
    response=state.values.get('message',[])
    message_hist=[]
    for r in response:
        if isinstance(r,HumanMessage):
            role='user'
        else:
            role='assistant'

        message_hist.append({'role':role,'content':r.content})         
    
    #message_hist.reverse() 
    st.session_state['chat_history']=message_hist

#****************************************************************


#************************ static and load component **************

col1, col2, col3 = st.columns([1, 2, 1]) # Adjust column ratios as needed

with col2:
    st.title('Chat Assistant')

if 'chat_history' not in st.session_state:
    st.session_state.chat_history=[]

if 'threads' not in st.session_state:
    st.session_state['threads']=[]
    generate_thread_id() 

if 'current_thread' not in st.session_state:
    st.session_state['current_thread']=''

if "thread_topic_map" not in st.session_state:
    st.session_state['thread_topic_map']={}

#*****************************************************************

#**************** side bar **************************************
st.sidebar.title('Conversations')
if st.sidebar.button('New Chat', key="green_button"):
    generate_thread_id()
    reset_chat()

st.markdown("""
<style>
div.stButton > button :hover{
    color:black;                               
}
</style>
""", unsafe_allow_html=True)

for thread in st.session_state['threads']:
    if st.sidebar.button(str(thread),type="tertiary"):
        st.session_state['current_thread']=thread
        add_chat_history(thread)
        
#****************************************************************



#*********************** chat part *********************************
if st.session_state['chat_history'] != None and st.session_state['chat_history'] !=[] :
    for chat in st.session_state['chat_history']:
        with st.chat_message(chat['role']):
            st.text(chat['content'])


user_input=st.chat_input("Enter here.")
if user_input:
    st.session_state.chat_history.append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    #get response from llm 
    #save that llm response into chat_history in session_state
    ai_response=workflow.invoke({'message':HumanMessage(content=user_input)},config={'configurable':{'thread_id':st.session_state['current_thread']}})
    response=ai_response['message'][-1].content

    st.session_state.chat_history.append({'role':'assistant','content':response})
    
    with st.chat_message('assistant'):
        st.text(response) 


