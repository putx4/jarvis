from os import error
import requests
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from random import choice
from utils import opening_text
from pprint import pprint
from functions.online_ops import (

    find_my_ip, get_latest_news, get_random_advice, get_random_joke,
    get_trending_movies, get_weather_report, play_on_youtube, search_on_google,
    search_on_wikipedia, send_email, send_whatsapp_message
)
from functions.os_ops import (
    open_calculator, open_camera, open_cmd, open_discord, open_notepad
)

USERNAME = config('USER')
BOTNAME = config('BOTNAME')

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Buenos días {USERNAME}")
    elif 12 <= hour < 16:
        speak(f"Buenas tardes {USERNAME}")
    elif 16 <= hour < 19:
        speak(f"Buenas noches {USERNAME}")
    speak(f"Yo soy {BOTNAME}. ¿Cómo puedo ayudarte?")

def take_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Escuchando....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Reconociendo...')
        query = r.recognize_google(audio, language='es-ES')
        return query.lower()
        query = ""
        speak(choice(opening_text))
    except sr.RequestError as e:
        speak(f"Error en la solicitud de reconocimiento de voz: {e}")
    except Exception as e:
        error_message = f"No pude entender. ¿Podrías decir eso de nuevo? {str(e)}"
        print(error_message)
        speak(error_message)
        query = ""

    return query.lower()

if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()

        speak(choice(opening_text))

        if 'abre el block de notas' in query:
            open_notepad()

        elif 'abre discord' in query:
            open_discord()


        if 'abre la caja de comando' in query or 'open cmd' in query:
            open_cmd()

        elif 'abre la camara' in query:
            open_camera()

        elif 'abre la calculadora' in query:
            open_calculator()

        if 'direccion ip' in query:
            ip_address = find_my_ip()
        if ip_address:
            speak(f'Su dirección IP es {ip_address}.')
            print(f'Su dirección IP es {ip_address}')

        if 'busca en wikipedia' in query:
            speak('¿Qué desea buscar en Wikipedia, señor?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"De acuerdo con Wikipedia, {results}")
            speak("Para su comodidad, mostraré en pantalla los resultados, señor.")
            print(results)

        if 'busca en youtube' in query:
            speak('¿Qué desea ver en YouTube, señor?')
            video = take_user_input().lower()
            play_on_youtube(video)

        if 'busca en google' in query:
            speak('¿Qué desea buscar en Google, señor?')
            search_query = take_user_input().lower()
            search_on_google(search_query)

        if "envia un whatsapp" in query:
            speak('¿A qué número envío el mensaje, señor?')
            number = input("Ingrese el número: ")
            speak("¿Cuál es el mensaje, señor?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("El mensaje ha sido enviado, señor.")

        if "envia un email" in query:
            speak("¿A qué dirección de correo la envío, señor? Por favor, ingrésela: ")
            receiver_address = input("Ingrese la dirección de correo electrónico: ")
            speak("¿Cuál es el asunto, señor?")
            subject = take_user_input().capitalize()
            speak("¿Cuál es el mensaje, señor?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("El correo ha sido enviado, señor.")
            else:
                speak("Algo ha salido mal mientras estaba enviando el correo.")

        if 'dime un chiste' in query:
            joke = get_random_joke()
            speak(f"Espero que le guste este chiste, señor: {joke}")
            speak("Aquí tiene su chiste, señor")
            pprint(joke)

        if "dame un consejo" in query:
            advice = get_random_advice()
            speak(f"Acá hay un consejo para usted, señor: {advice}")
            speak("Mostrando en pantalla, señor")
            pprint(advice)

        if "peliculas taquilleras" in query:
            trending_movies = get_trending_movies()
            speak(
            f"Algunas de las películas más taquilleras son:{','.join(trending_movies)}")
            speak("Para su conveniencia, las estoy imprimiendo en pantalla, señor.")
            pprint(trending_movies)

        if 'noticias' in query:
            news = get_latest_news()
            speak("Estoy leyendo los titulares de noticias más recientes, señor")
            speak(news)
            speak("Para su conveniencia, los estoy imprimiendo en pantalla, señor.")
            pprint(news)



        if 'cómo está el clima' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Obteniendo el informe del clima para su ciudad {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(
            f"La temperatura actual es {temperature}, pero se siente como {feels_like}"
            )