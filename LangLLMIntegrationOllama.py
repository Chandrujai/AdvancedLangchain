from dotenv import load_dotenv

load_dotenv()

from langchain_ollama import ChatOllama

# Runs on your own computer -- no API key needed
llm = ChatOllama(model="llama3")

response = llm.invoke("What is Python in one sentence?")
print(response.content)

for chunk in llm.stream("Count from 1 to 5 slowly."):
    print(chunk.content, end="", flush=True)