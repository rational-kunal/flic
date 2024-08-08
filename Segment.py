import AudioManager
from functools import cached_property


class SegmentModel:
    def __init__(self, caption, image_url_string):
        self.caption = caption
        self.image_url_string = image_url_string

    @cached_property
    def audio_speech_file(self):
        return AudioManager.manager.to_speech_audiofile(self.caption)
