import logging
import Uncyclopedia
from Renderer import Renderer
from Segment import SegmentModel
from nltk import tokenize


def direct(uncyclopedia_url: str, background_video_path: str):
    # Step 1: Fetch data
    result = Uncyclopedia.manager.fetch(uncyclopedia_url)
    logging.info(f"Data fetched from {uncyclopedia_url}")

    # Step 2: Split data
    summary_text_segments = tokenize.sent_tokenize(result.summary)
    segments = [SegmentModel(text_segment, result.image_url_string) for text_segment in summary_text_segments]
    logging.info(f"Created {len(segments)} segments")

    # Step 2: Render
    renderer = Renderer(background_video_path=background_video_path)
    renderer.create_video(segments)


# For debugging
if __name__ == "__main__":
    direct(uncyclopedia_url="https://en.uncyclopedia.co/wiki/Lead",
           background_video_path="Assets/BlurMinecraftBG.mp4")
