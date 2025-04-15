import asyncio

from redis import from_url
from redis.asyncio import from_url as afrom_url
from rq import Queue
from rq.job import Job

from ..general_utils import get_required_env

BROKER_URI = get_required_env("BROKER_URI")
queue = Queue(connection=from_url(BROKER_URI))
aredis = afrom_url(BROKER_URI, decode_responses=True)


async def wait_and_receive_messages(job: Job):
    sub = aredis.pubsub(ignore_subscribe_messages=True)
    await sub.subscribe(f"task-messages-{job.id}")
    while not job.is_finished:  # Todo check that still applies when canceled of failed
        await asyncio.sleep(0.5)
        while (message_raw := await sub.get_message()) is not None:
            yield message_raw["data"]
    # Collect remaining messages
    while (message_raw := await sub.get_message()) is not None:
        yield message_raw["data"]
