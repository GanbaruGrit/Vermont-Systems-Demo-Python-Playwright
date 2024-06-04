import time
from playwright.sync_api import APIRequestContext, Page, expect

webtrac_context = 'temp' # Populate via local API

# Mock API test using local database to simulate creating user and testing actions
def test_create_user(
    webtrac_context: APIRequestContext,
    project_column_ids: list[str]) -> None:

    # Prep test data
    now = time.time()
    note = f'Test entry at: {now}'

    # Create a new entry with username data
    c_response = webtrac_context.post(
        f'/projects/columns/{project_column_ids[0]}/users',
        data={'note': note})
    expect(c_response).to_be_ok()
    assert c_response.json()['note'] == note

    # Retrieve the newly created entry
    card_id = c_response.json()['id']
    r_response = webtrac_context.get(f'/projects/columns/users/{card_id}')
    expect(r_response).to_be_ok()
    assert r_response.json() == c_response.json()