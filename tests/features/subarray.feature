Feature: SDP Subarray Device

        Scenario: AssignResources command configures processing blocks and sets receive addresses
                Given I have an SDPSubarray device
                And obsState is EMPTY
                When I call AssignResources
                Then obsState should be IDLE
                And receiveAddresses should have the expected value
