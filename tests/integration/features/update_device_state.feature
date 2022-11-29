Feature: Update device state

  Scenario: Set device state to turned_on
    Given user is logged in
    And device with id '33523ad3-650f-4904-b325-22e24637be5a' exists for logged user
    When user tries to update the device state as turned_on for device with id '33523ad3-650f-4904-b325-22e24637be5a'
    Then device state is updated successfully