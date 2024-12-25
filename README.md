# 🔹 AI Conversation Assistant

**🌟 Your Secret Weapon for Perfect Conversations! 🌟**

---

## 🔎 Overview

Say hello to **AI Conversation Assistant** – your ultimate AI buddy for smooth, real-time interactions! 🌚 It’s designed to answer questions, solve problems, and provide personalized help, all through an easy-to-use web platform. Whether you need quick info or in-depth guidance, we’ve got your back. 🤖✨

---

## 🔧 Features

### ⭐ 1. Real-Time Conversational Interface

🔗 Chat naturally on a user-friendly **Streamlit-based website** – no tech skills needed!

### 🗣️ 2. Speech-to-Text Conversion

🎤 Powered by Groq’s `whisper-large-v3-turbo LLM`, turning your voice into text with ease.

### 🕵️‍♂️ 3. AI-Powered Question Analysis

🤔 Groq’s `gemma2-9b-it LLM` dives into the conversation to pull out the most relevant questions.

### 🚀 4. Intelligent Agent Designation

🙌 Crew AI’s smart models figure out where to route your query:
- **RAG (Retrieval-Augmented Generation)**: For deep dives into personalized or document-based info.
- **Web Agent**: Perfect for web-based searches.
- **Direct LLM Response**: For quick, no-fuss answers.

### 📈 5. Advanced Retrieval Mechanisms

- **RAG Workflow Highlights**:
  - 🧠 Semantic search powered by `Pinecone` Vector DB.
  - 🔍 Precise embeddings via `all-MiniLM-L6-v2` sentence transformer model.
  - 📄 Extracting PDFs using  `Pymupdf`.
  - 🛠️ Smooth integration through `LangChain`.

### 🔍 6. Web Search Integration

🌐 With `Serper AI`'s API, fetch the freshest web data on the go.

### 🔹 7. Real-Time Results

🔥 Get answers fast, displayed right on the website. No waiting around!

---

## 🧬 Technical Stack

### Core Technologies

- 🔹 **Frontend**: Streamlit for intuitive interfaces.
- 🔹 **Backend**:
  - Groq's `whisper-large-v3-turbo` for Speech-to-Text.
  - Groq's `gemma2-9b-it` for question analysis.
  - `Crew AI` agentic models for smart task management.

### Supporting Tools

- 🌍 **Data Processing**:
  - `PyMuPDF` for PDFs.
  - `all-MiniLM-L6-v2` for embeddings.
- 🌐 **Web Search**: `Serper AI`'s API integrated with Crew AI tools.
- 🧠 **Vector Storage**: `Pinecone` for blazing-fast retrieval.

---

## 🛠️ Installation

### Prerequisites

- 🔸 Python 3.8+.
- 🔸 Virtual environment setup (recommended).

### Steps

1. **Clone the repository**:

   ```bash
   git clone <repository_url>
   cd AI-Conversation-Assistant
   ```

2. **Set up a virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:

   Create a `.env` file:
   ```env
   SERPER_API_KEY=<your_serper_api_key>
   PINECONE_API_KEY=<your_pinecone_api_key>
   GROQ_API_KEY=<your_groq_api_key>
   ```

5. **Run the application**:

   ```bash
   streamlit run app.py
   ```

---

## 🚀 Usage

1. Open the Streamlit website.
2. Hit the “Record” button to capture voice input. 🎤
3. Watch as your words turn into text in real time. 🔍
4. Chat away! For extra help, click “Help AI” and get spot-on answers. 🌟
5. Enjoy a smooth, engaging conversation experience. 🙌

---

## 💡 Future Enhancements

- 🌐 Support for multiple languages.
- 🛠️ Smarter agentic task handling.
- 🔸 User feedback integration for AI improvements.

---

## 📢 Contributing

🙏 We’d love your help! Follow these steps to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with details about your changes.

---

