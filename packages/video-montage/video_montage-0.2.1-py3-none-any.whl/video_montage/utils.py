import pathlib
from datetime import datetime
from functools import lru_cache
from typing import List, Optional

import moviepy.editor as mp


@lru_cache()
def datetime_str() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def create_video_clips(
    input_video_folders_path: pathlib.Path, max_n_videos: Optional[int] = None
) -> List[mp.VideoFileClip]:
    VIDEO_EXTENSIONS = ["*.mp4", "*.webm", "*.avi", "*.mov", "*.mkv", "*.gif"]

    video_file_paths = sum(
        [
            sorted(
                list(input_video_folders_path.glob(video_extension)),
                key=lambda x: x.name,
            )
            for video_extension in VIDEO_EXTENSIONS
        ],
        [],
    )

    max_n_videos = max_n_videos if max_n_videos is not None else len(video_file_paths)
    selected_video_file_paths = video_file_paths[:max_n_videos]

    video_clips = [
        mp.VideoFileClip(str(video_file_path))
        for video_file_path in selected_video_file_paths
    ]
    return video_clips


def overlay_text_on_clip(
    clip: mp.VideoClip,
    text: str,
    vertical_position: str = "top",
    horizontal_position: str = "center",
    color: str = "black",
    bg_color: str = "white",
    width_buffer: float = 0.9,
) -> mp.VideoClip:
    LARGE_FONT_SIZE_FOR_BETTER_RESOLUTION = 100
    font_path = pathlib.Path(__file__).parent / "assets/fonts/DejaVuSans-Bold.ttf"
    assert font_path.exists(), f"Font file not found: {font_path}"
    text_clip = (
        mp.TextClip(
            text,
            color=color,
            bg_color=bg_color,
            fontsize=LARGE_FONT_SIZE_FOR_BETTER_RESOLUTION,
            font=str(
                pathlib.Path(__file__).parent / "assets/fonts/DejaVuSans-Bold.ttf"
            ),
        )
        .set_position((horizontal_position, vertical_position))
        .set_duration(clip.duration)
        .resize(width=int(clip.w * width_buffer))
    )
    return mp.CompositeVideoClip([clip, text_clip])
