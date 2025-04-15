from redis import from_url
from rq import get_current_job

from ..general_utils import get_required_env


redis = from_url(
    get_required_env("REDIS_URL"), decode_responses=True
)  # ENV value that worker assumes


def get_send_message_function():
    job = get_current_job()
    if job is None:
        return print

    channel = f"task-messages-{job.id}"

    def send_message(message: str):
        redis.publish(channel, message)

    return send_message
