import os
import json
import random
from datetime import date

import tango
from pytest_bdd import scenarios, given, when, then, parsers
from common import wait_for_predicate

DEVICE_NAME = "test_sdp/elt/subarray_1"

scenarios("features/subarray.feature")

# -----------
# Given steps
# -----------


@given("I connect to an SDP subarray", target_fixture="subarray_device")
def connect_to_subarray():
    """Connect to the subarray using a Tango DeviceProxy."""
    return tango.DeviceProxy(DEVICE_NAME)


@given(parsers.parse("the state is {state:S}"))
def set_state(subarray_device, state):
    """
    Set the device state to the desired value.

    This function sets the obsState to EMPTY.

    :param subarray_device: subarray device
    :param state: desired device state

    """
    set_state_and_obs_state(subarray_device, state, "EMPTY")


@given(parsers.parse("obsState is {obs_state:S}"))
def set_obs_state(subarray_device, obs_state):
    """
    Set the obsState to the desired value.

    This function sets the device state to ON.

    :param subarray_device: SDP subarray device
    :param obs_state: desired obsState

    """
    set_state_and_obs_state(subarray_device, "ON", obs_state)


# ----------
# When steps
# ----------


@when(parsers.parse("I call {command:S}"))
def call_command(subarray_device, command):
    """
    Call a device command.

    :param subarray_device: SDP subarray device
    :param command: name of command to call

    """
    # Check command is present
    assert command in subarray_device.get_command_list()
    # Get the command argument
    if command in ["AssignResources", "Configure", "Scan"]:
        argument = json.dumps(read_command_argument(command))
    else:
        argument = None
    # Call the command
    subarray_device.command_inout(command, cmd_param=argument)


# ----------
# Then steps
# ----------


@then(parsers.parse("the state should be {state:S}"))
def state_is(subarray_device, state):
    """
    Check the device state.

    :param subarray_device: SDP subarray device proxy
    :param final_state: expected state value

    """
    assert subarray_device.State().name == state


@then(parsers.parse("obsState should be {obs_state:S}"))
def obs_state_is(subarray_device, obs_state):
    """
    Check the obsState.

    :param subarray_device: SDP subarray device proxy
    :param obs_state: the expected obsState

    """
    assert subarray_device.obsState.name == obs_state


@then(parsers.parse("obsState should become {obs_state:S}"))
def obs_state_becomes(subarray_device, obs_state):
    """
    Check the obsState becomes the expected value.

    :param subarray_device: SDP subarray device proxy
    :param obs_state: the expected obsState

    """
    wait_for_obs_state(subarray_device, obs_state)


@then("receiveAddresses should have the expected value")
def receive_addresses_expected(subarray_device):
    """
    Check receiveAddresses has the expected value.

    :param subarray_device: subarray device

    """
    # Get the expected receive addresses from the data file
    receive_addresses_expected = read_receive_addresses()
    receive_addresses = json.loads(subarray_device.receiveAddresses)
    assert receive_addresses == receive_addresses_expected


@then("receiveAddresses should be empty")
def receive_addresses_empty(subarray_device):
    """
    Check receiveAddresses is empty.

    :param subarray_device: subarray device

    """
    receive_addresses = json.loads(subarray_device.receiveAddresses)
    assert receive_addresses == None


@then("scanType should have the expected value")
def scan_type_expected(subarray_device):
    """
    Check the scanType attribute has the expected value.

    :param subarray_device: subarray device

    """
    # Get the expected scan type from the Configure argument
    scan_type_expected = read_command_argument("Configure")["scan_type"]
    assert subarray_device.scanType == scan_type_expected


@then("scanType should be empty")
def scan_type_empty(subarray_device):
    """
    Check the scanType attribute is empty.

    :param subarray_device: subarray device

    """
    assert subarray_device.scanType == "null"


@then("scanID should have the expected value")
def scan_id_expected(subarray_device):
    """
    Check the scanID attribute has the expected value.

    :param subarray_device: subarray device

    """
    # Get the expected scan ID from the Scan argument
    scan_id_expected = read_command_argument("Scan")["scan_id"]
    assert subarray_device.scanID == scan_id_expected


@then("scanID should be 0")
def scan_id_zero(subarray_device):
    """
    Check the scanType attribute is empty.

    :param subarray_device: subarray device

    """
    assert subarray_device.scanID == 0


# -----------------------------------------------------------------------------
# Ancillary functions
# -----------------------------------------------------------------------------


def read_command_argument(name):
    """
    Read command argument from JSON file.

    :param name: name of command

    """
    config = read_json_data(f"command_{name}.json")

    if name == "AssignResources":
        # Insert new IDs into configuration
        config["eb_id"] = create_id("eb")
        for pb in config["processing_blocks"]:
            pb["pb_id"] = create_id("pb")

    return config


def create_id(prefix):
    """
    Create an ID with the given prefix.

    The ID will contain today's date and a random 5-digit number.

    :param prefix: the prefix

    """
    generator = "test"
    today = date.today().strftime("%Y%m%d")
    number = random.randint(0, 99999)
    return f"{prefix}-{generator}-{today}-{number:05d}"


def read_receive_addresses():
    """Read receive addresses from JSON file."""
    return read_json_data("receive_addresses.json")


def read_json_data(filename):
    """
    Read data from JSON file in the data directory.

    :param filename: name of the file to read

    """
    path = os.path.join(os.path.dirname(__file__), "data", filename)
    with open(path, "r") as file:
        data = json.load(file)
    return data


def set_state_and_obs_state(device, state, obs_state):
    """
    Set subarray device state and observing state.

    :param device: subarray device proxy
    :param state: the desired device state
    :param obs_state: the desired observing state

    """
    if device.State().name != state or device.obsState.name != obs_state:
        if device.State().name != "OFF":
            call_command(device, "Off")
        if state == "ON":
            call_command(device, "On")
            if obs_state in ["IDLE", "READY", "SCANNING"]:
                call_command(device, "AssignResources")
                wait_for_obs_state(device, "IDLE")
            if obs_state in ["READY", "SCANNING"]:
                call_command(device, "Configure")
            if obs_state == "SCANNING":
                call_command(device, "Scan")

    assert device.State().name == state
    assert device.obsState.name == obs_state


def wait_for_obs_state(device, obs_state):
    """
    Wait for obsState to have the expected value.

    :param device: device proxy
    :param obs_state: the expected value

    """
    predicate = lambda: device.obsState.name == obs_state
    description = f"obsState {obs_state}"
    wait_for_predicate(predicate, description)
