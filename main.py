import os.path
import director
import argparse

# TODO: Out directory + Out file name
# TODO: Random article support
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='flic: generate short video from the uncyclopedia url')
    parser.add_argument("uncyclopedia_url", metavar="url", type=str, help="Uncyclopedia url")
    parser.add_argument("background_video_path", metavar="bg", type=str, help="Path to background url")

    args = parser.parse_args()
    uncyclopedia_url: str = args.uncyclopedia_url
    background_video_path: str = args.uncyclopedia_url

    assert len(uncyclopedia_url) > 0
    assert os.path.isfile(background_video_path)

    director.direct(uncyclopedia_url=uncyclopedia_url, background_video_path=background_video_path)
