import os
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import torch
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PdfProcessor:
    def _init_(self, api_key, index_name, use_gpu=False):
        self.device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        self.query_prompt_name = "s2p_query"
        self.setup_pinecone(api_key, index_name)
        self.setup_model()
        
    def setup_pinecone(self, api_key, index_name):
        try:
            self.pc = Pinecone(api_key=api_key)
            self.index = self.pc.Index(index_name)
            logger.info("Pinecone connection established successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {str(e)}")
            raise

    def setup_model(self):
        try:
            self.model =SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
            logger.info(f"Model initialized on {self.device}")
        except Exception as e:
            logger.error(f"Error loading SentenceTransformer model: {str(e)}")
            raise

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        try:
            doc = fitz.open(pdf_path)
            text = " ".join(page.get_text() for page in doc)
            doc.close()
            if not text.strip():
                logger.warning(f"No text extracted from {pdf_path}")
            return text
        except Exception as e:
            logger.error(f"Failed to extract text from {pdf_path}: {str(e)}")
            return ""

    @staticmethod
    def chunk_text(text, chunk_size=500, chunk_overlap=100):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        return splitter.split_text(text)

    def generate_embeddings(self, chunks, pdf_file, is_query=False):
        try:
            if is_query:
                embeddings = self.model.encode(
                    chunks,
                    prompt_name=self.query_prompt_name,
                    convert_to_tensor=True
                )
            else:
                embeddings = self.model.encode(chunks, convert_to_tensor=True)

            logger.info(f"Generated embeddings for {pdf_file}, shape: {embeddings.shape}")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings for {pdf_file}: {str(e)}")
            return None

    def process_and_push_to_pinecone(self, folder_path, batch_size=100):
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder path not found: {folder_path}")

        pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
        
        for pdf_file in tqdm(pdf_files, desc="Processing PDF files"):
            try:
                pdf_path = os.path.join(folder_path, pdf_file)
                text = self.extract_text_from_pdf(pdf_path)
                if not text.strip():
                    logger.warning(f"Skipping {pdf_file} due to empty text extraction")
                    continue

                chunks = self.chunk_text(text)
                embeddings = self.generate_embeddings(chunks, pdf_file)

                if embeddings is None:
                    logger.warning(f"Skipping {pdf_file} due to failed embeddings")
                    continue

                for i in range(0, len(embeddings), batch_size):
                    batch_embeddings = embeddings[i:i + batch_size]
                    vectors = [
                        {
                            "id": f"{pdf_file}-{j}",
                            "values": embedding.tolist(),
                            "metadata": {"source": pdf_file, "chunk": j, "text": chunks[j]}
                        }
                        for j, embedding in enumerate(batch_embeddings, start=i)
                    ]
                    self.index.upsert(vectors=vectors)
            except Exception as e:
                logger.error(f"Error processing {pdf_file}: {str(e)}")

    def query_similarity(self, queries, docs):
        try:
            query_embeddings = self.generate_embeddings(queries, "queries", is_query=True)
            doc_embeddings = self.generate_embeddings(docs, "docs")

            if query_embeddings is None or doc_embeddings is None:
                logger.warning("Failed to generate embeddings for queries or documents")
                return None

            similarities = self.model.similarity(query_embeddings, doc_embeddings)
            logger.info(f"Similarity matrix shape: {similarities.shape}")
            return similarities
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            return None

def main():
    try:
        api_key = "pcsk_6RHz6Y_LbWKy2peojQDozzxQJCUh95UwNvJeq1uLmcrmtYUFcQaUZGVzNkz6p2UakPBLf5"
        index_name = "assignment"
        folder_path = "data"

        processor = PdfProcessor(api_key, index_name, use_gpu=False)
        processor.process_and_push_to_pinecone(folder_path)

        # query = ["Nitin Kumar Reddy resume experience with HPE and Pinecone"]
        # response = processor.index.query(query, top_k=5, include_metadata=True)
        # print(response)

        
        logger.info("All PDF files processed and uploaded to Pinecone successfully")
    except Exception as e:
        logger.error(f"Main execution failed: {str(e)}")
        raise

if __name__ == "__main__":
   main()
