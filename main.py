import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import openai


# Initialize text-to-speech engine

engine = pyttsx3.init()


# Function to speak text

def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to listen for user command

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Sorry, I didn't catch that. Can you please repeat?")
        return ""

    return query


# Function to greet

def greet():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good morning! I'm JARVIS")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon! I'm JARVIS")
    else:
        speak("Good evening! I'm JARVIS")

    speak("How can I assist you today?")


# Function to execute commands

def execute_command(command):
    if 'wikipedia' in command:
        speak("Searching Wikipedia...")
        query = command.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia:")
        print(results)
        speak(results)
    elif 'open YouTube'.lower() in command:
        webbrowser.open("https://www.youtube.com")
    elif 'open google'.lower() in command:
        webbrowser.open("https://www.google.com")
    elif 'what time is it'.lower() in command:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {time}")
    elif 'artificial intelligence'.lower() in command:
        ai(command)
    elif 'exit'.lower() in command:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I didn't understand that command.")


# Function to use OpenAI

def ai(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    text = f"Open AI response : {prompt} \n *****************\n\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
    )
    text += response["choices"][0]["text"]
    if not os.path.exists("OpenAI"):
        os.mkdir("OpenAI")
    with open(f"OpenAI/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)


# Main function

def main():
    greet()
    while True:
        command = listen().lower()
        if command != "":
            execute_command(command)

if __name__ == '__main__':
    main()
