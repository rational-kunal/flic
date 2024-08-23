import logging
import AudioManager
from functools import cached_property
from enum import Enum
import tempfile
import requests
import os
from urllib.parse import urlparse


class SegmentType(Enum):
    TITLE = "TITLE"
    CAPTION = "CAPTION"


class SegmentModel:
    def __init__(self, text, segment_type: SegmentType, image_url_string=""):
        self.text = text
        self.segment_type = segment_type
        self.image_url_string = image_url_string

    @cached_property
    def audio_speech_file(self):
        return AudioManager.manager.pyttsx_to_speech_audiofile(self.text)

    # TODO: Probably move this in its own manager
    @cached_property
    def image_file(self):
        # TODO: image_url_string validation
        if self.image_url_string is None or len(self.image_url_string) <= 0:
            return None

        response = requests.get(self.image_url_string)
        response.raise_for_status()  # Raise an error for bad status codes

        parsed_url = urlparse(self.image_url_string)
        filename = os.path.basename(parsed_url.path)
        name, extension = os.path.splitext(filename)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension)

        with open(temp_file.name, 'wb') as f:
            f.write(response.content)

        logging.info(f"Wrote image to {temp_file}")

        return temp_file.name
