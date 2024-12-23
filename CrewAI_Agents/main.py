from crewai import Crew
from CrewAI_Agents.agents import Designator_agent, web_agent, LLM_agent, rag_agent
from CrewAI_Agents.task import designation_task, web_task, llm_task, rag_task
from dotenv import load_dotenv

load_dotenv()

import os
pinecone_api_key = os.getenv("PINECONE_API_KEY")

# Initialize RAG Crew
rag_crew = Crew(
    agents=[rag_agent],
    tasks=[rag_task],
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# Initialize Designator Crew
designator_crew = Crew(
    agents=[Designator_agent],
    tasks=[designation_task],
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# Initialize Web Search Crew
web_crew = Crew(
    agents=[web_agent],
    tasks=[web_task],
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# Initialize LLM Crew
llm_crew = Crew(
    agents=[LLM_agent],
    tasks=[llm_task],
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# Define the sequence of execution
def execute_task(question, context):
    # Step 1: Use RAG agent to find relevant context
    rag_response = rag_crew.kickoff(question=question, context=context)
    
    if "no relation" in rag_response.lower():
        # Step 2: Use Designator agent to choose the appropriate agent
        agent_choice = designator_crew.kickoff(question=question)
        
        if "web search agent" in agent_choice.lower():
            # Step 3: Use Web Search Agent
            return web_crew.kickoff(question=question)
        else:
            # Step 3: Use LLM Agent
            return llm_crew.kickoff(question=question)
    else:
        return rag_response

# Example usage
# question = "What is the capital of France?"
# context = ""
# response = execute_task(question, context)
# print(response)
