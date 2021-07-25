Feature: Get measures from device
  Scenario: Get summarized measures from last 5 minutes
    Given user is logged in
    And device with id '33523ad3-650f-4904-b325-22e24637be5a' exists for logged user
    And device with id '33523ad3-650f-4904-b325-22e24637be5a' has recent measures
    When user tries to get measures for device with id '33523ad3-650f-4904-b325-22e24637be5a'
    Then summarized measures are returned successfully
