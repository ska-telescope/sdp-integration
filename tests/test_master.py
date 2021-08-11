import time

import tango
from pytest_bdd import scenarios, given, when, then, parsers

DEVICE_NAME = "test_sdp/elt/master"

scenarios("features/master.feature")

# -----------
# Given steps
# -----------


@given("I connect to the SDP master", target_fixture="master_device")
def connect_to_master():
    """Connect to the master using a Tango DeviceProxy."""
    return tango.DeviceProxy(DEVICE_NAME)


@given("the state is <initial_state>")
def set_state(master_device, initial_state):
    """
    Set the device state.

    :param master_device: SDPMaster device
    :param initial_state: desired device state

    """
    # Set the device state if incorrect
    if master_device.State().name != initial_state:
        # Call command to put device into the desired state
        master_device.command_inout(initial_state)


# ----------
# When steps
# ----------


@when("I call <command>")
def call_command(master_device, command):
    """
    Call a command.

    :param master_device: SDPMaster device
    :param command: name of command to call

    """
    # Check command is present
    assert command in master_device.get_command_list()
    # Call the command
    master_device.command_inout(command)


# ----------
# Then steps
# ----------


@then("the state should be <final_state>")
def state_is(master_device, final_state):
    """
    Check the device state.

    :param master_device: SDPMaster device
    :param final_state: expected state value

    """
    assert master_device.State().name == final_state
