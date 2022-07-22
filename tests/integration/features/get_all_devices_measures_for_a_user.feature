Feature: Get all devices measures for a user
  Scenario: Get summarized measures from last 5 minutes for all user's device
    Given user is logged in
    And device with id '33523ad3-650f-4904-b325-22e24637be6a' exists for logged user
    And device with id '33523ad3-650f-4904-b325-22e24637be6b' exists for logged user
    And device with id '33523ad3-650f-4904-b325-22e24637be6c' exists for logged user
    And device with id '33523ad3-650f-4904-b325-22e24637be6a' has recent measures
    And device with id '33523ad3-650f-4904-b325-22e24637be6b' has recent measures
    And device with id '33523ad3-650f-4904-b325-22e24637be6c' has recent measures
    When user tries to get measures for all devices
    Then summarized measures are returned successfully
