from Segment import SegmentModel, SegmentType
from moviepy.editor import *
import logging
import random

YOUTUBE_SHORT_RESOLUTION = (1080, 1920)
MP4_FILE_EXTENSION = ".mp4"
CAPTION_FONT_PADDING = 20
CAPTION_CLIP_HORIZONTAL_LENGTH = YOUTUBE_SHORT_RESOLUTION[0] - 2*CAPTION_FONT_PADDING
SEGMENT_COOL_OFF_DURATION = 0.5
FALLBACK_FONT_RAW = "Courier-Bold"
TITLE_FONT_RAW = "Bookman-Demi"
TITLE_FONT = TITLE_FONT_RAW if len(TextClip.search(TITLE_FONT_RAW, "font")) > 0 else FALLBACK_FONT_RAW
CAPTION_FONT_RAW = "AvantGarde-Demi"
CAPTION_FONT = CAPTION_FONT_RAW if len(TextClip.search(CAPTION_FONT_RAW, "font")) > 0 else FALLBACK_FONT_RAW


class CaptionRenderHelper:
    def __init__(self, segment: SegmentModel):
        self.segment = segment

    def font_name(self):
        if self.segment.segment_type is SegmentType.TITLE:
            return TITLE_FONT
        if self.segment.segment_type is SegmentType.CAPTION:
            return CAPTION_FONT
        raise AssertionError

    def font_size(self):
        if self.segment.segment_type is SegmentType.TITLE:
            return 128
        if self.segment.segment_type is SegmentType.CAPTION:
            return 64
        raise AssertionError


class Renderer:

    def __init__(self, background_video_path):
        background_video = VideoFileClip(background_video_path).resize(YOUTUBE_SHORT_RESOLUTION)
        self.background_video = background_video

    def create_video(self, segments: list[SegmentModel], out_filename: str):
        assert len(segments) > 0

        clips = []

        for i, segment in enumerate(segments):
            try:
                segment_clip = self.__segment_clip(segment)
                clips.append(segment_clip)
            except Exception as e:
                logging.error(f"Error processing file {segment}: {e}")

        concatenate_video_clips = concatenate_videoclips(clips, method="compose")

        final_duration = concatenate_video_clips.duration
        random_start_t = random.uniform(0, self.background_video.duration - final_duration - 0.1)
        background_video = self.background_video.subclip(random_start_t, random_start_t + final_duration)

        final_clip = CompositeVideoClip([background_video,
                                         concatenate_video_clips.set_position(("center", "center"))])

        out_filename = out_filename + MP4_FILE_EXTENSION
        final_clip.write_videofile(out_filename, fps=24, codec='libx264', audio_codec='aac')
        logging.info(f"Video saved as {out_filename}")

    def __segment_clip(self, segment: SegmentModel):
        audio_clip = self.__audio_clip(segment)

        segment_duration_with_cool_off = audio_clip.duration + SEGMENT_COOL_OFF_DURATION
        caption_clip = self.__caption_clip(segment)
        caption_clip = caption_clip.set_duration(segment_duration_with_cool_off)

        segment_clip = caption_clip

        image_clip = self.__image_clip(segment)
        if image_clip:
            image_clip = image_clip.set_duration(segment_duration_with_cool_off)
            spacer_clip = ColorClip(size=(image_clip.w, 50), color=(0, 0, 0, 0))
            spacer_clip = spacer_clip.set_duration(segment_duration_with_cool_off)
            segment_clip = clips_array([[image_clip], [spacer_clip], [caption_clip]])

        segment_clip = segment_clip.set_audio(audio_clip)
        return segment_clip

    def __audio_clip(self, segment: SegmentModel):
        return AudioFileClip(segment.audio_speech_file)

    def __caption_clip(self, segment: SegmentModel):
        # TODO: Customize captions
        helper = CaptionRenderHelper(segment)
        return TextClip(segment.text,
                        fontsize=helper.font_size(), font=helper.font_name(),
                        color='white', bg_color='transparent',
                        stroke_color="Black", stroke_width=2,
                        size=(CAPTION_CLIP_HORIZONTAL_LENGTH, None), method='caption')

    def __image_clip(self, segment: SegmentModel):
        if not segment.image_file:
            return None

        return ImageClip(segment.image_file)


# For testing
if __name__ == "__main__":
    renderer = Renderer(background_video_path="Assets/BlurMinecraftBG.mp4")
    dummy_segments = [SegmentModel(text="Hello World", segment_type=SegmentType.TITLE,
                                   image_url_string="https://fastly.picsum.photos/id/237/536/354.jpg?hmac=i0yVXW1ORpyCZpQ-CknuyV-jbtU7_x9EBQVhvT5aRr0"),
                      SegmentModel(text="Oo this is super cool", segment_type=SegmentType.CAPTION, image_url_string="")]
    renderer.create_video(dummy_segments, out_filename="dummy")
