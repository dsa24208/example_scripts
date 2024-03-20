
# main.py
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import os
import datetime
import smtplib


class PersonalAssistant:
    """A class that represents a personal assistant that can perform various tasks based on commands given by the user.

       Attributes:
           engine (pyttsx3.engine): A speech engine that is used to speak output.
           commands (dict): A dictionary that maps commands to functions that perform the associated task.

       """

    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.commands = {
            'wikipedia': self.search_wikipedia,
            'open youtube': self.open_youtube,
            'open google': self.open_google,
            'play music': self.play_music,
            'the time': self.tell_time,
            'open code': self.open_code,
            'email to someone': self.handle_send_email,
            'quit': self.quit
        }
        self.device_number = 1

    def speak(self, audio: str) -> None:
        """Speak the given audio using the text-to-speech engine.

        Args:
            audio (str): The audio to speak.

        """
        self.engine.say(audio)
        self.engine.runAndWait()

    def wish_me(self):
        """Greet the user based on the time of day."""
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")

    def take_command(self) -> str:
        """Use the speech recognition library to listen for commands from the user.

            Returns:
                The command that was spoken by the user.
        """
        try:
            r = sr.Recognizer()
            with sr.Microphone(device_index=self.device_number) as source:
                print("Listening...")
                r.pause_threshold = 1
                audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-US')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return ''
        return query.lower()

    def handle_send_email(self):
        """Handle the process of sending an email based on voice commands."""
        try:
            # Ask for the recipient's email
            self.speak("Whom should I send the email to?")
            recipient_email = self.take_command()
            if recipient_email is None or recipient_email.strip() == "":
                self.speak("I didn't catch the recipient's email. Please try again.")
                return

            to = recipient_email

            # Ask for the email content
            self.speak("What should I say?")
            content = self.take_command()
            if content is None or content.strip() == "":
                self.speak("I didn't catch that. Please try again.")
                return

            # Call the method to send the email
            self.send_email_command(to, content)
            self.speak("Email has been sent!")
        except Exception as e:
            print(e)
            self.speak("Sorry, I was unable to send that email.")

    def send_email_command(self, to: str, content: str) -> None:
        """Send an email using the provided SMTP server.

            Args:
                to (str): The email address of the recipient.
                content (str): The content of the email to be sent.

            Raises:
                Exception: If there was an error sending the email.

            Returns:
                None: This function does not return any additional values.
            """
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login('your_email@gmail.com', 'your_password')
            server.sendmail('your_email@gmail.com', to, content)
            server.close()
        except Exception as e:
            print(e)
            self.speak("Sorry, I was unable to send that email")

    def search_wikipedia(self, query: str) -> None:
        """Search Wikipedia for the provided query.

        Args:
            query (str): The query to search for.

        Raises:
            ValueError: If the query is empty.

        Returns:
            None: This function does not return any additional values.
        """
        query = query.replace("wikipedia", "")
        if not query:
            raise ValueError("You didn't provide a term to search for on Wikipedia.")
        try:
            results = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia")
            print(results)
            self.speak(results)
        except wikipedia.exceptions.PageError:
            self.speak("Sorry, I couldn't find a Wikipedia page for that query.")
        except wikipedia.exceptions.DisambiguationError as e:
            self.speak("There are multiple possible matches on Wikipedia. Here are some options:")
            for option in e.options:
                self.speak(option)

    def open_youtube(self):
        webbrowser.open("youtube.com")

    def open_google(self):
        webbrowser.open("google.com")

    def play_music(self):
        """Play a music file"""
        music_dir = 'your_music_directory'
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))

    def tell_time(self):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        self.speak(f"Sir, the time is {time}")

    def open_code(self):
        code_path = "path_to_your_code_editor"
        os.startfile(code_path)

    def quit(self):
        exit()

    def run(self):
        self.wish_me()
        while True:
            query = self.take_command()
            if query is None:
                continue

            # Handle commands directly without additional input
            if query in self.commands:
                action = self.commands[query]
                action()
                continue

            # Special handling for Wikipedia to ensure the query is properly formatted
            if 'wikipedia' in query:
                self.search_wikipedia(query)
                continue


if __name__ == "__main__":
    jarvis = PersonalAssistant()
    jarvis.run()
