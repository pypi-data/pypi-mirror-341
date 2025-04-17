"""
Integration with imbue-foreman (our central server).

"""
import asyncio
import time
from typing import Optional

import aiohttp
from loguru import logger

# TODO: Replace this with the persistent public instance URL once it exists.
DEFAULT_FOREMAN_URL = "http://localhost:8000"
MAX_WAITING_TIME_SECONDS = 60


class ForemanUnexpectedResponseError(Exception):
    pass


class SculptorInstanceNotReadyInTimeError(Exception):
    pass


async def get_or_create_sculptor_server(api_key: str, foreman_url: str) -> Optional[str]:
    """
    Negotiates a scultptor instance with foreman and waits until it's ready.

    (Can be an existing one or a new one, we don't know.)

    """
    headers = {"Authorization": f"Bearer {api_key}"}
    base_url = foreman_url.rstrip("/")
    async with aiohttp.ClientSession(headers=headers) as session:
        logger.info("Getting sculptor instance from foreman...")
        instance_url = await _get_or_create_sculptor_server(session, base_url)
        if instance_url is None:
            logger.info("Foreman didn't give us an instance URL.")
            return None
        logger.info("Waiting until the instance is ready...")
        await _wait_for_the_instance_to_be_ready(session, instance_url)
        logger.info("Instance is ready.")
        return instance_url


async def _get_or_create_sculptor_server(session: aiohttp.ClientSession, base_url: str) -> Optional[str]:
    try:
        response = await session.post(f"{base_url}/ensure-instance/")
        response.raise_for_status()
    except aiohttp.ClientConnectionError as e:
        # We're robust towards the foreman not being available at all and to auth errors.
        # We should raise for all other cases, though.
        # (Because it typically means we need to fix something.)
        logger.info(f"Failed to negotiate sculptor instance with foreman: {e}")
        return None
    except aiohttp.ClientResponseError as e:
        if e.status in (401, 403):
            logger.info(f"Failed to negotiate sculptor instance with foreman: {e}")
            return None
        raise
    try:
        instance_data = await response.json()
        logger.info(f"Got sculptor instance data from foreman: {instance_data}")
        instance_url = instance_data["url"]
    except aiohttp.ContentTypeError:
        logger.info(f"Failed to get URL from foreman: {response.text}")
        raise ForemanUnexpectedResponseError(f"Failed to get URL from foreman: {response.text}")
    return instance_url


async def _wait_for_the_instance_to_be_ready(session: aiohttp.ClientSession, instance_url: str) -> None:
    """
    Waits until the instance is ready.

    """
    started_at = time.monotonic()
    while True:
        try:
            response = await session.get(f"{instance_url}/api/ping/", timeout=5)
            response.raise_for_status()
            return
        except (aiohttp.ClientConnectionError, aiohttp.ClientResponseError):
            logger.info("Still waiting...")
            # This is a newly spawned instance and it takes it a bit more time to be ready.
            await asyncio.sleep(2)
            if time.monotonic() - started_at > MAX_WAITING_TIME_SECONDS:
                raise SculptorInstanceNotReadyInTimeError("Timed out waiting for the instance to be ready.")
            continue
