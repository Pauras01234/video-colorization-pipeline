from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
from pathlib import Path

import redis
from rq import Queue
from rq.job import Job

from src.jobs import process_video_job

app = FastAPI()

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

redis_conn = redis.Redis(host="localhost", port=6379)
queue = Queue("default", connection=redis_conn)


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    temp_id = file.filename.replace(" ", "_")

    input_path = UPLOAD_DIR / temp_id
    output_path = OUTPUT_DIR / f"{Path(temp_id).stem}_output.mp4"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    job = queue.enqueue(process_video_job, str(input_path), str(output_path))

    return {"job_id": job.id}


@app.get("/status/{job_id}")
def get_status(job_id: str):
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        return {"status": job.get_status()}
    except Exception:
        return {"status": "not_found"}


@app.get("/download/{job_id}")
def download_video(job_id: str):
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        if job.get_status() != "finished":
            return {"error": "file not ready"}

        output_path = job.args[1]
        file_path = Path(output_path)

        if file_path.exists():
            return FileResponse(file_path, media_type="video/mp4")

        return {"error": "file missing"}
    except Exception:
        return {"error": "job not found"}