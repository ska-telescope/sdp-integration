"""Common functions for tests."""

import time
import pytest


def wait_for_predicate(predicate, description, count=20, wait=0.5):
    """
    Wait for predicate to be true.

    :param predicate: callable to test
    :param description: description to use if test fails
    :param count: number of times to test condition
    :param wait: time to wait between attempts, in seconds

    """
    if not predicate():
        for _ in range(count):
            time.sleep(wait)
            if predicate():
                break
        else:
            pytest.fail(f"{description} not achieved after {count * wait} seconds")


def wait_for_state(device, state):
    """
    Wait for device state to have the expected value.

    :param device: device proxy
    :param state: the expected state

    """
    predicate = lambda: device.State().name == state
    description = f"Device state {state}"
    wait_for_predicate(predicate, description)
