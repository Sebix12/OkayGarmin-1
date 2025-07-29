import speech_recognition as sr
import keyboard
import json

manifest = {}

def clip():
    keyboard.send(manifest["medal_keybind"])

def recognizer():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        while True:
            print("Running")
            audio_text = r.listen(source)
            
            try:
                words = (str(r.recognize_google(audio_text, language="de-DE")).lower() + " " + str(r.recognize_google(audio_text, language="en-US")).lower())
                print(words)

                if any(item in words for item in manifest["pattern"]):
                    clip()
                else:
                    print("Did not detect anything")
                    break
            except:
                print("Failed to recognize voice")

if __name__ == "__main__":
    # load application info from manifest
    with open("manifest.json", "r") as f:
        manifest = json.load(f)
        f.close()

    print(manifest)

    print(f"OkayGarmin v{manifest["version"]}")
    print("By: cablesalty")
    print()

    # Start main recognizer
    recognizer()