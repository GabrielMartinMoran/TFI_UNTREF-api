Feature: Get device scheduling tasks

  Scenario: Get device tasks
    Given user is logged in
    And device with id '33523ad3-650f-4904-b325-22e24637be5a' exists for logged user
    And device with id '33523ad3-650f-4904-b325-22e24637be5a' has scheduling tasks
    When user tries to get scheduling tasks for device with id '33523ad3-650f-4904-b325-22e24637be5a'
    Then scheduling tasks are returned successfully
