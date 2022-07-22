Feature: Get user data
  Scenario: Get logged user data
    Given user is logged in
    When user tries to get his data
    Then user data is returned
