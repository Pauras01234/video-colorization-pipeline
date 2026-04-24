import redis
from rq import Queue, SimpleWorker

redis_conn = redis.Redis(host="localhost", port=6379)

if __name__ == "__main__":
    queue = Queue("default", connection=redis_conn)
    worker = SimpleWorker([queue], connection=redis_conn)
    worker.work()