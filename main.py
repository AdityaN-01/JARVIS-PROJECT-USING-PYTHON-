import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
# import os

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "enter your api key"

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
# def speak(text):
#      tts = gTTS(text)
#      tts.save('temp.mp3')
     
#      # Initialize Pygame mixer
#      pygame.mixer.init()

#      # Load the MP3 file
#      pygame.mixer.music.load('temp.mp3')

#      # Play the MP3 file
#      pygame.mixer.music.play()

#      # Keep the program running until the music stops playing
#      while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)
    
#         pygame.mixer.music.unload()
#         os.remove("temp.mp3") "It will for some time only after that it will asked for google_cloud subscription basically it is a paid version"

    
def aiProcess(command):
    client = OpenAI(api_key="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",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content
 
    
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]  
        webbrowser.open(link) 
        
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])
                
    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 
    
    
    
if __name__ == "__main__":
    speak("Initializing jarvis...")
    while True:
        # Listen for the wake word jarvis
        # obtain audio from the microphone
        r = sr.Recognizer()
        
            
        

        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                #Listen for command
                with sr.Microphone() as source:
                   print("Jarvis Active...")
                   audio = r.listen(source)
                   command = r.recognize_google(audio)
                   
                   processCommand(command)
                
        except Exception as e:
            print("Error; {0}".format(e))