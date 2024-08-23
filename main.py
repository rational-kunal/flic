import director
import argparse
from pathlib import Path
import logging

RANDOM_UNCYCLOPEDIA_URL = "https://en.uncyclopedia.co/wiki/Special:RandomRootpage/Main"

# TODO: Out directory + Out file name
# TODO: Random article support
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='flic: generate short video from the uncyclopedia url')
    parser.add_argument("-verbose", "--v", metavar="debug", type=bool,
                        action=argparse.BooleanOptionalAction,
                        required=False, default=False)
    parser.add_argument("-uncyclopedia_url", "--url", metavar="url", type=str,
                        help="Uncyclopedia url keep empty for random article",
                        required=False, default=RANDOM_UNCYCLOPEDIA_URL)
    parser.add_argument("-background_video_path", "--bg", metavar="bg", type=Path,
                        help="Path to background url keep empty for default background article",
                        required=False, default="./Assets/BlurMinecraftBG.mp4")
    parser.add_argument("-out-dir", "--out", type=Path,
                        help="Path to out directory",
                        required=False, default="./out")

    args = parser.parse_args()
    verbose = args.v
    uncyclopedia_url: str = args.url
    background_video_path: Path = args.bg
    out_directory: Path = args.out

    assert len(uncyclopedia_url) > 0
    assert background_video_path.exists()

    if verbose:
        logging.basicConfig(level=logging.INFO)

    if not out_directory.exists():
        out_directory.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created directory: {out_directory}")

    director.direct(uncyclopedia_url=uncyclopedia_url,
                    out_directory=out_directory,
                    background_video_path=background_video_path.absolute().as_posix())
