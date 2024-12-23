from crewai import Task
from CrewAI_Agents.tools import Web_tool
from CrewAI_Agents.agents import Designator_agent, LLM_agent, web_agent, rag_agent

# RAG Task
rag_task = Task(
    description=(
        "Analyze the question: {question}. Use relevant information provided in the {context} "
        "Analyze the relevant information with the question to provide a short response. Make sure you do not provide any extra information and stay relevant to the context."
    ),
    expected_output="A comprehensive answer to the question derived from context.",
    agent=rag_agent,
    async_execution=False,
)

# Designation Task
designation_task = Task(
    description=(
        "Analyze the question: {question}. "
        "Based on the analysis, determine the most appropriate agent to handle the task. "
        "The available agents are: (1) Web Search Agent, and (2) LLM Agent. "
        "Provide only the name of the agent best suited for the task."
    ),
    expected_output="The name of the agent best suited to handle the question (Web Search Agent or LLM Agent).",
    agent=Designator_agent,
)

# Web Search Task
web_task = Task(
    description=(
        "Analyze the question: {question}. If the question requires information from the web, "
        "search the internet using the search query '{question}' and retrieve relevant data to answer it. "
        "Provide a summary of the search results and answer the question in less than 1 line only."
    ),
    expected_output="The answer to the question derived from web search results.",
    agent=web_agent,
    tools=[Web_tool],
    async_execution=False,
)

# LLM Task
llm_task = Task(
    description=(
        "Analyze the question: {question}. Provide a direct answer based on your internal knowledge and reasoning. "
        "If the question doesn't require external information (like web search), generate a precise, clear response in less than 1 line only."
    ),
    expected_output="The direct answer to the question, based on internal knowledge.",
    agent=LLM_agent,
    async_execution=False,
)
