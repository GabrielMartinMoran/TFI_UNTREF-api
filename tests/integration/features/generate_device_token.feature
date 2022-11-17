Feature: Generate device token

  Scenario: Generate token
    Given user is logged in
    And device with id '33523ad3-650f-4904-b325-b2e24637be6a' exists for logged user
    When user tries to generate a token for device with id '33523ad3-650f-4904-b325-b2e24637be6a'
    Then device token is returned successfully
