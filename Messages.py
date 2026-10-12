from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")
print("Ready!")

# messages = [
#     SystemMessage(content="You are a friendly teacher. Keep answers very short."),
#     HumanMessage(content="What is a variable in Python?")
# ]

# response = llm.invoke(messages)
# print(response.content)

# print("Type of reply:", type(response).__name__)
# print("Reply text:", response.content)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="My name is Anjali.")
]

# First reply
reply = llm.invoke(messages)
print("AI:", reply.content)

# Add the AI's reply, then ask a follow-up
messages.append(reply)
messages.append(HumanMessage(content="What is my name?"))

reply = llm.invoke(messages)
print("AI:", reply.content)