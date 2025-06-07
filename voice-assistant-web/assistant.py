import webbrowser
import datetime
import wikipedia
import pyjokes
import os
import time
import pyautogui
from bs4 import BeautifulSoup
import requests
import pyttsx3
import speech_recognition as sr
import pywhatkit
import re
import math

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech"""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen for user voice input and convert to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You: {query}")
        return query.lower()
    except Exception as e:
        print("Sorry, I didn't catch that. Could you repeat?")
        return ""

def wish_user():
    """Greet the user based on time of day"""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning! How can I help you today?")
    elif 12 <= hour < 18:
        speak("Good afternoon! How can I assist you?")
    else:
        speak("Good evening! What can I do for you?")

def get_weather(city):
    """Get weather information using web scraping"""
    try:
        url = f"https://www.google.com/search?q=weather+{city.replace(' ', '+')}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract weather information
        location = soup.find('div', attrs={'id': 'wob_loc'}).text
        time = soup.find('div', attrs={'id': 'wob_dts'}).text
        status = soup.find('span', attrs={'id': 'wob_dc'}).text
        temp = soup.find('span', attrs={'id': 'wob_tm'}).text
        
        return f"Current weather in {location}: {temp}°C, {status} as of {time}"
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return "Sorry, I couldn't fetch the weather information."

def get_news():
    """Get news headlines using web scraping"""
    try:
        url = "https://news.google.com/news/rss"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'xml')
        items = soup.find_all('item')[:5]
        
        news_items = []
        for i, item in enumerate(items):
            news_items.append(f"{i+1}. {item.title.text}")
        
        return "Here are some top news headlines:\n" + "\n".join(news_items)
    except Exception as e:
        print(f"Error fetching news: {e}")
        return "Sorry, I couldn't fetch the news right now."

def set_reminder():
    """Set a reminder for the user"""
    speak("What should I remind you about?")
    reminder = take_command()
    if not reminder:
        return "No reminder set."
    
    speak("In how many minutes?")
    minutes = take_command()
    try:
        minutes = float(minutes)
        seconds = minutes * 60
        time.sleep(seconds)
        speak(f"Reminder: {reminder}")
        return f"Reminder set: {reminder} in {minutes} minutes"
    except:
        return "Sorry, I couldn't set that reminder."

def search_web(query):
    """Search the web for the given query"""
    try:
        pywhatkit.search(query)
        return f"Here's what I found for {query} on the web"
    except Exception as e:
        print(f"Error searching web: {e}")
        return "Sorry, I couldn't perform the web search."

def calculate(query):
    """Perform basic calculations"""
    try:
        # Remove words and keep only math expression
        query = query.replace('calculate', '').replace('what is', '').strip()
        # Handle percentage calculations
        if '%' in query:
            parts = query.split('%')
            if 'of' in parts[1]:
                num = float(parts[0].strip())
                of_num = float(parts[1].replace('of', '').strip())
                result = (num / 100) * of_num
                return f"{num}% of {of_num} is {result}"
        
        # Handle regular calculations
        math_expr = ''.join([c for c in query if c in '0123456789+-*/.()'])
        if not math_expr:
            return "I couldn't find a valid calculation in your request."
        
        result = eval(math_expr)  # Note: eval can be dangerous with untrusted input
        return f"The answer is {result}"
    except Exception as e:
        print(f"Calculation error: {e}")
        return "Sorry, I couldn't perform that calculation."

def system_control(command):
    """Control system functions"""
    try:
        if 'screenshot' in command:
            pyautogui.screenshot('screenshot.png')
            return "Screenshot taken and saved"
        elif 'lock' in command:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "Locking your system"
        elif 'shutdown' in command:
            os.system("shutdown /s /t 1")
            return "Shutting down the system"
        elif 'restart' in command:
            os.system("shutdown /r /t 1")
            return "Restarting the system"
        else:
            return "I didn't understand that system command."
    except Exception as e:
        print(f"System control error: {e}")
        return "Sorry, I couldn't perform that system operation."

def get_definition(word):
    """Get dictionary definition using web scraping"""
    try:
        word = word.strip()
        url = f"https://www.dictionary.com/browse/{word}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        definition = soup.find('span', class_='one-click-content').text
        return f"The definition of {word} is: {definition}"
    except Exception as e:
        print(f"Error getting definition: {e}")
        return "Sorry, I couldn't find the definition."

def run_assistant():
    wish_user()
    while True:
        query = take_command()

        if not query:
            continue

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia:")
                speak(result)
            except:
                speak("Sorry, I couldn't find anything.")

        elif 'open youtube' in query:
            speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            speak("Opening Google...")
            webbrowser.open("https://www.google.com")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {strTime}")

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif 'weather' in query:
            speak("Which city's weather would you like to know?")
            city = take_command()
            weather_info = get_weather(city)
            speak(weather_info)

        elif 'news' in query:
            news_info = get_news()
            speak(news_info)

        elif 'remind' in query:
            reminder_info = set_reminder()
            speak(reminder_info)

        elif 'search' in query:
            search_query = query.replace('search', '').strip()
            search_result = search_web(search_query)
            speak(search_result)

        elif 'calculate' in query or 'what is' in query and ('+' in query or '-' in query or '*' in query or '/' in query):
            calculation_result = calculate(query)
            speak(calculation_result)

        elif 'meaning of' in query or 'definition of' in query:
            word = query.split('of')[-1].strip()
            definition = get_definition(word)
            speak(definition)

        elif 'screenshot' in query or 'lock' in query or 'shutdown' in query or 'restart' in query:
            control_result = system_control(query)
            speak(control_result)

        elif 'note' in query or 'remember' in query:
            speak("What should I note down?")
            note = take_command()
            with open("notes.txt", "a") as f:
                f.write(f"{datetime.datetime.now()}: {note}\n")
            speak("I've noted that down for you.")

        elif 'read notes' in query:
            try:
                with open("notes.txt", "r") as f:
                    notes = f.read()
                speak("Your notes:")
                speak(notes)
            except:
                speak("You don't have any notes yet.")

        elif 'exit' in query or 'bye' in query:
            speak("Goodbye! Have a nice day!")
            break

        else:
            try:
                result = wikipedia.summary(query, sentences=1)
                speak(result)
            except:
                speak("I'm not sure I understand. Could you rephrase that?")

if __name__ == "__main__":
    run_assistant()