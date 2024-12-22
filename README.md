# Interview CheatMate

**Your Secret Weapon for Interview Success**

## Overview

Interview CheatMate is an innovative tool designed to assist users in preparing for interviews by leveraging advanced AI models and technologies. It facilitates seamless, real-time conversations on a web-based platform, analyzes user queries, and provides targeted assistance through state-of-the-art natural language processing and agent-based decision-making systems.

---

## Features

### 1. Real-Time Conversational Interface

- Users can engage in natural conversations directly on a user-friendly Streamlit-based website.

### 2. Speech-to-Text Conversion

- Groq Whisper API is utilized to convert spoken interactions into text, which is stored in a buffer for further processing.

### 3. AI-Powered Question Analysis

- When a user requests help, Groq's Llama LLM analyzes the text buffer to extract the most relevant question based on the context of the conversation.

### 4. Intelligent Agent Designation

- The extracted question is processed by Crew AI’s agentic models, which include:
  - **Designator Agent**: Determines whether to route the query to:
    - **RAG (Retrieval-Augmented Generation)**: For personalized or document-based searches.
    - **Web Agent**: For tasks requiring web-based information retrieval.
    - **Direct LLM Response**: For straightforward general inquiries.

### 5. Advanced Retrieval Mechanisms

- **RAG Workflows**:
  - Semantic search powered by Pinecone vector database.
  - Sentence-transformer embeddings using the `all-MiniLM-L6-v2` model.
  - PDF content extraction facilitated by PyMuPDF.
  - Orchestration and integration via LangChain.

### 6. Web Search Integration

- Serper API enables robust web search capabilities to address information needs beyond local data.

### 7. Response Presentation

- Results are displayed in real-time on the website, ensuring users receive actionable insights promptly.

---

## Technical Stack

### Core Technologies

- **Frontend**: Streamlit for an interactive and intuitive user interface.
- **Backend**:
  - Groq Whisper API for Speech-to-Text.
  - Groq Llama LLM for question extraction and analysis.
  - Crew AI agentic models for task delegation and execution.

### Supporting Tools

- **Data Processing**:
  - PyMuPDF for PDF processing.
  - Sentence-Transformers for embedding generation.
- **Vector Storage**:
  - Pinecone for efficient and scalable vector-based data retrieval.
- **Web Search**:
  - Serper API integrated as a Crew AI tool for web search tasks.

---

## Installation

### Prerequisites

- Python 3.8 or higher.
- Virtual environment setup (recommended).

### Steps

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd AI-InterviewAssistant
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # For Linux/Mac
   .venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in a `.env` file:

   ```env
   SERPER_API_KEY=<your_serper_api_key>
   PINECONE_API_KEY=<your_pinecone_api_key>
   GROQ_API_KEY=<your_groq_api_key>
   ```

5. Run the application:

   ```bash
   streamlit run app.py
   ```

---

## Usage

1. Access the Streamlit-based website via the provided URL.
2. Click the "Record" button to capture your voice input. The transcribed text will appear in the text box below.
3. Engage in a conversation through the interface (either text or voice).
4. Click the "Help AI" button whenever assistance is needed.
5. View the AI-generated response tailored to your query.

---

## Future Enhancements

- Incorporate additional agentic capabilities for more nuanced task handling.
- Expand support for multiple languages in Speech-to-Text conversion.
- Integrate user feedback mechanisms to refine AI responses.

---

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with a detailed description of your changes.

---

