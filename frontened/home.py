import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from langchain_core.messages import HumanMessage
from backened.chat_assistant_backened import *
from backened.utils.model import EuriLLM

model=EuriLLM()
thread_id='thread-1'
config={'configurable':{'thread_id':thread_id}}


if 'chat_history' not in st.session_state:
    st.session_state.chat_history=[]

for chat in st.session_state.chat_history:
    with st.chat_message(chat['role']):
        st.text(chat['content'])


user_input=st.chat_input("Enter here.")
if user_input:
    st.session_state.chat_history.append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    #get response from llm 
    #save that llm response into chat_history in session_state
    ai_response=workflow.invoke({'message':HumanMessage(content=user_input)},config=config)
    response=ai_response['message'][-1].content

    st.session_state.chat_history.append({'role':'assistant','content':response})
    with st.chat_message('assistant'):
        st.text(response)    
