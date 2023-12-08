import os, sys, webbrowser, requests, subprocess, pyttsx3, voice
import voice

engine = pyttsx3.init()
engine.setProperty('rate', 180) 

def speaker(text):
    engine.say(text)
    engine.runAndWait()


def news():
    webbrowser.open('https://gorod48.ru/', new=2)


def browser():
    webbrowser.open('https://www.youtube.com', new=2)

def game():
    subprocess.Popen('D:/Notepad++/notepad++.exe')

def offpc():
    os.system('shutdown -s')

def weather():
    try:
        params = {'q': 'London', 'units': 'metric', 'lang': 'ru', 'appid': 'api_key'}
        response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params)
        if not response:
            raise
        w = response.json()
        voice.speaker(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")
    except:
        voice.speaker('Произошла ошибка при попытке запроса к ресурсу API, проверь код')



def offBot():
    sys.exit()

def passive():
    pass