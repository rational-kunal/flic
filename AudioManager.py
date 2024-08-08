import tempfile
import pyttsx3
import logging


class AudioManager:

    def __init__(self):
        self.engine = pyttsx3.init()

    def to_speech_audiofile(self, text):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_filename = temp_file.name
            self.engine.save_to_file(text, temp_filename)
            self.engine.runAndWait()
            # TODO: Close file, Delete file
            logging.info(f"Audio file for {text} saved at: {temp_filename}")

        return temp_filename


manager = AudioManager()
