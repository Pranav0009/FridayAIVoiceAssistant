import ctypes
import os
import subprocess
import webbrowser
import pywhatkit
import pyjokes
import pyttsx3
import requests
import speech_recognition as sr
import eel
import time
import pyautogui
from datetime import datetime
from PIL import Image
from Feature.emailsender import *
from Feature.gpt4_free import GPT
import random
from ecapture import ecapture as ec
import requests
from requests.exceptions import ConnectionError
import time
import sys
import keyboard


def speak(text):
    text = str(text.replace("*", ""))
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)

    except Exception as e:
        return ""

    return query.lower()

@eel.expose
def allCommands(message=1):

    from Feature.gpt4_free import GPT

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        # if 'open' in query:
        #     app_name = query.replace('open', '')
        #     speak('opening' + app_name)
        #     pyautogui.press('super')
        #     pyautogui.typewrite(app_name)
        #     pyautogui.sleep(0.7)
        #     pyautogui.press('enter')

        elif 'current time' in query:
            current_time = datetime.now().strftime("%I:%M %p")
            speak('Current time is ' + current_time)

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif 'take screenshot' in query:
            speak("Taking screenshot")
            pyautogui.screenshot("screenshot.png")
            image = Image.open('screenshot.png')
            image.show()

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if (contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()

                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'

                whatsApp(contact_no, query, flag, name)

        elif 'write an email' in query or 'compose an email' in query or 'send an email' in query:
            speak(
                'Sure sir, Can you provide me name of user to whom you want to send an email below :')
            receiver = "".join(takecommand().lower().replace(
                "at the rate", "@").split())
            print(receiver)  # Edited
            # receiver = takecommand() #WOriginal
            # input('Enter receivers email address: ')
            speak('what should be subject of the email')
            subject = takecommand()
            speak('what should be the content. Just provide me a prompt')
            email_prompt = takecommand()
            # content = gpt_instance.generate_response('write a mail for ' + email_prompt)
            content = GPT('write a mail for ' + email_prompt)
            send_email(receiver, subject, content)
            speak(f'email sent successfully to {receiver}')

        elif 'play' in query:
            song_name = query.replace('play', '')
            speak('Sure sir. Playing' + song_name + ' in youtube')
            pywhatkit.playonyt(song_name)

        elif 'switch tab' in query:
            pyautogui.hotkey('ctrl', 'tab')

        elif 'close tab' in query:
            pyautogui.hotkey('ctrl', 'w')

        elif 'close window' in query:
            pyautogui.hotkey('alt', 'F4')
            speak('Done, sir')

        elif "who made you" in query or "who created you" in query:
            speak("I have been created by ARPP.")

        elif "what is your name" in query:
            speak("Hello, I'm Friday, your voice assistant.")

        elif 'news' in query:
            news_url = "https://timesofindia.indiatimes.com/home/headlines"
            webbrowser.open_new_tab(news_url)
            speak('Here are some headlines from the Times of India. Happy reading!')
            time.sleep(6)

        elif "camera" in query or "take a photo" in query:
            ec.capture(0, "Friday Camera ", "img.jpg")

        elif 'lock window' in query:
            speak("locking the device")
            ctypes.windll.user32.LockWorkStation()

        elif 'shutdown system' in query:
            speak("Hold On a Sec ! Your system is on its way to shut down")
            subprocess.call('shutdown / p /f')

        elif "restart system" in query:
            subprocess.call(["shutdown", "/r"])

        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            subprocess.call("shutdown / h")

        elif "weather" in query:

            
            # to get API of Open weather
            api_key = "c0b785a2fda1f42aff64cd1b364b90ad"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            speak(" Location name ")
            city_name = takecommand()
            complete_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
            max_retries = 3
            retry_delay = 1
            for _ in range(max_retries):
                try:
                    response = requests.get(complete_url)
                    response.raise_for_status()
                    x = response.json()
                except ConnectionError:
                    print("Connection error occurred. Retrying...")
                    time.sleep(retry_delay)

            if x["cod"] != "4n04":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(f" Temperature is: {str(int(current_temperature-273.15))} ° Celsius, Atmospheric pressure is: {str(current_pressure)} hPa , \n Humidity is: {str(current_humidiy)} % , \n Description:  {str(weather_description)}.")
            else:
                speak(" City Not Found ")

        elif query == '':
            speak(random.choice(
                ["Sorry, I missed that.", "Sorry, I didn't catch that.", "Sorry, I didn't hear that."]))

        elif "joke" in query or "tell a joke" in query:
            speak(pyjokes.get_joke())

        else:
            # from engine.features import chatBot
            # chatBot(query)
            from Feature.gpt4_free import GPT
            res = GPT(query)
            speak(res)

    except Exception as err:
        print(f"Error: {err}")

    eel.ShowHood()
    
