import logging
import math
from pathlib import Path

import ffmpeg

from .constants import AUDIO_OPTIONS, SEGMENT_DURATION, VIDEO_OPTIONS
from .enums import Overlay
from .filters import build_filter_graph
from .schemas import MediaInfo, Segment

logger = logging.getLogger(__name__)


def probe(path: Path) -> MediaInfo:
    info = ffmpeg.probe(str(path))
    return MediaInfo(
        duration=float(info["format"]["duration"]),
        has_audio=any(s["codec_type"] == "audio" for s in info["streams"]),
    )


def split_segments(total: float) -> list[Segment]:
    """Split a video of `total` seconds into video_note-sized segments."""
    return [
        Segment(index=i, start=i * SEGMENT_DURATION, duration=min(SEGMENT_DURATION, total - i * SEGMENT_DURATION))
        for i in range(math.ceil(total / SEGMENT_DURATION))
    ]


def encode_segment(
    in_path: Path,
    out_path: Path,
    segment: Segment,
    overlay: Overlay,
    has_audio: bool,
) -> int:
    """Encode one round segment. Blocking — run in a thread. Returns the output duration in seconds."""
    src = ffmpeg.input(str(in_path), ss=segment.start, t=segment.duration, hwaccel="auto")
    video = build_filter_graph(src, overlay).filter("format", "yuv420p")

    if has_audio:
        streams, opts = [video, src.audio], {**VIDEO_OPTIONS, **AUDIO_OPTIONS}
    else:
        streams, opts = [video], VIDEO_OPTIONS

    try:
        ffmpeg.output(*streams, str(out_path), **opts).overwrite_output().run(quiet=True)
    except ffmpeg.Error as e:
        logger.error("Error encoding segment: %s", e.stderr.decode() if e.stderr else "unknown error")
        raise

    return int(probe(out_path).duration)
