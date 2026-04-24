from pathlib import Path
import subprocess


def extract_frames(video_path: str, output_dir: str) -> None:
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-i", video_path,
        f"{output_dir}/frame_%06d.png"
    ]

    subprocess.run(cmd, check=True)