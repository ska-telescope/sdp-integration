import os
import logging
from time import sleep

import pytest
import tango

from pytest_bdd import scenarios, given, when, then, parsers

logger = logging.getLogger(__name__)

#@pytest.fixture
#def sdp_config():
#   return ska_sdp_config.Config()


scenarios("features/master.feature")

# -----------
# Given steps
# -----------

@given("I have an SDPMaster device", target_fixture='master_device')
def connect_to_master_device():
   device = tango.DeviceProxy("test_sdp/elt/master")
   return device
   
# ----------
# Then steps
# ----------

@when(parsers.parse('the state is {initial_state:S}'))
@when('the state is <initial_state>')
def set_device_state(master_device, initial_state):
    """Set the device state.

    :param master_device: SDPMaster device
    :param state_value: desired device state

    """
    # Set the device state if incorrect
    if(master_device.state() != tango.DevState.names[initial_state]):
        # Get command function
       command_func = getattr(master_device, initial_state)
       # Call the command
       command_func()
            
       # Check that state has been set correctly
 
       wait_for_change(master_device, initial_state)    

@when(parsers.parse('I call {command:S}'))
@when('I call <command>')
def command(master_device, command):
    """Call the device commands.

    :param master_device: SDPMaster device
    :param command: name of command to call

    """
    # Check command is present
    command_list = master_device.get_command_list()
    assert command in command_list
    
    # Get command function
    command_func = getattr(master_device, command)
    # Call the command
    command_func()

# ----------
# Then steps
# ----------

@then(parsers.parse('the state should be {final_state:S}'))
@then('the state should be <final_state>')
def check_device_state(master_device, final_state):
    """Check the device state.

    :param master_device: SDPMaster device
    :param final_state: expected state value

    """
    if(master_device.state() != tango.DevState.names[final_state]):
       wait_for_change(master_device, final_state)
    
# -----------------------------------------------------------------------------
# Ancillary functions
# -----------------------------------------------------------------------------

def wait_for_change(device, state):
   """ Wait for any processing time un til device state changes
   
   :param device: Tamgo device DevProxy
   :param state: The expected state
   """
   for _ in range(10):
      if device.State() == tango.DevState.names[state]:
         break
      sleep(1)
   else:
      pytest.fail("State failed to change after 10 seconds!")
   return

