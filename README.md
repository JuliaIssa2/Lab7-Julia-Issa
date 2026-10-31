# Lab 7 – Python Testing

**Student:** Julia Issa  
**Course:** Software Tools Lab  
**Lab:** Lab 7 – Python Testing

## Overview

This project extends the Flask and SQLite user management application from Lab 5 by adding automated tests using pytest.

The tests verify both the database functions and Flask REST API endpoints.

## Tested Functionality

The test suite covers:

- Database creation and initial users
- `insert_user()`
- `get_users()`
- `get_user_by_id()`
- `update_user()`
- `delete_user()`
- GET user API
- ADD user API
- UPDATE user API
- DELETE user API

API tests verify both HTTP response status codes and returned JSON data.

## Installation

Create and activate a virtual environment, then install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Tests

Run:

```bash
python -m pytest -v --basetemp=.pytest_temp
```

## Test Result

All tests pass successfully:

```text
12 passed
```

A screenshot of the successful test run is included in the repository.