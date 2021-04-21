Feature: SDP Master Device

    Scenario Outline: Command succeeds in allowed state
        Given I have an SDPMaster device
        When the state is <initial_state>
        And I call <command>
        Then the state should be <final_state>
#        And the log should contain a transaction ID

        Examples:
        | command | initial_state | final_state |
        | Off     | STANDBY       | OFF         |
        | Off     | DISABLE       | OFF         |
        | Off     | ON            | OFF         |
        | Standby | OFF           | STANDBY     |
        | Standby | DISABLE       | STANDBY     |
        | Standby | ON            | STANDBY     |
        | Disable | OFF           | DISABLE     |
        | Disable | STANDBY       | DISABLE     |
        | Disable | ON            | DISABLE     |
        | On      | OFF           | ON          |
        | On      | STANDBY       | ON          |
        | On      | DISABLE       | ON          |

