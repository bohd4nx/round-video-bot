import ffmpeg

from .constants import CIRCLE_MASK_PATH, CROP_SIZE, CROP_X, CROP_Y, PLANE_PATH, VIDEO_OUTPUT_SIZE
from .enums import Overlay


def _crop_square(stream: ffmpeg.nodes.FilterableStream) -> ffmpeg.nodes.FilterableStream:
    return (
        stream.video.filter("crop", CROP_SIZE, CROP_SIZE, CROP_X, CROP_Y)
        .filter("scale", VIDEO_OUTPUT_SIZE, VIDEO_OUTPUT_SIZE, flags="lanczos")
        .filter("setsar", "1/1")
    )


def android_filters(src: ffmpeg.nodes.FilterableStream) -> ffmpeg.nodes.FilterableStream:
    plane = ffmpeg.input(str(PLANE_PATH), stream_loop=-1)
    circle_mask = ffmpeg.input(str(CIRCLE_MASK_PATH))

    base = _crop_square(src).split()

    # Background: tiny blur vignette
    background = (
        base[1]
        .filter("scale", 48, 48, flags="bilinear")
        .filter("eq", brightness=-0.25)
        .filter("gblur", sigma=3, steps=2)
        .filter("scale", VIDEO_OUTPUT_SIZE, VIDEO_OUTPUT_SIZE, flags="fast_bilinear")
    )

    foreground = ffmpeg.filter([base[0], circle_mask], "alphamerge")
    return background.overlay(plane, shortest=1).overlay(foreground)


def ios_filters(src: ffmpeg.nodes.FilterableStream) -> ffmpeg.nodes.FilterableStream:
    # Same circle mask as Android, but composited on white instead of blurred bg
    circle_mask = ffmpeg.input(str(CIRCLE_MASK_PATH))
    white_bg = ffmpeg.input(f"color=c=white:s={VIDEO_OUTPUT_SIZE}x{VIDEO_OUTPUT_SIZE}:r=60", f="lavfi")
    circle = ffmpeg.filter([_crop_square(src), circle_mask], "alphamerge")
    return white_bg.overlay(circle, shortest=1)


def build_filter_graph(src: ffmpeg.nodes.FilterableStream, overlay: Overlay) -> ffmpeg.nodes.FilterableStream:
    if overlay is Overlay.IOS:
        return ios_filters(src)
    return android_filters(src)
