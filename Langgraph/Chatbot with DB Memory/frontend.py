import streamlit as st
from backend import chatbot, all_threads
from langchain_core.messages import HumanMessage, SystemMessage
import uuid

############################################ Utilities ############################################
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    st.session_state['thread_id'] = generate_thread_id()
    st.session_state['message_history'] = []
    chat_threads(st.session_state['thread_id'])

def chat_threads(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_convo(thread_id):
    messages = chatbot.get_state(config={'configurable':{'thread_id':thread_id}}).values['messages']
    temp_messages = []
    for message in messages:
        if isinstance(message,HumanMessage):
            role = 'user'
        else:
            role = 'assistant'
        temp_messages.append({'role':role,'message':message.content}) 
    return temp_messages

############################################ Session State ############################################
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = all_threads
chat_threads(st.session_state['thread_id'])

############################################ UI ############################################
st.sidebar.title("Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("Conversations")
for thread_ids in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_ids)):
        st.session_state['thread_id'] = thread_ids
        st.session_state['message_history'] = load_convo(thread_ids)

############################################ Full Conversation ############################################
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['message'])


############################################ Q&A ############################################
config = {'configurable':{'thread_id':st.session_state['thread_id']}}
user_input = st.chat_input("Type here:") 

if user_input:
    st.session_state['message_history'].append({'role':'human','message':user_input})
    with st.chat_message('human'):
        st.text(user_input)

    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream( 
                {"messages": [HumanMessage(content=user_input)]},
                stream_mode="messages",
                config=config
            )
        )
    st.session_state['message_history'].append({'role':'assistant','message':ai_message})