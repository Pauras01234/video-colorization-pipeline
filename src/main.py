from pathlib import Path
import subprocess

from src.extract_frames import extract_frames
from src.rebuild_video import rebuild_video
from src.colorize_frames import colorize_frames


def split_video_into_chunks(video_path: str, chunks_dir: str, chunk_duration: int = 10) -> None:
    Path(chunks_dir).mkdir(parents=True, exist_ok=True)
    output_pattern = str(Path(chunks_dir) / "chunk_%03d.mp4")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-c", "copy",
        "-map", "0",
        "-segment_time", str(chunk_duration),
        "-f", "segment",
        "-reset_timestamps", "1",
        output_pattern
    ]

    subprocess.run(cmd, check=True)


def merge_rebuilt_chunks(outputs_dir: str, final_output_path: str) -> None:
    outputs_path = Path(outputs_dir).resolve()
    rebuilt_files = sorted(outputs_path.glob("rebuilt_chunk_*.mp4"))

    list_file = outputs_path / "chunks_list.txt"

    with open(list_file, "w") as f:
        for rebuilt_file in rebuilt_files:
            f.write(f"file '{rebuilt_file.resolve().as_posix()}'\n")

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",
        final_output_path
    ]

    subprocess.run(cmd, check=True)


def process_video(video_path: str, final_output_path: str):
    chunks_dir = "outputs/chunks"
    outputs_dir = "outputs"
    fps = 25

    split_video_into_chunks(video_path, chunks_dir, chunk_duration=10)

    chunk_files = sorted(Path(chunks_dir).glob("chunk_*.mp4"))

    for chunk_file in chunk_files:
        chunk_name = chunk_file.stem
        frames_dir = f"outputs/{chunk_name}_frames"
        colorized_dir = f"outputs/{chunk_name}_colorized"
        output_path = f"outputs/rebuilt_{chunk_name}.mp4"

        print(f"Processing {chunk_file}.......")

        extract_frames(str(chunk_file), frames_dir)
        colorize_frames(frames_dir, colorized_dir)
        rebuild_video(colorized_dir, fps, output_path)

    merge_rebuilt_chunks(outputs_dir, final_output_path)