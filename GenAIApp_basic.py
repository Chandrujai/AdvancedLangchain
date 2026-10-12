import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv

# 1. Page Configuration
st.set_page_config(page_title="AI Chef Assistant", page_icon="👨‍🍳")
st.title("👨‍🍳 AI Chef Assistant")
st.write("Your personal AI cooking partner with real-time memory and streaming.")

load_dotenv()

# 2. Setup API Key (Change 'your-openai-api-key-here' or rely on env variables)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found. Check your .env file."
    )


# 3. Initialize LLM and Chain (Cached so it doesn't reload on every click)
@st.cache_resource
def get_chain():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an expert chef. Help the user with recipes and cooking advice based on their conversation history."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])
    return prompt_template | llm | StrOutputParser()

base_chain = get_chain()

# 4. Modern Chat History wrapper synced with Streamlit Session State
class StreamlitChatHistory(BaseChatMessageHistory):
    def __init__(self, messages: list[BaseMessage]):
        self.messages = messages

    def add_messages(self, messages: list[BaseMessage]) -> None:
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []

if "chat_store" not in st.session_state:
    st.session_state.chat_store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in st.session_state.chat_store:
        st.session_state.chat_store[session_id] = []
    return StreamlitChatHistory(st.session_state.chat_store[session_id])

conversational_chain = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

config = {"configurable": {"session_id": "streamlit_user_session"}}

# 5. Render Past Messages on App Rerun
session_history = get_session_history("streamlit_user_session")
for message in session_history.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# 6. Handle New User Input & Live Streaming
if user_input := st.chat_input("What would you like to cook today?"):
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # Generate and stream AI response
    with st.chat_message("assistant"):
        def generate_response():
            for chunk in conversational_chain.stream({"input": user_input}, config=config):
                yield chunk
        
        # Streamlit's built-in helper for streaming text generators
        st.write_stream(generate_response())