from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# llm = ChatOpenAI(model="gpt-4o-mini",)

# print("Model is ready!")

# response = llm.invoke("What is Python in one sentence?")

# print(response.content)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0   # 0 = focused and predictable
)

response = llm.invoke("Give me 3 fun facts about space.")
print(response.content)

for chunk in llm.stream("Count from 1 to 5 slowly."):
    print(chunk.content, end="", flush=True)