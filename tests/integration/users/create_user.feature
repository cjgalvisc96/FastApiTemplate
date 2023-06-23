Feature: Create a new product
    Scenario: Create a valid user
        Given I authenticate using the following credentials:
            {
                "username": "admin@gmail.com",
                "password": "admin",
                "scope": "users:all"
            }
        And I send a POST request to "/v1/users/1" with body:
            {
                "name": "TestName", 
                "lastname": "TestLastname",
                "email": "test@gmail.com",
                "password": "TestPassword"
            }
        Then The response status code should be "201"
        And The response body should be:
            {
                "name": "TestName", 
                "lastname": "TestLastname",
                "email": "test@gmail.com"
            } 
