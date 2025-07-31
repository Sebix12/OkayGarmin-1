import speech_recognition as sr
import keyboard
import json
import time
import pygame
import os

settings = {}

def log(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}")

def clip():
    if settings.get("play_sound_experimental", True):
        try:
            sound_path = os.path.abspath("./sfx/garmin.wav")
            log(f"Playing sound from {sound_path}")
            sound = pygame.mixer.Sound(sound_path)
            sound.play()
            while pygame.mixer.get_busy():
                time.sleep(0.1)
        except Exception as e:
            log(f"Audio playback error: {e}")
    log(f"Pressing {settings.get('medal_keybind', 'F8')}")
    keyboard.send(settings.get("medal_keybind", "F8"))

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

                if any(item.lower() in words for item in settings.get("pattern", [])):
                    log("Keyword(s) detected, clipping")
                    clip()
            except Exception as e:
                log(f"Failed to recognize voice: {e}")

if __name__ == "__main__":
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
    except Exception as e:
        log(f"Failed to initialize pygame mixer: {e}")
        exit(1)

    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
    except Exception as e:
        log(f"Failed to load settings.json: {e}")
        exit(1)

    print(settings)
    print(f"OkayGarmin v{settings.get('version', 'unknown')}")
    print("By: cablesalty")
    print()

    try:
        recognizer()
    except KeyboardInterrupt:
        log("Exiting...")
        exit(0)
    except Exception as e:
        log(f"Error: {e}")
