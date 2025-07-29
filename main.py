import speech_recognition as sr
import simpleaudio as sa
import keyboard
import json

settings = {}

def clip():
    sa.WaveObject.from_wave_file("./sfx/garmin.wav").play()
    keyboard.send(settings["medal_keybind"])

def recognizer():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Program is now listening")
        while True:
            audio_text = r.listen(source)
            
            try:
                words = (str(r.recognize_google(audio_text, language="de-DE")).lower() + " " + str(r.recognize_google(audio_text, language="en-US")).lower())
                print(words)

                if any(item in words for item in settings["pattern"]):
                    clip()
                else:
                    print("Did not detect anything")
            except:
                print("Failed to recognize voice")

if __name__ == "__main__":
    # load application info from manifest
    with open("settings.json", "r") as f:
        settings = json.load(f)
        f.close()

    print(settings)

    print(f"OkayGarmin v{settings["version"]}")
    print("By: cablesalty")
    print()

    # Start main recognizer
    recognizer()