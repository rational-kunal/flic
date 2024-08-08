from Segment import SegmentModel

from moviepy.editor import *
import logging

YOUTUBE_SHORT_RESOLUTION = (1080, 1920)
SEGMENT_COOL_OFF_DURATION = 0.5


class Renderer:

    def __init__(self, background_video_path):
        self.background_video = VideoFileClip(background_video_path).resize(YOUTUBE_SHORT_RESOLUTION)

    def create_video(self, segments: list[SegmentModel]):
        assert len(segments) > 0

        clips = []

        for i, segment in enumerate(segments):
            try:
                audio = AudioFileClip(segment.audio_speech_file)

                # TODO: Customize captions
                caption_clip = TextClip(segment.caption, fontsize=70, color='white', bg_color='transparent',
                                        size=(YOUTUBE_SHORT_RESOLUTION[0], None), method='caption')
                caption_clip = caption_clip.set_duration(audio.duration + SEGMENT_COOL_OFF_DURATION)

                video_clip = caption_clip.set_audio(audio)

                clips.append(video_clip)

            except Exception as e:
                logging.error(f"Error processing file {segment}: {e}")

        concatenate_video_clips = concatenate_videoclips(clips, method="compose")
        background_video = self.background_video.subclip(0, concatenate_video_clips.duration)
        final_clip = CompositeVideoClip([background_video,
                                         concatenate_video_clips.set_position(("center", "bottom"), relative=True)])

        final_clip.write_videofile("output_video.mp4", fps=24, codec='libx264', audio_codec='aac')
        logging.info("Video saved as output_video.mp4")


# For testing
if __name__ == "__main__":
    renderer = Renderer(background_video_path="Assets/BlurMinecraftBG.mp4")
    dummy_segments = [SegmentModel(caption="Hello World", image_url_string=""),
                      SegmentModel(caption=3*"Lorem ipsum dorem amet ", image_url_string="")]
    renderer.create_video(dummy_segments)