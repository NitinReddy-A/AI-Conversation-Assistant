import torch
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# Initialize Pinecone and SentenceTransformer
def initialize(api_key, index_name, use_gpu=False):
    device = "cpu"
    model = SentenceTransformer("all-MiniLM-L6-v2", device=device)
    
    # Initialize Pinecone with API Key
    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)
    return model, index

# Perform the query
def search_query(model, index, query, top_k=5):
    try:
        # Encode the query into a vector using the SentenceTransformer model
        query_vector = model.encode(query).tolist()

        # Query the Pinecone index
        results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)

        # Print results with the retrieved text and metadata
        for result in results['matches']:
            score = round(result['score'], 5)
            text = result['metadata'].get('text', 'No Text Found')
            source = result['metadata'].get('source', 'Unknown Source')
            # print(f"Score: {score} - Text: {text} - Source: {source}")
            print("result:", type(str(result)))
            text = result['metadata']['text']
            return text
    
    except Exception as e:
        print(f"Search query failed: {str(e)}")

# if __name__ == "__main__":
#     api_key = "pcsk_6RHz6Y_LbWKy2peojQDozzxQJCUh95UwNvJeq1uLmcrmtYUFcQaUZGVzNkz6p2UakPBLf5"  # Replace with your actual PineconeAPI key
#     index_name = "assignment"  # Replace with your actual Pinecone index name
#     query = "Restaurant management and food wastage"

#     # Initialize the model and index, then perform the search query
#     model, index = initialize(api_key, index_name, use_gpu=False)
#     res = search_query(model,index,query)
#     print(res)