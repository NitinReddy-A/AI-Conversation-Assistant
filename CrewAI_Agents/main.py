from crewai import Crew
from CrewAI_Agents.agents import Designator_agent, web_agent, LLM_agent,rag_agent
from CrewAI_Agents.task import designation_task, web_task, llm_task,rag_task
from RAG_Embeddings.queryVDB import initialize, search_query
from dotenv import load_dotenv

load_dotenv()

import os
pinecone_api_key= os.getenv("PINECONE_API_KEY")


crew = Crew(
    agents=[Designator_agent], 
    tasks=[designation_task], 
    #process=Process.parallel, 
    memory=True, 
    cache=True, 
    max_rpm=100,
    share_crew=True 
)
crew1 = Crew(
    agents=[LLM_agent], 
    tasks=[llm_task], 
    #process=Process.parallel, 
    memory=True, 
    cache=True, 
    max_rpm=100,
    share_crew=True 
)

crew2 = Crew(
    agents=[web_agent], 
    tasks=[web_task], 
    #process=Process.parallel, 
    memory=True, 
    cache=True, 
    max_rpm=100,
    share_crew=True 
)

crew3 = Crew(
    agents=[rag_agent], 
    tasks=[rag_task], 
    #process=Process.parallel, 
    memory=True, 
    cache=True, 
    max_rpm=100,
    share_crew=True 
)


def delegate_task(question):

    try:
        designation_result = crew.kickoff(inputs={'question': question})
        
        print("Type of designation_result:", type(designation_result))
        print(designation_result)
        designation_result_string = str(designation_result)
        print(designation_result_string)
        
        if designation_result_string == 'Web Search Agent':
            web_result = crew2.kickoff(inputs={'question': question})
            print("Web search result:", web_result)
            return web_result
        
        elif designation_result_string == 'LLM Agent':
            llm_result = crew1.kickoff(inputs={'question': question})
            print(f"LLM agent result:{llm_result}")
            return llm_result
        
        elif designation_result_string == 'RAG':
            model, index = initialize(pinecone_api_key, "assignment", use_gpu=False)
            rag_result =  search_query(model,index,question)
            llm_result = crew3.kickoff(inputs={'question': question, 'context': rag_result})
            print(f"LLM agent result:{llm_result}")
            return llm_result
        
        else:
            print(f"No valid agent found for the task: {designation_result}")
            return None
    except Exception as e:
        print(f"Error in task delegation: {e}")
        return None

# input_question = 'Can you elaborate on your experience working on the "Income Tax GPT" project and its specific contributions?'
# result = delegate_task(input_question)
# print("Final result:", result)
