Feature: SDP Master Device

    Scenario: On command succeeds
        Given the SDP Master device
        And its state is STANDBY
        When I call On
        Then its state should become ON
