import os 
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

@tool 
def add(a : int ,b : int) -> int:
    "add two number"
    return a + b

@tool
def multiply(a: int ,b: int)-> int:
    "multipy two numbers"
    return a * b

tools = [add,multiply]

llm = ChatGoogleGenerativeAI(api_key = os.getenv("API_KEY"),model="gemini-2.5-flash")

agent = create_agent(model = llm , tools = tools , system_prompt="you are an ai assistant")

prompt = "what is 2 multipy 5 "

response = agent.invoke({
    "messages": [("user", prompt)]
})

print(response["messages"][-1].content)