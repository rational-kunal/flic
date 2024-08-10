import os.path
import director
import argparse
from pathlib import Path

# TODO: Out directory + Out file name
# TODO: Random article support
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='flic: generate short video from the uncyclopedia url')
    parser.add_argument("uncyclopedia_url", metavar="url", type=str, help="Uncyclopedia url")
    parser.add_argument("background_video_path", metavar="bg", type=Path, help="Path to background url")

    args = parser.parse_args()
    uncyclopedia_url: str = args.uncyclopedia_url
    background_video_path: Path = args.background_video_path

    assert len(uncyclopedia_url) > 0
    assert background_video_path.exists()

    director.direct(uncyclopedia_url=uncyclopedia_url,
                    background_video_path=background_video_path.absolute().as_posix())
