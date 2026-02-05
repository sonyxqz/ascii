import os
import time
import numpy as np
import imageio.v2 as imageio
from PIL import Image

ASCII_CHARS = " .:-=+*#%@"

def convert_frame_to_ascii(frame, width=80):
    img = Image.fromarray(frame).convert("L")

    original_width, original_height = img.size
    aspect_ratio = original_height / original_width

    height = int(width * aspect_ratio * 0.55)
    if height <= 0:
        height = 1

    img = img.resize((width, height))
    pixels = np.array(img) / 255.0

    ascii_frame = ""
    for row in pixels:
        for pixel in row:
            index = int(pixel * (len(ASCII_CHARS) - 1))
            ascii_frame += ASCII_CHARS[index]
        ascii_frame += "\n"

    return ascii_frame


def play_video_in_terminal(video_path, width=80):
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return

    reader = imageio.get_reader(video_path)
    meta = reader.get_meta_data()

    video_fps = meta.get("fps", 0)
    if video_fps <= 0:
        video_fps = 24

    try:
        start_time = time.perf_counter()
        frame_index = 0

        for frame in reader:
            ascii_art = convert_frame_to_ascii(frame, width)

            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_art)

            frame_index += 1
            expected_time = frame_index / video_fps
            elapsed = time.perf_counter() - start_time
            delay = expected_time - elapsed

            if delay > 0:
                time.sleep(delay)

    except KeyboardInterrupt:
        print("\nVideo playback interrupted.")

    finally:
        reader.close()


if __name__ == "__main__":
    video_path = input("Enter the path to the video file: ").strip()

    try:
        width = int(input("Enter terminal width (default 80): ") or "80")
    except ValueError:
        width = 80

    play_video_in_terminal(video_path, width)