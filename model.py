import re
import datetime
import subprocess
import webbrowser
import os
import wikipedia
from urllib.parse import quote_plus
import psutil
import math
import requests

class CommandProcessor:
    def __init__(self):
        # Basic app paths for Windows 
        self.app_paths = {
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "comet": r"C:\Users\dagur\AppData\Local\Programs\CometBrowser\comet.exe", 
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
            "spotify": r"C:\Users\YourUsername\AppData\Roaming\Spotify\Spotify.exe",  
            "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
            "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"
        }
        
        # Web services and URLs
        self.web_services = {
            "linkedin": "https://www.linkedin.com",
            "youtube": "https://www.youtube.com",
            "github": "https://github.com",
            "gmail": "https://mail.google.com",
            "maps": "https://www.google.com/maps",
            "twitter": "https://twitter.com",
            "facebook": "https://facebook.com",
            "instagram": "https://instagram.com",
            "amazon": "https://amazon.com",
            "netflix": "https://netflix.com",
            "weather": "https://weather.com",
            "news": "https://news.google.com",
            "translate": "https://translate.google.com",
            "drive": "https://drive.google.com",
            "calendar": "https://calendar.google.com"
        }
        
        self.start_time = datetime.datetime.now()
        self.last_opened_app = None
        self.browser_process_names = ["chrome.exe", "msedge.exe", "firefox.exe", "opera.exe", "comet.exe"]
        self.default_browser = "comet" 
        
        # Casual conversation data
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What did the grape say when it got stepped on? Nothing, it just let out a little wine!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why did the cookie go to the doctor? Because it was feeling crumbly!"
        ]
        
        self.fun_facts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old!",
            "Cows have best friends and get stressed when separated from them.",
            "The first oranges weren't orange! The original oranges from Southeast Asia were actually green.",
            "A day on Venus is longer than its year! Venus takes 243 Earth days to rotate on its axis.",
            "Penguins propose to their life mates with a pebble!"
        ]
        
        self.hobbies_responses = [
            "I love learning new things! What about you?",
            "I enjoy processing data and helping people. It's kind of my thing!",
            "Chatting with humans is definitely one of my favorite activities!",
            "I find solving problems and helping people quite fulfilling!",
            "I'm passionate about making tasks easier for humans. It's my purpose!"
        ]
        
        self.mood_responses = {
            "good": ["That's wonderful to hear!", "Awesome! Keep that positive energy!", "Great! Your good mood is contagious!"],
            "bad": ["I'm sorry to hear that. Tomorrow will be better!", "Remember, every cloud has a silver lining!", "Hang in there! Things will improve!"],
            "okay": ["Sometimes okay is perfectly fine!", "That's alright, steady and stable is good!", "Nothing wrong with being okay!"]
        }
        
        self.interests = [
            "Technology is fascinating! The way it evolves every day is amazing.",
            "I find human creativity incredibly interesting. You all think in such unique ways!",
            "Space exploration really captures my imagination. The universe is so vast!",
            "Art and music are beautiful aspects of human culture.",
            "I'm curious about everything! What interests you?"
        ]
        
        # Initialize features
        self.notes = []  # Store quick notes
        self.tasks = []  # Store tasks
        self.custom_apps = {} 
        
        # Command history tracking
        self.command_history = []
        self.max_history = 100 

    def process(self, command):
        """Process voice commands and return text response."""
        if not command:
            return ""
            
        # Clean the command
        cmd = command.lower().strip()
        
        # Ignore if command is just punctuation or whitespace
        if not cmd or cmd.isspace() or all(c in '.,/#!$%^&*;:{}=-_`~' for c in cmd):
            return ""
            
        print(f"[DEBUG] Processing command: '{cmd}'")  # Debug log
        
        # Add command to history (except for undo/close commands)
        if not any(word in cmd for word in ['undo', 'close']):
            self.command_history.append({
                'command': cmd,
                'timestamp': datetime.datetime.now(),
                'app_opened': None
            })
            # Trim history if too long
            if len(self.command_history) > self.max_history:
                self.command_history.pop(0)

        # Notes/Reminders management
        if "remind me to" in cmd:
            note = cmd.replace("remind me to", "").strip()
            if note:
                self.notes.append(note)
                return f"I'll remind you to {note}"
            return "Please specify what you'd like me to remind you about."
            
        if "read notes" in cmd or "show notes" in cmd or "show reminders" in cmd:
            if self.notes:
                return "Your reminders:\n" + "\n".join(f"{i+1}. {note}" for i, note in enumerate(self.notes))
            return "You don't have any reminders yet."
            
        if "clear notes" in cmd or "clear reminders" in cmd:
            self.notes = []
            return "All reminders have been cleared."
            
        # Task management
        if "add task" in cmd:
            task = cmd.replace("add task", "").strip()
            if task:
                self.tasks.append({"task": task, "completed": False})
                return f"Task added: {task}"
            return "Please specify the task."
            
        if "show tasks" in cmd or "list tasks" in cmd:
            if self.tasks:
                tasks_list = []
                for i, task in enumerate(self.tasks):
                    status = "✓" if task["completed"] else "○"
                    tasks_list.append(f"{i+1}. [{status}] {task['task']}")
                return "Your tasks:\n" + "\n".join(tasks_list)
            return "You don't have any tasks yet."
            
        if "complete task" in cmd:
            try:
                task_num = int(''.join(filter(str.isdigit, cmd))) - 1
                if 0 <= task_num < len(self.tasks):
                    self.tasks[task_num]["completed"] = True
                    return f"Marked task {task_num + 1} as completed."
                return "Invalid task number."
            except ValueError:
                return "Please specify the task number to complete."
                
        if "clear tasks" in cmd:
            self.tasks = []
            return "All tasks have been cleared."
            
        # Custom app management
        if "add app path" in cmd:
            parts = cmd.replace("add app path", "").strip().split("as")
            if len(parts) == 2:
                path = parts[0].strip()
                name = parts[1].strip()
                self.custom_apps[name] = path
                return f"Added {name} with path: {path}"
            return "Please specify both the path and name for the app."

        # Casual Conversation
        if re.search(r'\b(how are you|how\'s it going|how do you feel)\b', cmd):
            return "I'm doing great, thanks for asking! I'm always happy to chat and help. How are you?"

        # Handle user's mood responses
        if re.search(r'i(?:\s+am|\'m)\s+(good|great|happy|amazing|excellent)', cmd):
            return self.mood_responses["good"][int(datetime.datetime.now().timestamp()) % 3]
        if re.search(r'i(?:\s+am|\'m)\s+(bad|sad|depressed|unhappy|terrible)', cmd):
            return self.mood_responses["bad"][int(datetime.datetime.now().timestamp()) % 3]
        if re.search(r'i(?:\s+am|\'m)\s+(okay|fine|alright|not bad)', cmd):
            return self.mood_responses["okay"][int(datetime.datetime.now().timestamp()) % 3]

        # Tell a joke
        if re.search(r'\b(tell\s+(?:me\s+)?a\s+joke|make\s+me\s+laugh|joke)\b', cmd):
            return self.jokes[int(datetime.datetime.now().timestamp()) % len(self.jokes)]

        # Share a fun fact
        if re.search(r'\b(tell\s+(?:me\s+)?a\s+fact|fun\s+fact|interesting\s+fact)\b', cmd):
            return self.fun_facts[int(datetime.datetime.now().timestamp()) % len(self.fun_facts)]

        # Talk about hobbies/interests
        if re.search(r'\b(what\s+do\s+you\s+like|your\s+hobbies|what\s+interests\s+you)\b', cmd):
            return self.hobbies_responses[int(datetime.datetime.now().timestamp()) % len(self.hobbies_responses)]

        # Share capabilities and self-introduction
        if re.search(r'\b(tell\s+me\s+about\s+yourself|what\s+do\s+you\s+think\s+about|what\s+can\s+you\s+do)\b', cmd):
            capabilities = [
                "Hello! I'm AURA, your digital assistant. Here's what I can do for you:",
                " App Control: I can open and close applications like Chrome, Comet browser, Notepad, Calculator, and more",
                " Web Services: I can help you with YouTube, Google Maps, Gmail, LinkedIn, and other web services",
                " Task Management: I can maintain your to-do list and set reminders",
                " Web Search: I can search the web and find information on Wikipedia",
                " Calculator: I can perform basic calculations",
                " Browser Control: I can manage tabs (new, close, switch) in your browser",
                " Conversation: I can chat, tell jokes, share fun facts, and respond to your mood",
                " System Info: I can monitor your system's CPU, memory, and disk usage",
                "Feel free to ask me to help with any of these tasks!"
            ]
            return "\n".join(capabilities)

        # Favorite things
        if re.search(r'what\'s\s+your\s+favorite\b', cmd):
            return "That's a tricky one for an AI! I appreciate all kinds of things but I especially enjoy our conversations and helping you out!"

        # Casual thanks
        if re.search(r'\b(thank you|thanks)\b', cmd):
            return "You're welcome! It's my pleasure to help!"

        # Basic greetings with more variety
        if re.search(r'\b(hello|hi|hey)\b', cmd):
            greetings = [
                "Hello! How can I help you today?",
                "Hi there! Always nice to chat with you!",
                "Hey! What's on your mind?",
                "Greetings! How can I assist you?",
                "Hi! Ready to help whenever you need!"
            ]
            return greetings[int(datetime.datetime.now().timestamp()) % len(greetings)]

        # Open Applications with typing/searching capability
        elif match := re.search(r'open (\w+)(?: and (?:type|search)(?: for)? (.+))?', cmd):
            app = match.group(1)
            text_to_type = match.group(2) if match.group(2) else None
            path = self.custom_apps.get(app) or self.app_paths.get(app)
            
            if path:
                try:
                    import pyautogui
                    import time
                    
                    # Special handling for Comet browser
                    if app.lower() == "comet":
                        if text_to_type:
                            webbrowser.get('comet').open_new_tab(f"https://www.google.com/search?q={quote_plus(text_to_type)}")
                            return f"Opening Comet and searching for '{text_to_type}'"
                        else:
                            webbrowser.get('comet').open_new_tab('about:blank')
                            return "Opening Comet browser."
                    
                    # Open other applications
                    if path.startswith("http"):
                        webbrowser.open(path)
                    else:
                        subprocess.Popen(path)
                    
                    self.last_opened_app = app
                    
                    # Update the last command's app_opened field
                    if self.command_history:
                        self.command_history[-1]['app_opened'] = app
                    
                    # If there's text to type, wait briefly for the app to open then type
                    if text_to_type:
                        time.sleep(2)  # Wait for app to open
                        pyautogui.write(text_to_type)
                        pyautogui.press('enter')
                        return f"Opening {app} and typing '{text_to_type}'"
                    
                    return f"Opening {app}."
                except Exception as e:
                    print(f"[DEBUG] Error opening {app}: {e}")
                    return f"Failed to open {app}."
            else:
                return f"App {app} not found in my database."

        # Undo command
        elif re.search(r'\bundo\b', cmd):
            if not self.command_history:
                return "No previous commands to undo."
            
            last_cmd = self.command_history[-1]
            if match := re.search(r'open (\w+)', last_cmd['command']):
                app = match.group(1)
                result = self.close_application(app)
                self.command_history.pop()  # Remove the command we just undid
                return f"Undoing last command: {result}"
            return "Cannot undo the last command automatically."

        # Close command
        elif re.search(r'close', cmd):
            if self.last_opened_app:
                result = self.close_application(self.last_opened_app)
                closed_name = self.last_opened_app
                self.last_opened_app = None
                return f"Closing {closed_name}. {result}"
            # Try close specific app if mentioned
            match = re.search(r'close (\w+)', cmd)
            if match:
                return self.close_application(match.group(1))
            return "No recent application to close."

        # Time and Date queries
        elif re.search(r'\b(what\s+time|current\s+time|time\s+now)\b', cmd):
            return datetime.datetime.now().strftime("The time is %I:%M %p.")
            
        elif re.search(r'\b(what\s+date|today\'s\s+date|current\s+date)\b', cmd):
            return datetime.datetime.now().strftime("Today is %A, %B %d, %Y.")

        # YouTube playback
        elif match := re.search(r'play (.+?)(?:\s+on\s+youtube|\s*$)', cmd):
            query = quote_plus(match.group(1))
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            return f"Opening YouTube and searching for {match.group(1)}."
            
        # Tab management commands
        elif cmd == "new tab":
            try:
                webbrowser.get('comet').open_new_tab('about:blank')
            except:
                webbrowser.open_new_tab('about:blank')
            return "Opening new tab."
            
        elif cmd == "close tab":
            import pyautogui
            time.sleep(0.5)  # Small delay to ensure command is ready
            pyautogui.hotkey('ctrl', 'w')
            return "Closing current tab."
            
        elif cmd == "close all tabs":
            import pyautogui
            time.sleep(0.5)  # Small delay to ensure command is ready
            pyautogui.hotkey('alt', 'f4')  # Close entire window
            return "Closing all tabs."
            
        elif cmd == "next tab":
            import pyautogui
            time.sleep(0.5)  # Small delay to ensure command is ready
            pyautogui.hotkey('ctrl', 'tab')
            return "Switching to next tab."
            
        elif cmd == "previous tab":
            import pyautogui
            time.sleep(0.5)  # Small delay to ensure command is ready
            pyautogui.hotkey('ctrl', 'shift', 'tab')
            return "Switching to previous tab."
            
        # Web services
        elif match := re.search(r'open\s+(?:web\s+)?(?:service\s+)?(\w+)(?:\s+and\s+(?:search|type)\s+(.+))?', cmd):
            service = match.group(1).lower()
            query = match.group(2)
            
            if service in self.web_services:
                url = self.web_services[service]
                if query:
                    if service == "youtube":
                        url += f"/results?search_query={quote_plus(query)}"
                    elif service == "maps":
                        url += f"/search/{quote_plus(query)}"
                    elif service in ["github", "twitter", "amazon"]:
                        url += f"/search?q={quote_plus(query)}"
                    else:
                        url += f"/search?q={quote_plus(query)}"
                webbrowser.open(url)
                return f"Opening {service}" + (f" and searching for {query}" if query else "")
            
        # Search Google (keep this after other search handlers)
        elif match := re.search(r'search (.+)', cmd):
            query = quote_plus(match.group(1))
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching for {match.group(1)}."

        # Wikipedia
        elif match := re.search(r'wikipedia (.+)', cmd):
            topic = match.group(1)
            try:
                summary = wikipedia.summary(topic, sentences=2)
                return summary
            except Exception as e:
                print(f"[DEBUG] Wikipedia error: {e}")
                return f"I couldn't find information about {topic} on Wikipedia."

        # Answer short factual questions (what/how/who/explain)
        elif match := re.search(r'^(what|how|who|explain)\s+(.+)', cmd):
            qtype = match.group(1)
            query = match.group(2)
            print(f"[DEBUG] Question detected ({qtype}): {query}")

            # DuckDuckGo Instant Answer API first (no API key)
            try:
                ddg_q = quote_plus(query)
                ddg_url = f"https://api.duckduckgo.com/?q={ddg_q}&format=json&no_redirect=1&no_html=1"
                r = requests.get(ddg_url, timeout=5)
                if r.ok:
                    data = r.json()
                    abstract = data.get('Abstract') or ''
                    if abstract:
                        return self._shorten(abstract, 2)

                    # RelatedTopics as fallback
                    related = data.get('RelatedTopics', [])
                    for item in related:
                        text = item.get('Text') if isinstance(item, dict) else ''
                        if text:
                            return self._shorten(text, 2)
            except Exception as e:
                print(f"[DEBUG] DuckDuckGo error: {e}")

            # Fallback to Wikipedia search
            try:
                summary = wikipedia.summary(query, sentences=2)
                return summary
            except Exception as e:
                print(f"[DEBUG] Fallback Wikipedia error: {e}")
                return f"I couldn't find a concise answer for {query}. I can search the web if you'd like."

        # Goodbye
        elif re.search(r'\b(goodbye|exit)\b', cmd):
            return "Goodbye! Have a great day!"

        # Calculator
        elif match := re.search(r'calculate\s+(.*)', cmd):
            expr = match.group(1).replace('x', '*')
            try:
                # Safely evaluate basic math with limited functions
                allowed = {k: v for k, v in math.__dict__.items() 
                         if k in ('sin', 'cos', 'tan', 'sqrt', 'pi')}
                result = eval(expr, {"__builtins__": {}}, allowed)
                return f"The result is {result}"
            except Exception:
                return "Sorry, I couldn't calculate that. Try something like '2 + 2' or 'sqrt(16)'."

        # System Info
        elif re.search(r'system\s+info', cmd):
            try:
                cpu = psutil.cpu_percent(interval=1)
                mem = psutil.virtual_memory().percent
                disk = psutil.disk_usage('/').percent
                return f"System Status: CPU usage: {cpu}%, Memory usage: {mem}%, Disk usage: {disk}%"
            except Exception as e:
                print(f"[DEBUG] System info error: {e}")
                return "Sorry, I couldn't get the system information."

        else:
            # Only return the "don't understand" message for non-empty, actual commands
            if len(cmd.strip()) > 0 and not all(c in '.,/#!$%^&*;:{}=-_`~' for c in cmd):
                return "Sorry, I don't understand that command."
            return ""

    def _shorten(self, text, max_sentences=2):
        # Return up to max_sentences sentences from text
        if not text:
            return ''
        # Split sentences on terminal punctuation
        parts = re.split(r'(?<=[\.\?\!])\s+', text.strip())
        if len(parts) <= max_sentences:
            return ' '.join(parts).strip()
        return ' '.join(parts[:max_sentences]).strip()

    def close_application(self, app):
        """Close a running application by process name."""
        exe_name = None
        
        # Map app names to executable names
        exe_map = {
            "notepad": "notepad.exe",
            "calculator": "Calculator.exe",
            "calc": "Calculator.exe",
            "chrome": "chrome.exe",
            "comet": "comet.exe",
            "spotify": "Spotify.exe",
            "word": "WINWORD.EXE",
            "excel": "EXCEL.EXE",
            "powerpoint": "POWERPNT.EXE"
            
        }
        
        # Handle browser-specific cases
        if app.lower() in ["comet", "chrome"]:
            import pyautogui
            import time
            try:
                time.sleep(0.5)
                pyautogui.hotkey('alt', 'f4')
                return f"Closing {app} browser."
            except Exception as e:
                print(f"[DEBUG] Keyboard shortcut failed: {e}")
        
        exe_name = exe_map.get(app.lower())
        
        if exe_name:
            found = False
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] and proc.info['name'].lower() == exe_name.lower():
                        proc.terminate()
                        found = True
                except Exception:
                    pass
            if found:
                return f"Closed {app}."
            else:
                return f"No running process found for {app}."
        else:
            return f"Cannot close {app} automatically."
