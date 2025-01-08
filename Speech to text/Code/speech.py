from importer import sr, gTTS, os

recognizer = sr.Recognizer()

def voice_to_text():
    """Perform speech recognition and return the recognized text."""
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening... Speak now.")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results from the service; {e}"
    except Exception as e:
        return f"An error occurred: {e}"
def text_to_speech(text, filename="output.mp3"):
    """Convert text to speech and play the audio."""
    tts = gTTS(text=text, lang='en')
    tts.save(filename)