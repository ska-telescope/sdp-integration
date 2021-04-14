import os
import logging
from time import sleep

import pytest
import tango


from pytest_bdd import scenario, given, when, then

logger = logging.getLogger(__name__)

def wait_for_change(state):
   for _ in range(10):
      if pytest.dp.State() == state:
         break
      sleep(1)
   else:
      pytest.fail("State failed to change after 10 seconds!")
   return

@pytest.fixture
def global_var():
   pytest.dp = None

@scenario("features/master.feature", "On command succeeds")
def test_on_command():
   pass

@given("the SDP Master device")
def connect_to_master_device():
   pytest.dp = tango.DeviceProxy("test_sdp/elt/master")

@given("its state is STANDBY")
def check_standby_state():
   if pytest.dp.State() != tango._tango.DevState.STANDBY:
      pytest.dp.Standby()
   wait_for_change(tango._tango.DevState.STANDBY)

@when("I call On")
def call_on_command():
   pytest.dp.On()

@then("its state should become ON")
def check_state_change():
   wait_for_change(tango._tango.DevState.ON)
   logger.info("State change to ON")
     
