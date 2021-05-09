Feature: SDP subarray

    Scenario: On command
        Given I connect to an SDP subarray
        And the state is OFF
        When I call On
        Then the state should be ON
        And obsState should be EMPTY

    Scenario: AssignResources command sets receive addresses
        Given I connect to an SDP subarray
        And obsState is EMPTY
        When I call AssignResources
        Then obsState should become IDLE
        And receiveAddresses should have the expected value

    Scenario: Configure command sets scan type
        Given I connect to an SDP subarray
        And obsState is IDLE
        When I call Configure
        Then obsState should be READY
        And scanType should have the expected value

    Scenario: Scan commands sets scan ID
        Given I connect to an SDP subarray
        And obsState is READY
        When I call Scan
        Then obsState should be SCANNING
        And scanID should have the expected value

    Scenario: EndScan commands clears scan ID
        Given I connect to an SDP subarray
        And obsState is SCANNING
        When I call EndScan
        Then obsState should be READY
        And scanID should be 0

    Scenario: End command clears scan type
        Given I connect to an SDP subarray
        And obsState is READY
        When I call End
        Then obsState should be IDLE
        And scanType should be empty

    Scenario: ReleaseResources command clears receive addresses
        Given I connect to an SDP subarray
        And obsState is IDLE
        When I call ReleaseResources
        Then obsState should be EMPTY
        And receiveAddresses should be empty

    Scenario: Off command
        Given I connect to an SDP subarray
        And the state is ON
        When I call Off
        Then the state should be OFF
        And obsState should be EMPTY
