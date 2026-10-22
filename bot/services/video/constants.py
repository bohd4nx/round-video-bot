from pathlib import Path

# Telegram video_note limits
SEGMENT_DURATION = 60.0  # seconds
VIDEO_OUTPUT_SIZE = 640  # px

# Overlay assets
FILES_DIR = Path(__file__).resolve().parents[3] / "files"
PLANE_PATH = FILES_DIR / "plane.apng"
CIRCLE_MASK_PATH = FILES_DIR / "overlay.png"

# Centered square crop
CROP_SIZE = "min(in_w,in_h)"
CROP_X = "(in_w-min(in_w,in_h))/2"
CROP_Y = "(in_h-min(in_w,in_h))/2"

# ffmpeg output options
VIDEO_OPTIONS = {
    "vcodec": "libx264",
    "preset": "veryfast",
    "crf": 23,
    "pix_fmt": "yuv420p",
    "movflags": "+faststart",
    "fpsmax": 60,
    "threads": 0,
}
AUDIO_OPTIONS = {
    "acodec": "aac",
    "audio_bitrate": "128k",
}
