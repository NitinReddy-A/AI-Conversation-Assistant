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
    goal='Determine the most appropriate agent to handle the given question: {question} if the RAG agent fails to find relevant context. Options: (1) Web Search Agent, (2) LLM Agent.',
    verbose=True,
    memory=True,
    backstory=(
        "The Designator Agent is an expert in understanding complex queries and determining the best approach to answering them. "
        "It will evaluate the provided question and recommend the appropriate method for addressing it, whether it requires a web search or a direct answer, "
        "if the RAG agent fails to find relevant context."
    ),
    allow_delegation=True,
    llm=llm
)

## Create a RAG Agent
rag_agent = Agent(
    role='RAG Agent',
    goal='Retrieve relevant information and generate a comprehensive answer to the given question: {question} using the provided context: {context}.',
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
    goal='Assist in answering the query: {question} by searching the web and summarizing relevant information. Provide a summary of the search results and answer the question in less than 1 line only.',
    verbose=True,
    memory=True,
    backstory=(
        "The Web Search Agent is skilled at finding and summarizing information from the internet. "
        "It will search the web for relevant data and provide a concise summary to answer the question."
    ),
    tools=[Web_tool],
    allow_delegation=True,
    llm=llm
)

## Create an LLM Agent
LLM_agent = Agent(
    role='LLM Agent',
    goal='Provide a direct answer to the given question: {question} based on internal knowledge and reasoning. Generate a precise, clear response in less than 1 line only.',
    verbose=True,
    memory=True,
    backstory=(
        "The LLM Agent is an expert in generating direct answers based on its internal knowledge and reasoning capabilities. "
        "It will provide a precise and clear response to the question without requiring external information."
    ),
    allow_delegation=True,
    llm=llm
)
