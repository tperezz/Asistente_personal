import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'es_ES')

class Asistente():
    def __init__(self):
        self.engine = pyttsx3.init()
        self.running = True
        self.callado = False
        self.saludar()
        
        
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def saludar(self):
        self.speak('Hola Tomás, soy Jarvis. ¿Cómo estás? ¿Necesitas algo?')
        self.escuchar()
    
    def despedir(self):
        self.speak('Adiós')

    def escuchar(self):
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
            if 'jarvis' in comando:
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
            elif 'Buscar' in comando or 'Google' in comando or 'buscar' in comando:
                self.speak('Qué te gustaría buscar?')
                self.buscar_en_google()
            elif 'fecha' in comando:
                fecha = hoy.strftime("%d de %B") 
                dia = hoy.strftime("%A")
                self.speak(f'Hoy es {dia} {fecha}')
            elif 'hora' in comando:
                hora = hoy.strftime("%H y %M")
                self.speak(f'Son las {hora}')
            elif 'no gracias' in comando or 'silencio' in comando:
                self.callado = True
            elif 'stop' in comando or 'adiós' in comando:
                self.running = False
            else:
                self.speak('Perdon, no entendí el comando')
    
    def silencio(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Modo silencio... (presiona Ctrl+C para salir)")
            audio = recognizer.listen(source, timeout = 300)
        try:
            texto = recognizer.recognize_google(audio, language='es-ES')
            print("Se reconoció:", texto)
            if 'jarvis' in texto or 'escuchame' in texto:
                self.callado = False
                self.speak('Hola de vuelta Tomás. ¿Qué necesitas?')
            elif 'stop' in texto or 'adiós' in texto:
                self.running = False
                return
        except sr.UnknownValueError:
            print("Silencio mantenido...")
        except sr.RequestError:
            self.speak("Lo siento, ha ocurrido un error en la conexión.")

    def transcribir(self):
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
                self.escuchar()
                    
    def abrir_mail(self):
        url_mail = 'https://mail.google.com/mail/u/0/#inbox'
        webbrowser.open(url_mail)
        self.speak('Abriendo los mails...')
    
    def buscar_en_google(self):
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
                

hoy = datetime.now()
jarvis = Asistente()
while jarvis.running:
    if not jarvis.callado:
        jarvis.escuchar()
    while jarvis.callado:
        jarvis.silencio()
        if not jarvis.running:
            break
    if not jarvis.running:
            break
jarvis.despedir()