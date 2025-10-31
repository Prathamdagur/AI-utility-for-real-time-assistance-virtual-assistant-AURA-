"""
speak.py – Text-to-Speech Module
Speaks responses using pyttsx3.
"""

import pyttsx3
import logging

class VoiceSpeaker:
    def __init__(self, rate=160, volume=1.0, voice_gender="female"):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            self.set_voice(voice_gender)
        except Exception as e:
            logging.error(f"Failed to initialize speech engine: {e}")
            self.engine = None

    def set_voice(self, gender):
        try:
            voices = self.engine.getProperty('voices')
            # Prefer female/male voice by name if available
            if gender == "female":
                for v in voices:
                    if any(name in v.name.lower() for name in ["female", "zira", "hazel"]):
                        self.engine.setProperty('voice', v.id)
                        return True
            else:
                for v in voices:
                    if any(name in v.name.lower() for name in ["male", "david", "james"]):
                        self.engine.setProperty('voice', v.id)
                        return True
            
            # If no matching voice found, use first available
            if voices:
                self.engine.setProperty('voice', voices[0].id)
                return True
            return False
        except Exception as e:
            logging.error(f"Failed to set voice: {e}")
            return False

    def speak(self, text):
        """Speak the given text using text-to-speech."""
        if not text or not self.engine:
            return False
        
        try:
            self.engine.stop()  # Stop any ongoing speech
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            logging.error(f"Speech error: {e}")
            return False

    def test_voices(self):
        """Test available voices."""
        if not self.engine:
            logging.error("Speech engine not initialized")
            return
            
        voices = self.engine.getProperty('voices')
        for voice in voices:
            try:
                self.engine.setProperty('voice', voice.id)
                print(f"Testing voice: {voice.name}")
                self.speak("Hello, I am a voice test.")
            except Exception as e:
                print(f"Error testing voice {voice.name}: {e}")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Test the speaker
    speaker = VoiceSpeaker()
    if speaker.engine:
        speaker.speak("Hello! I'm your voice assistant.")
