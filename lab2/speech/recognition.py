import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak now!")
    audio = recognizer.listen(source)

try:
    print(f'Google thinks you said: {recognizer.recognize_google(audio)}')
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
