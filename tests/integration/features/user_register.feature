Feature: User registration
  Scenario: Unregistered user registration
    Given user is not registered
    When user tries to register with username 'test_user', email 'test_user@test.com' and password 'Passw0rd'
    Then user registers successfully

  Scenario: Invalid password on user registration
    Given user is not registered
    When user tries to register with username 'test_user', email 'test_user@test.com' and password 'invalid_password'
    Then user registration fails
    And error is 'User.password is not valid'

  Scenario: Invalid email on user registration
    Given user is not registered
    When user tries to register with username 'test_user', email 'invalid_email' and password 'Password'
    Then user registration fails
    And error is 'User.email is not a valid email address'

  Scenario: Invalid username on user registration
    Given user is not registered
    When user tries to register with username '_', email 'test_user@test.com' and password 'Password'
    Then user registration fails
    And error is 'User.username is shorter than 3'

  Scenario: User already registered
    Given user with email 'already_registered_user@test.com' is already registered
    When user tries to register with username 'already_registered_user', email 'already_registered_user@test.com' and password 'Passw0rd'
    Then user registration fails
    And error is 'User with same email already exists'