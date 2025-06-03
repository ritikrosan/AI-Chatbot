from flask import Flask, render_template, request, jsonify
import threading
import webbrowser
import os
import datetime
import wikipedia
import pyjokes
import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from assistant import speak, take_command, wish_user, get_weather, get_news, set_reminder, search_web, calculate, system_control, get_definition

app = Flask(__name__)

# Configure Wikipedia
wikipedia.set_lang("en")

# HTML Template with all improvements
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Voice Assistant</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        :root {
            --primary-color: #4361ee;
            --secondary-color: #3f37c9;
            --accent-color: #4895ef;
            --dark-color: #1a1a2e;
            --light-color: #f8f9fa;
            --success-color: #4cc9f0;
            --warning-color: #f72585;
            --error-color: #ef233c;
            --gray-color: #adb5bd;
            --text-dark: #212529;
            --text-light: #f8f9fa;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f5f7fa;
            color: var(--text-dark);
            line-height: 1.6;
        }
        
        .app-container {
            max-width: 900px;
            margin: 2rem auto;
            padding: 2rem;
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        .header {
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        }
        
        .header h1 {
            color: var(--primary-color);
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .header p {
            color: var(--gray-color);
            font-weight: 300;
        }
        
        .status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: var(--light-color);
            padding: 0.75rem 1.5rem;
            border-radius: 50px;
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
        }
        
        .status-indicator {
            display: flex;
            align-items: center;
        }
        
        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
            background-color: var(--success-color);
        }
        
        .status-dot.offline {
            background-color: var(--gray-color);
        }
        
        .status-dot.working {
            background-color: var(--accent-color);
            animation: pulse 1.5s infinite;
        }
        
        .status-dot.error {
            background-color: var(--error-color);
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .chat-container {
            height: 500px;
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            padding: 1.5rem;
            overflow-y: auto;
            margin-bottom: 1.5rem;
            background-color: #fff;
            display: flex;
            flex-direction: column;
        }
        
        .message {
            max-width: 75%;
            padding: 0.75rem 1rem;
            margin-bottom: 1rem;
            border-radius: 12px;
            line-height: 1.5;
            position: relative;
            word-wrap: break-word;
        }
        
        .user-message {
            align-self: flex-end;
            background-color: var(--primary-color);
            color: white;
            border-bottom-right-radius: 4px;
        }
        
        .assistant-message {
            align-self: flex-start;
            background-color: var(--light-color);
            color: var(--text-dark);
            border-bottom-left-radius: 4px;
        }
        
        .message-time {
            display: block;
            font-size: 0.7rem;
            opacity: 0.7;
            margin-top: 0.5rem;
            text-align: right;
        }
        
        .input-container {
            display: flex;
            gap: 0.75rem;
        }
        
        .input-field {
            flex: 1;
            padding: 0.75rem 1.25rem;
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 50px;
            font-size: 1rem;
            outline: none;
            transition: border 0.3s;
        }
        
        .input-field:focus {
            border-color: var(--primary-color);
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 50px;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .btn-primary {
            background-color: var(--primary-color);
            color: white;
        }
        
        .btn-primary:hover {
            background-color: var(--secondary-color);
        }
        
        .btn-voice {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background-color: var(--accent-color);
            color: white;
        }
        
        .btn-voice:hover {
            background-color: var(--secondary-color);
        }
        
        .btn-voice.listening {
            background-color: var(--warning-color);
            animation: pulse 1.5s infinite;
        }
        
        .loading-message {
            background-color: #f8f9fa;
            padding: 12px 16px;
            border-radius: 12px;
        }
        
        .loading-content {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .typing-dots {
            display: flex;
            gap: 4px;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--gray-color);
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(1) { animation-delay: 0s; }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-5px); }
        }
        
        .command-suggestions {
            display: flex;
            gap: 0.5rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }
        
        .suggestion-chip {
            padding: 0.5rem 1rem;
            background-color: var(--light-color);
            border-radius: 50px;
            font-size: 0.8rem;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .suggestion-chip:hover {
            background-color: var(--primary-color);
            color: white;
        }
        
        @media (max-width: 768px) {
            .app-container {
                margin: 1rem;
                padding: 1rem;
            }
            
            .chat-container {
                height: 400px;
            }
            
            .message {
                max-width: 85%;
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header">
            <h1><i class="fas fa-robot"></i> Professional Assistant</h1>
            <p>Your AI-powered voice and text assistant</p>
        </div>
        
        <div class="status-bar">
            <div class="status-indicator">
                <div class="status-dot" id="status-dot"></div>
                <span id="status-text">Ready</span>
            </div>
            <div id="current-time"></div>
        </div>
        
        <div class="chat-container" id="chat-window">
            <div class="message assistant-message">
                Hello! I'm your professional assistant. How can I help you today?
                <span class="message-time" id="welcome-time"></span>
            </div>
        </div>
        
        <div class="command-suggestions">
            <div class="suggestion-chip" onclick="insertSuggestion('What\'s the weather today?')">Weather</div>
            <div class="suggestion-chip" onclick="insertSuggestion('Tell me a joke')">Joke</div>
            <div class="suggestion-chip" onclick="insertSuggestion('What time is it?')">Time</div>
            <div class="suggestion-chip" onclick="insertSuggestion('Latest news')">News</div>
            <div class="suggestion-chip" onclick="insertSuggestion('Calculate 15 * 23')">Calculate</div>
        </div>
        
        <div class="input-container">
            <input type="text" class="input-field" id="user-input" placeholder="Type your message or command..." autocomplete="off">
            <button class="btn btn-primary" id="send-btn"><i class="fas fa-paper-plane"></i></button>
            <button class="btn btn-voice" id="voice-btn"><i class="fas fa-microphone"></i></button>
        </div>
    </div>

    <script>
        const chatWindow = document.getElementById('chat-window');
        const userInput = document.getElementById('user-input');
        const sendBtn = document.getElementById('send-btn');
        const voiceBtn = document.getElementById('voice-btn');
        const statusText = document.getElementById('status-text');
        const statusDot = document.getElementById('status-dot');
        const currentTimeElement = document.getElementById('current-time');
        const welcomeTime = document.getElementById('welcome-time');
        
        // Set initial time
        updateTime();
        welcomeTime.textContent = getCurrentTime();
        setInterval(updateTime, 60000);
        
        function updateTime() {
            currentTimeElement.textContent = getCurrentTime();
        }
        
        function getCurrentTime() {
            const now = new Date();
            return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }
        
        // Add welcome message
        addMessage('assistant', 'Hello! I\\'m your professional assistant. How can I help you today?');
        
        // Handle text input
        sendBtn.addEventListener('click', sendCommand);
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendCommand();
        });
        
        // Handle voice input
        voiceBtn.addEventListener('click', toggleVoiceRecognition);
        
        function insertSuggestion(text) {
            userInput.value = text;
            userInput.focus();
        }
        
        function addMessage(sender, text) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            messageDiv.innerHTML = text;
            
            const timeSpan = document.createElement('span');
            timeSpan.className = 'message-time';
            timeSpan.textContent = getCurrentTime();
            
            messageDiv.appendChild(timeSpan);
            chatWindow.appendChild(messageDiv);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
        
        function showLoadingState(type) {
            const typing = document.getElementById('typing-indicator');
            if (typing) typing.remove();
            
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message assistant-message loading-message';
            loadingDiv.id = 'typing-indicator';
            
            let loadingText = 'Assistant is thinking...';
            let estimatedTime = '';
            
            switch(type) {
                case 'weather':
                    estimatedTime = ' (usually takes 5-8 seconds)';
                    break;
                case 'wikipedia':
                    estimatedTime = ' (usually takes 3-5 seconds)';
                    break;
                case 'calculation':
                    loadingText = 'Calculating...';
                    break;
                case 'instant':
                    loadingText = 'Processing...';
                    break;
                default:
                    loadingText = 'Processing your request...';
            }
            
            loadingDiv.innerHTML = `
                <div class="loading-content">
                    <div class="typing-dots">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                    <span>${loadingText}${estimatedTime}</span>
                </div>
            `;
            
            chatWindow.appendChild(loadingDiv);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
        
        function hideTyping() {
            const typing = document.getElementById('typing-indicator');
            if (typing) typing.remove();
        }
        
        function determineLoadingType(command) {
            command = command.toLowerCase();
            if (command.includes('weather')) return 'weather';
            if (command.includes('wiki') || command.includes('wikipedia')) return 'wikipedia';
            if (command.includes('calculate') || command.match(/\d+[\+\-\*\/]\d+/)) return 'calculation';
            if (command.includes('time') || command.includes('date') || command.includes('joke')) return 'instant';
            return 'default';
        }
        
        function sendCommand() {
            const command = userInput.value.trim();
            if (!command) return;
            
            addMessage('user', command);
            userInput.value = '';
            
            const loadingType = determineLoadingType(command);
            showLoadingState(loadingType);
            statusText.textContent = 'Processing';
            statusDot.classList.add('working');
            
            // Start timeout timer
            const timeoutDuration = loadingType === 'weather' ? 10000 : 
                                  loadingType === 'wikipedia' ? 7000 : 
                                  loadingType === 'calculation' ? 5000 : 3000;
            
            const timeoutId = setTimeout(() => {
                hideTyping();
                statusText.textContent = 'Error';
                statusDot.classList.remove('working');
                statusDot.classList.add('error');
                addMessage('assistant', 'Sorry, this is taking longer than expected. Please try again or ask something else.');
            }, timeoutDuration);
            
            fetch('/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: command, type: 'text' })
            })
            .then(response => response.json())
            .then(data => {
                clearTimeout(timeoutId);
                hideTyping();
                statusText.textContent = 'Ready';
                statusDot.classList.remove('working', 'error');
                if (data.response) {
                    addMessage('assistant', data.response);
                }
            })
            .catch(error => {
                clearTimeout(timeoutId);
                hideTyping();
                statusText.textContent = 'Error';
                statusDot.classList.remove('working');
                statusDot.classList.add('error');
                addMessage('assistant', 'Sorry, there was an error processing your request. Please try again.');
                console.error('Error:', error);
            });
        }
        
        function toggleVoiceRecognition() {
            if (!('webkitSpeechRecognition' in window)) {
                addMessage('assistant', 'Your browser doesn\\'t support speech recognition. Please use Chrome or Edge.');
                return;
            }
            
            if (voiceBtn.classList.contains('listening')) {
                // Stop listening
                if (window.recognition) {
                    window.recognition.stop();
                }
                voiceBtn.classList.remove('listening');
                statusDot.classList.remove('working');
                statusText.textContent = 'Ready';
            } else {
                // Start listening
                voiceBtn.classList.add('listening');
                statusDot.classList.add('working');
                statusText.textContent = 'Listening...';
                
                const recognition = new webkitSpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'en-US';
                
                recognition.onstart = () => {
                    addMessage('assistant', 'Listening... Please speak now.');
                };
                
                recognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript;
                    userInput.value = transcript;
                    sendCommand();
                };
                
                recognition.onerror = (event) => {
                    addMessage('assistant', 'Error: ' + event.error);
                    voiceBtn.classList.remove('listening');
                    statusDot.classList.remove('working');
                    statusDot.classList.add('error');
                    statusText.textContent = 'Error';
                };
                
                recognition.onend = () => {
                    voiceBtn.classList.remove('listening');
                    statusDot.classList.remove('working');
                    statusText.textContent = 'Ready';
                };
                
                window.recognition = recognition;
                recognition.start();
            }
        }
    </script>
</body>
</html>
"""

# Cached functions for better performance
@lru_cache(maxsize=100)
def cached_wikipedia_search(query):
    return wikipedia.summary(query, sentences=2)

@lru_cache(maxsize=100)
def cached_weather_search(city):
    return get_weather(city)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def handle_command():
    data = request.json
    command = data.get('command', '').lower()
    command_type = data.get('type', 'text')
    
    start_time = time.time()
    
    try:
        response = process_command(command, command_type)
        processing_time = time.time() - start_time
        print(f"Command processed in {processing_time:.2f} seconds")
        
        # If processing took too long, add a note to the response
        if processing_time > 3:
            response += "\n\n(Sorry for the delay, some information takes longer to retrieve)"
            
    except Exception as e:
        response = f"Sorry, I encountered an error: {str(e)}"
    
    return jsonify({'response': response})

def process_command(command, command_type):
    """Process commands with timeout protection and priority handling"""
    if not command:
        return "I didn't receive any command."
    
    # Instant commands (very fast)
    if 'time' in command:
        return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}"
        
    elif 'date' in command:
        return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"
    
    # Fast commands (local processing)
    elif 'joke' in command:
        return pyjokes.get_joke()
    
    # Medium commands (might take a few seconds)
    elif 'wikipedia' in command or 'wiki' in command:
        query = command.replace("wikipedia", "").replace("wiki", "").strip()
        if not query:
            return "What would you like me to search on Wikipedia?"
        try:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(cached_wikipedia_search, query)
                result = future.result(timeout=5)  # 5 second timeout
            return f"According to Wikipedia: {result}"
        except TimeoutError:
            return "Wikipedia search is taking too long. Please try a different query."
        except wikipedia.exceptions.DisambiguationError as e:
            return f"There are multiple options. Could you be more specific? Options: {', '.join(e.options[:5])}..."
        except wikipedia.exceptions.PageError:
            return "Sorry, I couldn't find any information on that topic."
    
    # Weather command (external API)
    elif 'weather' in command:
        city = command.replace('weather', '').replace('in', '').replace('for', '').strip()
        if not city:
            return "Which city's weather would you like to know?"
        try:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(cached_weather_search, city)
                return future.result(timeout=8)  # 8 second timeout for weather
        except TimeoutError:
            return "Weather service is taking too long to respond."
        except Exception as e:
            return f"Sorry, I couldn't fetch the weather information. Error: {str(e)}"
    
    # News command
    elif 'news' in command or 'headlines' in command:
        try:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(get_news)
                return future.result(timeout=7)  # 7 second timeout
        except TimeoutError:
            return "News service is taking too long to respond."
        except Exception as e:
            return f"Sorry, I couldn't fetch the news right now. Error: {str(e)}"
    
    # Open websites
    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube..."
    
    elif 'open google' in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google..."
    
    # Calculations
    elif 'calculate' in command or 'what is' in command and ('+' in command or '-' in command or '*' in command or '/' in command):
        try:
            return calculate(command)
        except Exception as e:
            return f"Sorry, I couldn't perform that calculation. Error: {str(e)}"
    
    # Definitions
    elif 'what is' in command or 'define' in command:
        term = command.replace('what is', '').replace('define', '').strip()
        if term:
            try:
                with ThreadPoolExecutor() as executor:
                    future = executor.submit(get_definition, term)
                    return future.result(timeout=5)
            except TimeoutError:
                return "Definition lookup is taking too long."
            except Exception as e:
                return f"Sorry, I couldn't find a definition for that. Error: {str(e)}"
        return "What would you like me to define?"
    
    # System control
    elif 'shutdown' in command or 'restart' in command or 'sleep' in command:
        return system_control(command)
    
    # Reminders
    elif 'remind' in command or 'reminder' in command:
        try:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(set_reminder, command)
                return future.result(timeout=5)
        except TimeoutError:
            return "Setting the reminder took too long."
        except Exception as e:
            return f"Sorry, I couldn't set that reminder. Error: {str(e)}"
    
    # Greetings
    elif any(word in command for word in ['hello', 'hi', 'hey']):
        return wish_user()
    
    # Goodbye
    elif any(word in command for word in ['exit', 'bye', 'goodbye']):
        return "Goodbye! Have a great day!"
    
    # Web search
    else:
        try:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(search_web, command)
                return future.result(timeout=7)
        except TimeoutError:
            return "Web search is taking too long."
        except Exception as e:
            return f"I'm not sure how to handle that. You can try asking me to search the web for: {command}"

def open_browser():
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Save the HTML template with UTF-8 encoding
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(HTML_TEMPLATE)
    
    # Open browser after 1 second
    threading.Timer(1, open_browser).start()
    
    # Run the Flask app
    app.run(debug=True)
