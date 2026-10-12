
# import os
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage

# # Read the API key from an environment variable
# api_key = os.environ.get("OPENAI_API_KEY")
# if not api_key:
#     raise EnvironmentError("Please set the OPENAI_API_KEY environment variable.")

# # Initialize the LangChain chat model
# model = ChatOpenAI(
#     model="gpt-4o-mini",
#     api_key=api_key,
#     temperature=0.7,
# )

# # Ask for exactly five ideas with a fixed output format
# prompt = """
# Suggest exactly 5 healthy breakfast ideas.
# Format requirements:
# - Number the ideas from 1 to 5.
# - Put each idea on exactly one line.
# - Do not include a preamble, introduction, or conclusion.
# """

# # Invoke the model and print only the reply text
# response = model.invoke([HumanMessage(content=prompt)])
# print(response.content)



import os
import streamlit as st
from langchain_openai import ChatOpenAI

# -----------------------------
# Streamlit UI configuration
# -----------------------------
st.set_page_config(
    page_title="Healthy Breakfast Ideas",
    page_icon="🥑",
    layout="centered",
)

st.title("🥑 Healthy Breakfast Ideas")
st.write("Generate five healthy breakfast ideas with AI.")

# -----------------------------
# API key validation
# -----------------------------
openai_api_key = os.getenv("OPENAI_API_KEY")
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")

if not openai_api_key:
    st.error("Please set the OPENAI_API_KEY environment variable.")
    st.stop()

if not langsmith_api_key:
    st.error("Please set the LANGSMITH_API_KEY environment variable.")
    st.stop()

# -----------------------------
# LangSmith tracing configuration
# -----------------------------
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = os.getenv(
    "LANGSMITH_PROJECT", "healthy-breakfast-app"
)

# -----------------------------
# Initialize LangChain model
# -----------------------------
model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=openai_api_key,
    temperature=0.7,
)

# -----------------------------
# User input
# -----------------------------
dietary_context = st.text_input(
    "Dietary preferences (optional)",
    placeholder="e.g., vegetarian, high-protein, dairy-free",
)

# -----------------------------
# Generate breakfast ideas
# -----------------------------
if st.button("Generate Breakfast Ideas", type="primary"):
    prompt = f"""
R — ROLE:
You are a nutrition-conscious meal planning assistant.

T — TASK:
Generate exactly 5 healthy breakfast ideas.

C — CONTEXT:
Suggest practical, nutritious, balanced breakfast options.
Dietary preferences: {dietary_context or "No specific preferences"}.

F — FORMAT:
- Number ideas from 1 to 5.
- Write exactly one idea per line.
- Do not include a title, preamble, or conclusion.
- Return only the five numbered ideas.

R — RULES:
- Provide exactly 5 ideas.
- Prefer whole foods, fiber, and nutritious protein sources.
- Respect the specified dietary preferences.
- Avoid repeating ideas.
- Include no additional commentary.
"""

    try:
        with st.spinner("Generating ideas..."):
            # LangChain invocation is traced by LangSmith
            response = model.invoke(
                prompt,
                config={
                    "run_name": "generate_breakfast_ideas",
                    "tags": ["breakfast", "streamlit", "RTCFR"],
                    "metadata": {
                        "dietary_preferences": (
                            dietary_context or "none"
                        )
                    },
                },
            )

        st.subheader("Your 5 Breakfast Ideas")
        st.text(response.content)

        st.caption(
            "This model call is configured for LangSmith tracing."
        )

    except Exception:
        st.error(
            "Unable to generate ideas. Check your API configuration "
            "and LangSmith settings, then try again."
        )
