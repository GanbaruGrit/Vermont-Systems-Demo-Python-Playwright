# Vermont Systems Demo - Playwright Python
This is a demo testing suite for the end-to-end donation path for the WebTrac platform.
Notable additions from the JavaScript version:
- A virtual environment is being used 'venv' to handle dependency packages locally.
- API tests added in 'test_api_project.py' to simulate seeding the database and retrieving credentials.
- Page Object Model pattern is being used to make the tests modular and scalable.
- Page Object Fixtures added to expand capabilities for API testing.
- Tests were converted to being synchronized while leveraging Playwright's built in wait structure to improve efficiency.
- Parallel testing enabled using pytest-xdist to improve test speeds (currently working on multi-browser login tests to utilize).
