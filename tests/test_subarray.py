import os
import logging
from time import sleep
import json

import pytest
import tango

from pytest_bdd import scenarios, given, when, then, parsers

from ska_sdp_lmc import (AdminMode, HealthState, ObsState)

DEVICE_NAME = 'test_sdp/elt/subarray_1'

logger = logging.getLogger(__name__)

scenarios("features/subarray.feature")

# -----------
# Given steps
# -----------

@given("I have an SDPSubarray device", target_fixture='subarray_device')
def connect_to_subarray_device():
   device = tango.DeviceProxy(DEVICE_NAME)
   return device
   
@given('obsState is EMPTY')
def set_subarray_device_obstate(subarray_device):
    """Set the obsState to the specified value.

    This function sets the device state to ON.

    :param subarray_device: an SDPSubarray device

    """
    # This needs more thought as there seems no way to change obsState 
    # back from, # for example, IDLE by using Tango commands!
    if(subarray_device.ObsState  != ObsState['EMPTY']):
       subarray_device.Off()
       wait_for_change(subarray_device, 'OFF')
    
    if(subarray_device.state() != tango.DevState.names['ON']): 
       subarray_device.On()
       wait_for_change(subarray_device, 'ON')

# ----------
# When steps
# ----------

@when(parsers.parse('I call {command:S}'))
@when('I call <command>')
def command(subarray_device, command):
    """Call the device commands.

    :param subarray_device: SDPSubarray device
    :param command: name of command to call

    """
    # Check command is present
    command_list = subarray_device.get_command_list()
    assert command in command_list
    # Get information about the command and the command itself
    command_config = subarray_device.get_command_config(command)
    command_func = getattr(subarray_device, command)

    try:
        # Call the command
        if command_config.in_type == tango.DevVoid:
            command_func()
        elif command_config.in_type == tango.DevString:
            config_str = read_command_argument(command)
            command_func(config_str)
        else:
            message = 'Cannot handle command with argument type {}'
            raise ValueError(message.format(command_config.in_type))
        subarray_device.exception = None

    except tango.DevFailed as e:
        subarray_device.exception = e

# ----------
# Then steps
# ----------

@then(parsers.parse('the state should be {final_state:S}'))
@then('the state should be <final_state>')
def check_device_state(subarray_device, final_state):
    """Check the device state.

    :param subarray_device: SDPSubarray device
    :param final_state: expected state value

    """
    if(subarray_device.state() != tango.DevState.names[final_state]):
       wait_for_change(subarray_device, final_state)
       
@then(parsers.parse('obsState should be {final_obs_state:S}'))
@then('obsState should be <final_obs_state>')
def obs_state_equals(subarray_device, final_obs_state):
    """Check the Subarray obsState attribute value.

    :param subarray_device: an SDPSubarray device.
    :param final_obs_state: the expected obsState.
    """
    for _ in range(10):
       if subarray_device.ObsState == ObsState[final_obs_state]:
          break
       sleep(10)
    else:
       pytest.fail("State failed to change after 10 seconds!")

@then('receiveAddresses should have the expected value')
def receive_addresses_expected(subarray_device):
    """Check that the receiveAddresses value is as expected.

    :param subarray_device: An SDPSubarray device.

    """

    # Get the expected receive addresses from the data file
    receive_addresses_expected = read_receive_addresses()
    receive_addresses = json.loads(subarray_device.receiveAddresses)
    assert receive_addresses == receive_addresses_expected
    
# -----------------------------------------------------------------------------
# Ancillary functions
# -----------------------------------------------------------------------------

def read_command_argument(name, invalid=False, decode=False):
    """Read command argument from JSON file.

    :param name: name of command
    :param invalid: read the invalid version of the argument
    :param decode: decode the JSON data into Python

    """
    if invalid:
        fmt = 'command_{}_invalid.json'
    else:
        fmt = 'command_{}.json'
    return read_json_data(fmt.format(name), decode=decode)

def wait_for_change(device, state):
   """ Wait for any Tango processing delay until device state changes
   
   :param device: SDPSubarray device
   :param state: The expected state
   """
   for _ in range(10):
      if device.State() == tango.DevState.names[state]:
         break
      sleep(0.5)
   else:
      pytest.fail("State failed to change after 5 seconds!")
   return

def read_receive_addresses():
    """Read receive addresses from JSON file."""
    return read_json_data('receive_addresses.json', decode=True)


def read_json_data(filename, decode=False):
    """Read JSON file from data directory.

    If the file does not exist, it returns an empty JSON object.

    :param decode: decode the JSON data into Python

    """
    path = os.path.join(os.path.dirname(__file__), 'data', filename)
    if os.path.exists(path):
        with open(path, 'r') as file:
            data = file.read()
    else:
        data = '{}'
    if decode:
        data = json.loads(data)
    return data
