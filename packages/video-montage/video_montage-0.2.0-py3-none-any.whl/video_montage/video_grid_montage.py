import math
import pathlib
from typing import Literal, Optional

import moviepy.editor as mp
from tap import Tap

from video_montage.utils import create_video_clips, datetime_str, overlay_text_on_clip


class ArgumentParser(Tap):
    input_video_folder_path: pathlib.Path
    output_video_folder_path: pathlib.Path = pathlib.Path(".")
    output_video_filename: Optional[str] = None
    max_n_videos: Optional[int] = None
    montage_duration_seconds: Optional[float] = None
    fps: Optional[int] = None
    num_per_row: Optional[int] = None
    overlay_filename: bool = False
    fill_mode: Literal["freeze", "loop", "black"] = "freeze"

    @property
    def output_video_filepath(self) -> pathlib.Path:
        if self.output_video_filename is None:
            filename = f"{self.input_video_folder_path.name}_{datetime_str()}_video_grid_montage.mp4"
        else:
            filename = self.output_video_filename
        return self.output_video_folder_path / filename


def adjust_video_clip_duration(
    video_clip: mp.VideoClip, target_duration: float, fill_mode: str
) -> mp.VideoClip:
    """
    Adjusts a single video clip to have the specified target_duration.

    If the clip is longer than target_duration, it is trimmed.
    If it is shorter, the extra time is filled according to fill_mode:
      - 'freeze': last frame is held as a still image.
      - 'loop': clip is repeated until reaching target_duration.
      - 'black': a black clip is appended.
    """
    current_duration = video_clip.duration

    if current_duration > target_duration:
        # Clip is longer: trim it.
        return video_clip.subclip(0, target_duration)
    elif current_duration == target_duration:
        return video_clip
    else:
        extra_time = target_duration - current_duration

        if fill_mode == "freeze":
            # Get the last frame (a little before the very end to ensure availability).
            last_frame = video_clip.get_frame(
                max(current_duration - 1 / video_clip.fps, 0)
            )
            freeze_clip = (
                mp.ImageClip(last_frame)
                .set_duration(extra_time)
                .set_fps(video_clip.fps)
            )
            return mp.concatenate_videoclips([video_clip, freeze_clip])
        elif fill_mode == "loop":
            # Loop the clip repeatedly and then trim to exactly target_duration.
            loops_required = math.ceil(target_duration / current_duration)
            looped_clip = mp.concatenate_videoclips([video_clip] * loops_required)
            return looped_clip.subclip(0, target_duration)
        elif fill_mode == "black":
            # Create a black clip to append.
            black_clip = mp.ColorClip(
                size=video_clip.size,
                color=(0, 0, 0),
                duration=extra_time,
            ).set_fps(video_clip.fps)
            return mp.concatenate_videoclips([video_clip, black_clip])
        else:
            raise ValueError(f"Invalid fill_mode: {fill_mode}")


def main() -> None:
    args: ArgumentParser = ArgumentParser().parse_args()
    assert args.input_video_folder_path.exists(), (
        f"Input video folder path {args.input_video_folder_path} does not exist."
    )

    if not args.output_video_folder_path.exists():
        print(f"Creating output folder {args.output_video_folder_path}")
        args.output_video_folder_path.mkdir(parents=True)

    # Create video clips from the input folder (if max_n_videos is provided, it will limit the number).
    video_clips = create_video_clips(
        args.input_video_folder_path, max_n_videos=args.max_n_videos
    )
    filenames = [
        pathlib.Path(video_clip.filename).name for video_clip in video_clips
    ]

    # Determine the target montage duration:
    # If user provided a duration, use it; otherwise, use the longest clip's duration.
    if args.montage_duration_seconds is not None:
        target_duration = args.montage_duration_seconds
    else:
        target_duration = max(video_clip.duration for video_clip in video_clips)

    # Adjust each clip to be exactly target_duration using the chosen fill_mode.
    video_clips = [
        adjust_video_clip_duration(
            video_clip=video_clip,
            target_duration=target_duration,
            fill_mode=args.fill_mode,
        )
        for video_clip in video_clips
    ]

    num_videos = len(video_clips)

    if args.overlay_filename:
        video_clips = [
            overlay_text_on_clip(
                clip=video_clip, text=filename
            )
            for video_clip, filename in zip(video_clips, filenames)
        ]

    # Determine grid layout for the montage.
    DEFAULT_NUM_PER_ROW = math.ceil(math.sqrt(num_videos))
    num_per_row = (
        args.num_per_row if args.num_per_row is not None else DEFAULT_NUM_PER_ROW
    )
    num_rows = math.ceil(num_videos / num_per_row)

    num_slots = num_per_row * num_rows
    num_empty_slots = num_slots - num_videos
    BLACK = (0, 0, 0)
    video_clips += [
        mp.ColorClip(
            size=video_clips[0].size,
            color=BLACK,
            duration=target_duration,
        )
        for _ in range(num_empty_slots)
    ]
    assert len(video_clips) == num_slots, f"{len(video_clips)} != {num_slots}"

    # Create the video grid from the array of clips.
    video_grid = mp.clips_array(
        [video_clips[i * num_per_row : (i + 1) * num_per_row] for i in range(num_rows)]
    )

    # Use the fps of the first clip if not specified.
    fps = args.fps if args.fps is not None else video_clips[0].fps
    video_grid.write_videofile(
        str(args.output_video_filepath),
        fps=fps,
    )


if __name__ == "__main__":
    main()
