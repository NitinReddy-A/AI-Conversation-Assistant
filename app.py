import streamlit as st
import time
import sounddevice as sd
import soundfile as sf
import os
from groq import Groq
import numpy as np
import io
from datetime import datetime
from dotenv import load_dotenv
import queue
import threading
import time
#import openai
from CrewAI_Agents.main import delegate_task
# Load environment variables
load_dotenv()


# Configuration
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1024
MAX_RECORDING_SECONDS = 30

st.markdown("""
    <style>
    .stButton > button {
        background-color: #3498db;
        color: white;
        border: 2px solid white;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        padding: 15px 25px;
        font-size: 16px;
        font-weight: 500;
        width: 200px;
        margin: 10px;
    }
    .stButton > button:hover {
        background-color: #2980b9;
    }
    .conversation-text {
        font-family: monospace;
        white-space: pre-wrap;
        padding: 20px;
        color: black !important;
        background-color: white !important;
        border: 1px solid #ddd;
        border-radius: 5px;
        font-size: 16px;
        line-height: 1.5;
    }
    body {
        background-color: white !important;
        color: black !important;
    }
    p {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
#initialize openai key
#open_api_key = os.getenv("OPENAI_API_KEY")
if not groq_api_key:
    st.error("GROQ_API_KEY not found in environment variables")
    groq_client = None
else:
    try:
        groq_client = Groq(api_key=groq_api_key)
    except Exception as e:
        st.error(f"Error initializing Groq client: {e}")
        groq_client = None

class AudioRecorder:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.audio_thread = None

    def callback(self, indata, frames, time, status):
        if status:
            print(f'Error in audio callback: {status}')
        self.audio_queue.put(indata.copy())

    def start_recording(self):
        self.is_recording = True
        self.audio_thread = threading.Thread(target=self._record)
        self.audio_thread.start()

    def _record(self):
        with sd.InputStream(callback=self.callback,
                          channels=CHANNELS,
                          samplerate=SAMPLE_RATE):
            while self.is_recording:
                time.sleep(0.1)

    def stop_recording(self):
        self.is_recording = False
        if self.audio_thread:
            self.audio_thread.join()
        
        audio_chunks = []
        while not self.audio_queue.empty():
            audio_chunks.append(self.audio_queue.get())
        
        if audio_chunks:
            return np.concatenate(audio_chunks)
        return None

def transcribe_audio(audio_data):
    try:
        audio_data = audio_data / np.max(np.abs(audio_data))
        audio_bytes = io.BytesIO()
        sf.write(audio_bytes, audio_data, SAMPLE_RATE, format='WAV')
        audio_bytes.seek(0)

        transcription = groq_client.audio.transcriptions.create(
            file=("recording.wav", audio_bytes.read()),
            model="whisper-large-v3-turbo",
            response_format="json",
        )
        return transcription.text
    except Exception as e:
        st.error(f"Transcription error: {e}")
        return None

def initialize_session_state():
    if "recording" not in st.session_state:
        st.session_state.recording = False
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    if "audio_recorder" not in st.session_state:
        st.session_state.audio_recorder = AudioRecorder()
    if "current_speaker" not in st.session_state:
        st.session_state.current_speaker = None

def handle_person_recording(person_label):
    button_label = "Press to speak as\n" + person_label
    unique_key = f"{person_label}_record_button"

    if st.button(button_label, key=unique_key):
        if not st.session_state.recording:
            start_recording(person_label)
        elif st.session_state.current_speaker == person_label:
            stop_recording(person_label)

def start_recording(person_label):
    if not st.session_state.recording:
        st.session_state.recording = True
        st.session_state.current_speaker = person_label
        st.session_state.audio_recorder.start_recording()
        st.write(f"Recording {person_label}...")

def stop_recording(person_label):
    st.session_state.recording = False
    st.session_state.current_speaker = None
    audio_data = st.session_state.audio_recorder.stop_recording()
    
    if audio_data is not None:
        with st.spinner("Converting speech to text..."):
            transcribed_text = transcribe_audio(audio_data)
            if transcribed_text:
                st.session_state.conversation.append((person_label, transcribed_text))
                st.rerun()



def handle_help_from_ai():
    """
    Summarize the recent conversation between Person 1 and Person 2
    by combining the transcribed text into a single block and then
    generating a question using OpenAI's API.
    """
    # Get the current conversation
    transcribed_text = st.session_state.conversation

    # Filter conversation for Person 1 and Person 2 after the last AI response
    if "last_ai_index" not in st.session_state:
        st.session_state.last_ai_index = -1  # Initialize last AI index if not present

    start_index = st.session_state.last_ai_index + 1
    relevant_conversation = transcribed_text[start_index:]

    # Debugging: Print relevant conversation to check the data
    print("Relevant Conversation:", relevant_conversation)

    if relevant_conversation:
        # Combine only the text (not speaker labels) into a single string
        combined_text = " ".join([text for _, text in relevant_conversation])
        summarized_text = f"{combined_text}"
    else:
        summarized_text = "No new conversation available to analyze."

    # Call OpenAI to generate a question based on the summarized conversation
    try:
        # Use Groq's GPT to generate a question
        client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the interview conversation and generate a professional, one-line question focusing on topics like projects, internships, or relevant details. Ensure the question is clear, concise, and relevant to the context of the interview.Additionally, sometimes there can we generic question and try to keep relevency to the latest conversation"
                },
                {
                    "role": "user",
                    "content": f"Based on the following interview conversation, summarize and generate a professional, one-line question that is directly relevant to the discussion:\n\n{summarized_text}"
                }
            ],
            model="llama3-8b-8192",  # Replace with your desired Groq model
            max_tokens=150,
            temperature=0.7
        )
        response_dict = chat_completion.model_dump() 
        # Correctly access the message content in the response
        question = response_dict["choices"][0]["message"]["content"]
        
        # Add the question to the conversation
        st.session_state.conversation.append(("AI Question", question))

        # Update the AI's response index
        st.session_state.last_ai_index = len(st.session_state.conversation) - 1

        
        #time.sleep(4)

        ########################################################################################################
        response = delegate_task(question)

        # Add the question to the conversation
        st.session_state.conversation.append(("AI Answer", response))

        # Update the AI's response index
        st.session_state.last_ai_index = len(st.session_state.conversation) - 1

    # except openai.OpenAIError as e:
    #     st.error(f"OpenAI API Error: {e}")
    #     print(f"OpenAI API Error: {e}")  # This will print any OpenAI-specific errors

    except Exception as e:
        st.error(f"Error generating question: {e}")
        print(f"Error generating question: {e}")  # This will print any general errors

    # Rerun to update the UI
    st.rerun()

def main():
    st.title("Interview Helper")

    if not groq_client:
        st.error("Please configure your GROQ_API_KEY in the .env file")
        return

    initialize_session_state()

    # Center-align the buttons using columns
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        handle_person_recording("Person 1")

    with col2:
        handle_person_recording("Person 2")

    with col3:
        if st.button("Press to get\nHelp from AI", key="help_from_ai_button"):
            question =  handle_help_from_ai()


    # Display conversation in simple text format
    if st.session_state.conversation:
        conversation_text = ""
        for speaker, text in st.session_state.conversation:
            conversation_text += f"{speaker}: {text}\n"
        st.markdown(f'<div class="conversation-text">{conversation_text}</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
