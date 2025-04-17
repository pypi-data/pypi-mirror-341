import hashlib
import json
import os
import time
import inspect
import functools
import traceback
import requests

from typing import Optional
from pydantic import BaseModel

from cdp.cdp_client import CdpClient
from cdp.evm_client import EvmClient
from cdp.solana_client import SolanaClient


class ErrorEventData(BaseModel):
    """
    The data in an error event
    """

    method: (
        str  # The API method where the error occurred, e.g. createAccount, getAccount
    )
    message: str  # The error message
    name: str  # The name of the event. This should match the name in AEC
    stack: Optional[str] = None  # The error stack trace


EventData = ErrorEventData


async def send_event(event: EventData) -> None:
    """
    Sends an analytics event to the default endpoint

    Args:
        event: The event data containing event-specific fields

    Returns:
        None - resolves when the event is sent
    """
    timestamp = int(time.time() * 1000)

    enhanced_event = {
        "event_type": event.name,
        "platform": "server",
        "event_properties": {
            "platform": "server",
            "project_name": "cdp-sdk",
            "time_start": timestamp,
            "cdp_sdk_language": "python",
            **event.model_dump(),
        },
    }

    events = [enhanced_event]
    stringified_event_data = json.dumps(events)
    upload_time = str(timestamp)

    checksum = hashlib.md5(
        (stringified_event_data + upload_time).encode("utf-8")
    ).hexdigest()

    analytics_service_data = {"e": stringified_event_data, "checksum": checksum}

    api_endpoint = "https://cca-lite.coinbase.com"
    event_path = "/amp"
    event_endpoint = f"{api_endpoint}{event_path}"

    response = requests.post(
        event_endpoint,
        headers={"Content-Type": "application/json"},
        json=analytics_service_data,
    )
    response.raise_for_status()


def wrap_with_error_tracking(func):
    """
    Decorator that wraps a method with error tracking.

    Args:
        func: The function to wrap.

    Returns:
        The wrapped function.
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as error:
            event_data = ErrorEventData(
                method=func.__name__,
                message=str(error),
                stack=traceback.format_exc(),
                name="error",
            )

            if os.getenv("DISABLE_CDP_ERROR_REPORTING") != "true":
                try:
                    await send_event(event_data)
                except Exception:
                    # ignore error
                    pass

            raise

    return wrapper


def wrap_class_with_error_tracking(cls):
    """
    Wraps all methods of a class with error tracking.

    Args:
        cls: The class to wrap.

    Returns:
        The class with wrapped methods.
    """
    for name, method in inspect.getmembers(cls, inspect.isfunction):
        if not name.startswith("__"):
            setattr(cls, name, wrap_with_error_tracking(method))
    return cls


wrap_class_with_error_tracking(CdpClient)
wrap_class_with_error_tracking(EvmClient)
wrap_class_with_error_tracking(SolanaClient)
