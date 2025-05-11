import os
import openai
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import tkinter as tk
from tkinter import scrolledtext

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

recognizer = sr.Recognizer()
tts = pyttsx3.init()
tts.setProperty('rate', 180)

def speak(text):
    """Convert text to speech."""
    tts.say(text)
    tts.runAndWait()

def listen():
    """Listen to the user's voice input."""
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            query = recognizer.recognize_google(audio)
            return query
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except sr.RequestError:
            return "Network error."

def ask_chatgpt(prompt):
    """Send a prompt to ChatGPT and get a response using the latest OpenAI API."""
    try:
        client = openai.OpenAI()  
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def start_assistant():
    """Start the voice assistant."""
    user_input = listen()
    if user_input:
        chat_area.insert(tk.END, f"You: {user_input}\n")
        response = ask_chatgpt(user_input)
        chat_area.insert(tk.END, f"Assistant: {response}\n")
        chat_area.see(tk.END)
        speak(response)

def stop_assistant():
    """Stop the assistant."""
    speak("Goodbye! Have a great day!")
    root.destroy()

# Create the GUI
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("500x600")
root.configure(bg="#2c3e50")

# Title Label
title_label = tk.Label(root, text="Voice Assistant", font=("Helvetica", 20, "bold"), bg="#2c3e50", fg="#ecf0f1")
title_label.pack(pady=10)

# Chat Area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Helvetica", 12), bg="#34495e", fg="#ecf0f1", height=20, width=50)
chat_area.pack(pady=10)
chat_area.insert(tk.END, "Assistant: Hello! How can I assist you today?\n")

# Buttons
start_button = tk.Button(root, text="Start Listening", font=("Helvetica", 14), bg="#1abc9c", fg="#ffffff", command=start_assistant)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Exit", font=("Helvetica", 14), bg="#e74c3c", fg="#ffffff", command=stop_assistant)
stop_button.pack(pady=10)

# Run the GUI
root.mainloop()