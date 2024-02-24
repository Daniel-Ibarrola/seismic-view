# Changelog

## v0.3.2 (6/09/2023)

### Command Line interface
New flask CLI commands:

- Command to remove users.
- Command to update users password.
- Command to list users

All previous commands require authentication.

## v0.3.1 (5/09/2023)

### Bugfixes
- Fixed not being able to add user through add-user command if the new user email
was not in the valid emails list.

## v0.3.0 (5/09/2023)

### Features
- New flask CLI command to insert new valid emails (requires authentication).
- New flask CLI command to insert new users (requires authentication). 
- User passwords are no longer validated.

## v0.2.1 (16/08/2023)
- Updated domain name

## v0.2.0 (15/08/2023)

- Sample nginx configuration files.
- Health checks for containers.

## v0.1.0 (9/08/2023)

First release.

### Features
- Authenticate users with token based authentication.
- Can only register users on the emails.txt file.
- Users are stored to a sqlite database.
- Can run the app in development and production mode.
- Can run the app in containers

### Tests
- Unit and integration tests.
- CI through GitGub actions.