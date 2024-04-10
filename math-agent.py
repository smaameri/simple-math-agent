import sys
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI

from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv('.env')

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def square(a) -> int:
    """Calculates the square of a number."""
    a = int(a)
    return a * a

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a mathematical assistant. Use your tools to answer questions.
         If you do not have a tool to answer the question, say so. 

        Return only the answers. e.g
        Human: What is 1 + 1?
        AI: 2
        """),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

# Choose the LLM that will drive the agent
llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

# Setup the toolkit
tools = [add, multiply, square]

# Construct the OpenAI Tools agent
agent = create_openai_tools_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

yellow = "\033[0;33m"
green = "\033[0;32m"
white = "\033[0;39m"

chat_history = []
print(f"{yellow}---------------------------------------------------------------------------------")
print('I am a mathematical assistant. How can I help you?')
print('---------------------------------------------------------------------------------')

while True:
    query = input(f"{green}Prompt: ")
    if query == "exit" or query == "quit" or query == "q" or query == "f":
        print('Exiting')
        sys.exit()
    if query == '':
        continue
    result = agent_executor.invoke({"input": query})
    print(f"\n{white}Answer: " + result["output"] + "\n")
    chat_history.append((query, result["output"]))
