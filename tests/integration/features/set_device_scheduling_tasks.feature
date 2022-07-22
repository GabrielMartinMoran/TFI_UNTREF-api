Feature: Set device scheduling tasks

  Scenario: Set device tasks
    Given user is logged in
    And device with id '33523ad3-650f-4904-b325-22e24637be5a' exists for logged user
    When user tries to set some valid scheduling task to the device with id '33523ad3-650f-4904-b325-22e24637be5a'
    Then device has those scheduling tasks configured successfully
