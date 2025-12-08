# AURA – AI utility for real time assistance 

AURA is a local desktop voice assistant built with Python. It performs speech recognition, command processing, automation, task management, web search and offline text-to-speech.

## Features
- Speech recognition and offline TTS
- Open/close desktop applications
- Web search and YouTube playback
- Wikipedia lookup
- Task and reminder management
- System information monitoring
- Basic math and browser tab control

## Installation
pip install speechrecognition pyttsx3 psutil flask requests wikipedia pyautogui

## Run the Voice Assistant
python main_voice.py

## Run the Local API Server
python server.py

POST http://localhost:5000/api/command
Body: { "command": "open youtube" }

## Example Commands
open notepad  
close chrome  
search machine learning  
wikipedia galaxy  
add task buy groceries  
system info  
calculate 22 * 11  


