Feature: Add measure to device
  Scenario: Add valid measure to device
    Given user is logged in
    And device with id '33523ad3-650f-4904-b325-22e24637be5a' exists for logged user
    When user tries to add a measure for device with id '33523ad3-650f-4904-b325-22e24637be5a'
    Then measure is added successfully

  Scenario: Try add invalid measure to device
    Given user is logged in
    And device with id '33523ad3-650f-4904-b325-22e24637be5a' exists for logged user
    When user tries to add an invalid measure for device with id '33523ad3-650f-4904-b325-22e24637be5a'
    Then measure addition fails
