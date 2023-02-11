import openai
import speech_recognition as sr
#import pyttsx3
import os
from gtts import gTTS
import playsound

# Set OpenAI API key
openai.api_key = os.environ.get("PRIVATE_API_KEY")

def speak(audioString):
    tts = gTTS(text=audioString, lang='en')
    filename = "abc.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


def chatbot(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message

def get_audio_input():
    r = sr.Recognizer()
    with sr.Microphone(device_index=14) as source:
        print("Speak:")
        audio = r.listen(source)

    try:
        #text = r.recognize_sphinx(audio)1G
        text = r.recognize_google(audio)
        print("You said: {}".format(text))
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

def play_audio_output(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    engine.say(text)
    engine.runAndWait()

conversation_history = []
print("Hi, I am Friday, your personal voice assistant. How can I help you today?"
speak("Hi, I am Friday, your personal voice assistant. How can I help you today?")

while True:
    user_input = get_audio_input()
    if user_input is None:
        print("Sorry, I didn't get that.")
        play_audio_output("Sorry, I didn't get that.")
        speak("Sorry, I didn't get that.")
        continue
    if "bye" in user_input.lower():
        print("Goodbye! Have a great day.")
        speak("Goodbye! Have a great day.")
        break
    conversation_history.append(user_input)
    prompt = "\n".join(conversation_history)
    response = chatbot(prompt)
    print("Friday: " + response)
    speak(response)
    conversation_history.append(response)
