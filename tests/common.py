"""Common functions for tests."""

import time
import pytest

TIMEOUT = 60.0
INTERVAL = 0.5


def wait_for_predicate(predicate, description, timeout=TIMEOUT, interval=INTERVAL):
    """
    Wait for predicate to be true.

    :param predicate: callable to test
    :param description: description to use if test fails
    :param timeout: timeout in seconds
    :param interval: interval between tests of the predicate in seconds

    """
    start = time.time()
    while True:
        if predicate():
            break
        if time.time() >= start + timeout:
            pytest.fail(f"{description} not achieved after {timeout} seconds")
        time.sleep(interval)


def wait_for_state(device, state):
    """
    Wait for device state to have the expected value.

    :param device: device proxy
    :param state: the expected state

    """
    predicate = lambda: device.State().name == state
    description = f"Device state {state}"
    wait_for_predicate(predicate, description)
