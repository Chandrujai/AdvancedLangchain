from dotenv import load_dotenv

load_dotenv()

from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-opus-4-8")

response = llm.invoke("What is Python in one sentence?")
print(response.content)

for chunk in llm.stream("Count from 1 to 5 slowly."):
    print(chunk.content, end="", flush=True)