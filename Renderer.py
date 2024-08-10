from Segment import SegmentModel, SegmentType
from moviepy.editor import *
import logging

YOUTUBE_SHORT_RESOLUTION = (1080, 1920)
CAPTION_FONT_PADDING = 20
CAPTION_CLIP_HORIZONTAL_LENGTH = YOUTUBE_SHORT_RESOLUTION[0] - 2*CAPTION_FONT_PADDING
SEGMENT_COOL_OFF_DURATION = 0.5
FALLBACK_FONT_RAW = "Courier-Bold"
TITLE_FONT_RAW = "AvantGarde-Demi"
TITLE_FONT = TITLE_FONT_RAW if len(TextClip.search(TITLE_FONT_RAW, "font")) > 0 else FALLBACK_FONT_RAW
CAPTION_FONT_RAW = "PT-Mono-Bold"
CAPTION_FONT = CAPTION_FONT_RAW if len(TextClip.search(CAPTION_FONT_RAW, "font")) > 0 else FALLBACK_FONT_RAW


class RenderHelper:
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
            return 92

        if self.segment.segment_type is SegmentType.CAPTION:
            return 50

        raise AssertionError


class Renderer:

    def __init__(self, background_video_path):
        background_video = VideoFileClip(background_video_path).resize(YOUTUBE_SHORT_RESOLUTION)
        self.background_video = background_video

    def create_video(self, segments: list[SegmentModel]):
        assert len(segments) > 0

        clips = []

        for i, segment in enumerate(segments):
            render_helper = RenderHelper(segment)

            try:
                audio = AudioFileClip(segment.audio_speech_file)

                # TODO: Customize captions
                caption_clip = TextClip(segment.text,
                                        fontsize=render_helper.font_size(), font=render_helper.font_name(),
                                        color='white', bg_color='transparent',
                                        stroke_color="DarkGray", stroke_width=0.3,
                                        size=(CAPTION_CLIP_HORIZONTAL_LENGTH, None), method='caption')
                caption_clip = caption_clip.set_duration(audio.duration + SEGMENT_COOL_OFF_DURATION)

                video_clip = caption_clip.set_audio(audio)

                clips.append(video_clip)

            except Exception as e:
                logging.error(f"Error processing file {segment}: {e}")

        concatenate_video_clips = concatenate_videoclips(clips, method="chain")
        background_video = self.background_video.subclip(0, concatenate_video_clips.duration)
        final_clip = CompositeVideoClip([background_video,
                                         concatenate_video_clips.set_position(("center", "center"))])

        final_clip.write_videofile("output_video.mp4", fps=24, codec='libx264', audio_codec='aac')
        logging.info("Video saved as output_video.mp4")


# For testing
if __name__ == "__main__":
    renderer = Renderer(background_video_path="./Assets/BlurMinecraftBG.mp4")
    dummy_segments = [SegmentModel(text="Hello World", segment_type=SegmentType.TITLE, image_url_string=""),
                      SegmentModel(text="Oo this is super cool", segment_type=SegmentType.CAPTION, image_url_string="")]
    renderer.create_video(dummy_segments)
