from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path
import uuid
import os

import redis
from rq import Queue
from rq.job import Job
from dotenv import load_dotenv

from src.jobs import process_video_job
from src.storage import upload_file, create_presigned_url

load_dotenv()

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

redis_conn = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    password=os.getenv("REDIS_PASSWORD"),
    ssl=True,
)

queue = Queue("default", connection=redis_conn)


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    safe_filename = file.filename.replace(" ", "_")

    local_temp_path = UPLOAD_DIR / f"{job_id}_{safe_filename}"
    input_key = f"uploads/{job_id}_{safe_filename}"

    with open(local_temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    upload_file(str(local_temp_path), input_key)

    job = queue.enqueue(
    process_video_job,
    input_key,
    job_timeout=7200
)

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
            return JSONResponse({"error": "file not ready"}, status_code=400)

        output_key = job.result
        url = create_presigned_url(output_key)

        return {"download_url": url}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)