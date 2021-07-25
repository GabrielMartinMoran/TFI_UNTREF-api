Feature: User login
  Scenario: Registered user login
    Given user with email 'test_login_user@test.com' is already registered with password 'Passw0rd'
    When user tries to login with email 'test_login_user@test.com' and password 'Passw0rd'
    Then user logs in successfully

  Scenario: Unregistered user login
    Given user is not registered
    When user tries to login with email 'unregistered_user@test.com' and password 'Passw0rd'
    Then user login fails