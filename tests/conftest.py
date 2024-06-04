import pytest
import os
from playwright.sync_api import Page, Expect, Playwright, APIRequestContext
from typing import Generator

webtrac_access_token = 12345678 # Populate via local API

# API Fixtures - Scope set to 'session' to ensure that their only read once
@pytest.fixture(scope='session')
def webtrac_username() -> str:
    return _get_env_var('WEBTRAC_USERNAME')

@pytest.fixture(scope='session')
def webtrac_username_password() -> str:
    return _get_env_var('WEBTRAC_PASSWORD')

@pytest.fixture(scope='session')
def webtrac_username_access_token() -> str:
    return _get_env_var('WEBTRAC_ACCESS_TOKEN')

@pytest.fixture(scope='session')
def webtrac_username_project_name() -> str:
    return _get_env_var('WEBTRAC_PROJECT_NAME')

# API Testing - Reads environment variable by name and checks that it has value
def _get_env_var(varname: str) -> str:
    value = os.getenv(varname)
    assert value, f'{varname} is not set'
    return value

# Get target project
@pytest.fixture(scope='session')
def webtrac_project(
    webtrac_context: APIRequestContext,
    webtrac_username: str,
    webtrac_project_name: str) -> dict:

    resource = f'/users/{webtrac_username}/projects'
    response = webtrac_context.get(resource)
    Expect(response).to_be_ok()
    
    name_match = lambda x: x['name'] == webtrac_project_name
    filtered = filter(name_match, response.json())
    project = list(filtered)[0]
    assert project

    return project

# Get list of columns for project
@pytest.fixture()
def project_columns(
    webtrac_context: APIRequestContext,
    webtrac_project: dict) -> list[dict]:
    
    response = webtrac_context.get(webtrac_project['columns_url'])
    Expect(response).to_be_ok()

    columns = response.json()
    assert len(columns) >= 2
    return columns

# Get column IDs
@pytest.fixture()
def project_column_ids(project_columns: list[dict]) -> list[str]:
    return list(map(lambda x: x['id'], project_columns))

# Request context object to make API calls cleaner
@pytest.fixture(scope='session')
def webtrac_context(
    playwright: Playwright,
    webtrac_access_token: str) -> Generator[APIRequestContext, None, None]:

    headers = {
        "Accept": "application/vnd.webtrac.v3+json",
        "Authorization": f"token {webtrac_access_token}"}

    request_context = playwright.request.new_context(
        base_url="http://localhost/api",
        extra_http_headers=headers)

    yield request_context
    request_context.dispose()