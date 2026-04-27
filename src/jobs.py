from pathlib import Path

from src.main import process_video
from src.storage import download_file, upload_file


def process_video_job(input_key: str) -> str:
    work_dir = Path("/tmp/video_colorizer")
    work_dir.mkdir(parents=True, exist_ok=True)

    input_path = work_dir / "input.mp4"
    output_path = work_dir / "output.mp4"

    download_file(input_key, str(input_path))

    process_video(str(input_path), str(output_path))

    output_key = input_key.replace("uploads/", "outputs/")

    upload_file(str(output_path), output_key)

    return output_key