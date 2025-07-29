import speech_recognition as sr
import keyboard
import json
import time
import simpleaudio as sa

settings = {}

def log(message):
    print(f"[{time.strftime("%H:%M:%S")}] {message}")
    
def clip():
    if settings["play_sound_experimental"]: sa.WaveObject.from_wave_file("./sfx/garmin.wav").play().wait_done()
    log(f"Pressing {settings["medal_keybind"]}")
    keyboard.send(settings["medal_keybind"])
    
def recognizer():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Program is now listening")
        while True:
            audio_text = r.listen(source)
            
            try:
                text_de = r.recognize_google(audio_text, language="de-DE")
                text_en = r.recognize_google(audio_text, language="en-US")
                words = f"{text_de} {text_en}".lower()

                if any(item in words for item in settings["pattern"]):
                    log("Keyword(s) detected, clipping")
                    clip()
            except:
                log("Failed to recognize voice")

if __name__ == "__main__":
    with open("settings.json", "r") as f:
        settings = json.load(f)
        f.close()

    print(settings)

    print(f"OkayGarmin v{settings["version"]}")
    print("By: cablesalty")
    print()

    # Start main recognizer
    try:
        recognizer()
    except Exception as e:
        log(f"Error: {e}")
    except KeyboardInterrupt:
        log("Exiting...")
        exit(0)