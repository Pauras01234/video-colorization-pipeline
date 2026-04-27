import os
import redis
from rq import Queue, SimpleWorker
from dotenv import load_dotenv

load_dotenv()

redis_conn = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    password=os.getenv("REDIS_PASSWORD"),
    ssl=True,
)

queue = Queue("default", connection=redis_conn)

if __name__ == "__main__":
    worker = SimpleWorker([queue], connection=redis_conn)
    worker.work()