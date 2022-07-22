Feature: Device creation
  Scenario: Device created successfully
    Given user is logged in
    When user tries to create device with name 'Fridge'
    Then device is created successfully
