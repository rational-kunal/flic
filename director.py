import logging
import Uncyclopedia
from Renderer import Renderer
from Segment import SegmentModel, SegmentType
from nltk import tokenize
from pathlib import Path


def direct(uncyclopedia_url: str, out_directory: Path, background_video_path: str):
    # Step 1: Fetch data
    result = Uncyclopedia.manager.fetch(uncyclopedia_url)
    logging.info(f"Data fetched from {uncyclopedia_url}")

    # Step 2: Split data
    summary_text_segments = tokenize.sent_tokenize(result.summary)
    title_segment = SegmentModel(text=result.title, segment_type=SegmentType.TITLE,
                                 image_url_string=result.main_image_url_string)
    caption_segments = [SegmentModel(text=text_segment, segment_type=SegmentType.CAPTION) for text_segment in summary_text_segments]
    segments = [title_segment] + caption_segments
    logging.info(f"Created {len(segments)} segments")

    # Step 2: Render
    renderer = Renderer(background_video_path=background_video_path)
    renderer.create_video(segments, out_filename=out_directory.absolute().as_posix() + "/" + result.title)


# For debugging
if __name__ == "__main__":
    direct(uncyclopedia_url="https://en.uncyclopedia.co/wiki/Lead",
           background_video_path="Assets/BlurMinecraftBG.mp4")
