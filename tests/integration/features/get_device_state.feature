Feature: Get device state

  Scenario: Get device state
    Given user is logged in
    And device with id '33523ad3-650f-4904-b325-22e24637be5a' exists for logged user
    And the state for device with id '33523ad3-650f-4904-b325-22e24637be5a' is turned on
    When user tries to get the device state for device with id '33523ad3-650f-4904-b325-22e24637be5a'
    Then device state is turned on