import time
from typing import Callable, Optional, Union

from ..apiobject import Content, Ref
from ..exceptions import NotYetGeneratedException

MAX_RETRIES_FOR_GENERATED_JSON = 10
"""The maximum number of times to retry fetching generated JSON files."""

SLEEP_FOR_GENERATED_JSON = 1
"""The amount of time to sleep between attempts to fetch generated JSON files."""


def retry_not_yet_generated(
    method: Callable[[Union[Content, str], Optional[Ref]], dict], file_path: str, ref: Ref
) -> dict:
    """
    Request some generated json with retries if not yet available

    :param method: The request method that may raise
        NotYetGeneratedException, takes file_path and ref as arguments
    :param file_path: The path to the design document
    :param ref: The git ref to check.
    :returns: A dictionary containing the json results requested
    """
    attempts = 0
    while attempts < MAX_RETRIES_FOR_GENERATED_JSON:
        try:
            return method(file_path, ref)
        except NotYetGeneratedException:
            attempts += 1
            time.sleep(SLEEP_FOR_GENERATED_JSON)

    raise TimeoutError(
        f"Failed to fetch JSON for {file_path} after {MAX_RETRIES_FOR_GENERATED_JSON} attempts."
    )
