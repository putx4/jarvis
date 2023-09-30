from sys import exception
import requests
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice
from functions.online_ops import get_random_joke, get_trending_movies
from functions.online_ops import get_weather_report, play_on_youtube, search_on_google
from functions.online_ops import search_on_wikipedia, send_email, send_whatsapp_message
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad
from functions.os_ops import open_discord
from random import choice
from utils import opening_text
from pprint import pprint


USERNAME = config('USER')
BOTNAME = config('BOTNAME')


engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()


# Greet the user
def greet_user():
    """Greets the user according to the time"""
    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Buenos dias {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Buenas tardes {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Buenas noches {USERNAME}")
    speak(f"Yo soy {BOTNAME}. ¿Cómo puedo ayudarte?")


# Takes Input from User
def take_user_input():
    """Recibe entrada del usuario, la reconoce utilizando el módulo de reconocimiento de
    voz y la convierte en texto"""
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Escuchando....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Reconociendo...')
        query = r.recognize_google(audio, language='es-ES')
        return query.lower()
    except sr.RequestError as e:
        print(f"Error en la solicitud de reconocimiento de voz:{e}")
        return ""
        if not ('exit' in query or 'stop' in query):
         
         speak(choice(opening_text))

        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("buenas noches, señor!")
            else:
                speak('Tenga un buen dia, señor')
    except exception: 
        print("Lo siento, no pude entender. ¿Podrías decir eso de nuevo?")
    finally:
        print("Fin del proceso")
    
        
if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()

        if 'open notepad' in query:
            open_notepad()

        elif 'open discord' in query:
            open_discord()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is{ip_address}.\n SE lo muestro en pantalla, señor')
            print(f'Your IP Address is{ip_address}')

        elif 'wikipedia' in query:
            speak('¿Qué quiere buscar en Wikipedia, señor?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"De acuerdo con wikipedia, {results}")
            speak("Para su comodidad, mostraré en pantalla los resultados, señor.")
            print(results)

        elif 'youtube' in query:
            speak('¿Que desea ver en YouTube, señor?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'search on google' in query:
            speak('¿Qué desea buscar en Google, señor?')
            query = take_user_input().lower()
            search_on_google(query)

        elif "send whatsapp message" in query:
            speak(
                '¿A qué número envio el mensaje señor?, digítelo en la consola:')
            number = input("Ingrese el número: ")
            speak("¿Cúal es el mensaje, señor?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("El mensaje ha sido enviado, señor.")

        elif "send an email" in query:
            speak("¿A qué dirección de correo la envío, señor? Por favor, ingreselo: ")
            receiver_address = input("Ingrese la dirección de correo electrónico: ")
            speak("¿Cuál es el asunto, señor?")
            subject = take_user_input().capitalize()
            speak("¿Cuál es el mensaje, señor?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("El correo ha sido enviado, señor.")
            else:
                speak("Algo ha salido mal mientras estaba enviando el correo.")

        elif 'joke' in query:
            speak(f"Espero que le guste este chiste, señor:{get_random_joke()}")
            joke = get_random_joke()
            speak(joke)
            speak("Aquí tiene su chiste, señor")
            pprint(joke)

        elif "advice" in query:
            speak(f"Acá hay un consejo para usted, señor:{get_random_advice()}")
            advice = get_random_advice()  # noqa: E999
            speak(advice)
            speak("Mostrando en pantalla, señor")
            pprint(advice)

        elif "trending movies" in query:
            speak(f"Some of the trending movies are: {get_trending_movies()}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(*get_trending_movies(), sep='\n')

        elif 'news' in query:
            speak("I'm reading out the latest news headlines, sir")
            speak(get_latest_news())
            speak("For your convenience, I am printing it on the screen sir.")
            print(*get_latest_news(), sep='\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(
            f"The current temperature is {temperature}, but it feels like {feels_like}"
            )