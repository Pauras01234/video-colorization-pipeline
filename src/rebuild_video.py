import subprocess


def rebuild_video(frames_dir: str, fps: int, output_path: str) -> None:

    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", str(fps),
        "-i", f"{frames_dir}/frame_%06d.png",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        output_path
    ] 



    subprocess.run(cmd, check=True)