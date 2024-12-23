from crewai import Agent,LLM
from CrewAI_Agents.tools import Web_tool
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key= os.getenv("GROQ_API_KEY")

llm = LLM(
    model="groq/gemma2-9b-it",
    temperature=0.7,
    api_key= groq_api_key
)


## Create a Designator agent
Designator_agent = Agent(
    role='Task Designation Agent',
    goal='Determine the most effective way to answer the given question: {question}. Options: (1)RAG, (2) Web Search, (3) Direct Answer',
    verbose=True,
    memory=True,
    backstory=(
        "The Designator Agent is an expert in understanding complex queries and determining the best approach to answering them. "
        "It will evaluate the provided question and recommend the appropriate method for addressing it, whether it requires retrieval, "
        "a web search, or a direct answer."
    ),
    allow_delegation=True,
    llm=llm
)

## Create a RAG Agent
rag_agent = Agent(
    role='RAG Agent',
    goal='Retrieve relevant information and generate a comprehensive answer to the given question: {question}. and the provided context:{context}.',
    verbose=True,
    memory=True,
    backstory=(
        "The RAG Agent is an expert in combining retrieval and generation techniques to provide accurate and detailed answers. "
        "It retrieves relevant information from a knowledge base and uses advanced language models to generate a comprehensive response."
    ),
    allow_delegation=True,
    llm=llm 
)

## Create a Web Agent
web_agent = Agent(
    role='Web Search Agent',
    goal='Assist in answering the query: {question}. This may include searching the web and summarizing relevant information. Make sure you respond in less than 2 lines only.',
    verbose=True,
    memory=True,
    backstory=(
        "The Web Search Agent is an expert in leveraging web search tools to gather information. "
        "It will search the web for relevant information and synthesize it into a coherent answer for the provided question. "
        "If the query cannot be answered directly from available sources, the agent will use the web to find the most accurate, up-to-date information.Make sure you respond in less than 2 lines only."
    ),
    tools=[Web_tool],
    allow_delegation=False,
    llm=llm
)

## Create a LLM Agent
LLM_agent = Agent(
    role='LLM Agent',
    goal='Assist in answering the query: {question}. This agent will utilize its knowledge to generate a direct answer based on internal understanding.Make sure you respond in less than 2 lines only.',
    verbose=True,
    memory=True,
    backstory=(
        "The LLM Agent is an expert in natural language processing. It is capable of understanding complex queries and generating "
        "answers from its trained knowledge base. The agent will rely on its pre-trained model to answer questions that do not require "
        "external web searches or retrieval.Make sure you respond in less than 2 lines only"
    ),
    allow_delegation=False,
    llm=llm
)
