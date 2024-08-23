import tempfile
import pyttsx3
import logging
from gtts import gTTS


class AudioManager:

    def __init__(self):
        self.engine = pyttsx3.init()

    def to_speech_audiofile(self, text):
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_filename = temp_file.name
            tts.save(temp_filename)
            # TODO: Close file, Delete file
            logging.info(f"Audio file for {text} saved at: {temp_filename}")

        return temp_filename

    def pyttsx_to_speech_audiofile(self, text):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_filename = temp_file.name
            self.engine.save_to_file(text, temp_filename)
            self.engine.runAndWait()
            # TODO: Close file, Delete file
            logging.info(f"Audio file for {text} saved at: {temp_filename}")

        return temp_filename


manager = AudioManager()
