Feature: Set device scheduling tasks

  Scenario: Get device next scheduling task
    Given user is logged in
    And device with id '33523ad3-650f-4904-b325-22e24637be5a' exists for logged user
    And device with id '33523ad3-650f-4904-b325-22e24637be5a' has scheduling tasks
    When user tries to get next scheduling tasks for device with id '33523ad3-650f-4904-b325-22e24637be5a'
    Then next device scheduling task is returned successfully
