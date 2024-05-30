# Importo bibliotecas necesarias
import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
from datetime import datetime
import time
import locale
locale.setlocale(locale.LC_TIME, 'es_ES')


class Asistente():
    """Clase que representa a un asistente de voz personal"""
    def __init__(self):
        """Inicia una nueva instancia del asistente"""
        self.engine = pyttsx3.init()
        self.running = True
        self.callado = False
        self.saludar()
        
    def speak(self, text):
        """Funcion para que el asistente hable"""
        self.engine.say(text)
        self.engine.runAndWait()

    def saludar(self):
        """Funcion que saluda al iniciar el asistente"""
        self.speak('Hola Tomás, soy Luna. ¿Cómo estás? ¿Necesitas algo?')
        self.escuchar()
    
    def despedir(self):
        """Funcion para darse cuenta cuando el asistente deja de escuchar"""
        self.speak('Adiós')

    def escuchar(self):
        """Funcion que reconoce lo que el usuario dice por el microfono y lo transforma a texto en minusculas"""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Escuchando...")
            audio = recognizer.listen(source, timeout=30)
        try:
            texto = recognizer.recognize_google(audio, language='es-ES')
            texto = texto.lower()
            print("Se reconoció:", texto)
            self.procesar_comando(texto)
        except sr.UnknownValueError:
            self.speak("Lo siento, no entendí eso.")
        except sr.RequestError:
            self.speak("Lo siento, ha ocurrido un error en la conexión.")
            
    def procesar_comando(self, comando):
            """Funcion que contiene todos los comandos de texto que puede recibir el asistente y ejecuta sus respectivas funciones."""
            if 'luna' in comando:
                self.speak('Aquí estoy')
            elif'clima' in comando:
                self.speak('Aquí puedes integrar la función para obtener el clima.')
            elif 'noticias' in comando:
                self.speak('Aquí puedes integrar la función para obtener las noticias.')
            elif 'transcribir' in comando:
                self.speak('Qué te gustaría transcribir?')
                self.transcribir()
            elif 'mails' in comando:
                self.abrir_mail()
            elif 'buscar' in comando or 'google' in comando:
                self.speak('Qué te gustaría buscar?')
                self.buscar_en_google()
            elif 'fecha' in comando:
                hoy = datetime.now()
                fecha = hoy.strftime("%d de %B") 
                dia = hoy.strftime("%A")
                self.speak(f'Hoy es {dia} {fecha}')
            elif 'hora' in comando:
                hoy = datetime.now()
                hora = hoy.strftime("%H y %M")
                self.speak(f'Son las {hora}')
            elif 'timer' in comando or 'cronómetro' in comando:
                self.timer()
            elif 'no gracias' in comando or 'silencio' in comando:
                self.callado = True
            elif 'stop' in comando or 'adiós' in comando:
                self.running = False
            else:
                self.speak('Perdon, no entendí el comando')
    
    def silencio(self):
        """Funcion para que "duerma" el asistente excepto que se llame"""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Modo silencio... (presiona Ctrl+C para salir)")
            audio = recognizer.listen(source, timeout = 300)
        try:
            texto = recognizer.recognize_google(audio, language='es-ES')
            print("Se reconoció:", texto)
            if 'luna' in texto or 'escuchame' in texto:
                self.callado = False
                self.speak('Hola de vuelta Tomás. ¿Qué necesitas?')
            elif 'stop' in texto or 'adiós' in texto:
                self.running = False
                return
        except sr.UnknownValueError:
            print("Silencio mantenido...")
        except sr.RequestError:
            self.speak("Lo siento, ha ocurrido un error en la conexión.")
    
    def timer(self):
        """Funcion que funciona como temporizador"""
        self.speak('Temporizador. ¿En cuánto tiempo quieres que te avise?')
        recognizer = sr.Recognizer()
        
        try:
            with sr.Microphone() as source:
                print('Escuchando...')
                audio = recognizer.listen(source, timeout=30)
            
            tiempo = recognizer.recognize_google(audio, language='es-ES')
            palabras = tiempo.split()
            
            if 'horas' in palabras:
                segundos = int(palabras[0]) * 3600
                unidad = 'hora'
            elif 'minutos' in palabras:
                segundos = int(palabras[0]) * 60
                unidad = 'minuto'
            elif 'segundos' in palabras:
                segundos = int(palabras[0])
                unidad = 'segundo'
            else:
                self.speak('Lo siento, no entendí el tiempo especificado.')
                return

            self.speak(f'Temporizador iniciado por {tiempo}.')
            time.sleep(segundos)
            self.speak(f'¡El tiempo de {unidad} se ha terminado!')
            
        except sr.UnknownValueError:
            self.speak('Lo siento, no entendí eso.')
        except sr.RequestError:
            self.speak("Lo siento, ha ocurrido un error en la conexión.")

    def transcribir(self):
            """Funcion para transcribir lo que se le dicta"""
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Escuchando...")
                audio = recognizer.listen(source, timeout=30)
            try:
                texto = recognizer.recognize_google(audio, language='es-ES')
                print("Audio transcripto: ", texto)
            except sr.UnknownValueError:
                self.speak("Lo siento, no entendí eso.")
                self.transcribir()
            except sr.RequestError:
                self.speak("Lo siento, ha ocurrido un error en la conexión.")
                    
    def abrir_mail(self):
        """Funcion que abre el inbox de los mails"""
        url_mail = 'https://mail.google.com/mail/u/0/#inbox'
        webbrowser.open(url_mail)
        self.speak('Abriendo los mails...')
    
    def buscar_en_google(self):
        """Funcion para buscar en google la consulta que se dicte"""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Esperando la consulta de búsqueda...")
            audio = recognizer.listen(source, timeout=30)
        try:
            consulta = recognizer.recognize_google(audio, language='es-ES')
            print("Consulta de búsqueda:", consulta)
            url = f"https://www.google.com/search?q={consulta}"
            webbrowser.open(url)
            self.speak(f"Buscando {consulta} en Google.")
        except sr.UnknownValueError:
            self.speak("Lo siento, no entendí la consulta de búsqueda.")
        except sr.RequestError:
            self.speak("Lo siento, ha ocurrido un error en la conexión.")
                

luna = Asistente()
while luna.running:
    if not luna.callado:
        luna.escuchar()
    while luna.callado:
        luna.silencio()
        if not luna.running:
            break
    if not luna.running:
            break
luna.despedir()