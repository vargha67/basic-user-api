import pytest


''' Test granting permission to user '''
def test_add_user_permission(test_client):

    # Adding a sample user: 
    new_user = pytest.sample_users[0]
    response = test_client.post('/users/', json=new_user)
    assert response.status_code == 200, \
        f'Incorrect status code {response.status_code} after adding a valid user'
    new_user_id = response.json.get('id')

    # Adding an invalid permission type to user, expecting an error:
    new_perm = {
        'type': 'INVALID'
    }
    response = test_client.post(f'/users/{new_user_id}/permissions/', json=new_perm)
    assert response.status_code == 400, \
        f'Incorrect status code {response.status_code} after adding an invalid permission to user'

    # Adding a valid permission type to user, expecting the user permission item returned:
    new_perm['type'] = 'BASIC'
    response = test_client.post(f'/users/{new_user_id}/permissions/', json=new_perm)
    assert response.status_code == 200, \
        f'Incorrect status code {response.status_code} after adding a valid permission to user'
    assert response.json.get('user_id') == new_user_id, \
        f'Incorrect user id {response.json.get("user_id")} after adding a valid permission to user'
    assert response.json.get('type') == new_perm['type'], \
        f'Incorrect type {response.json.get("type")} after adding a valid permission to user'
    
    # Adding an existing permission type to user, expecting an error:
    response = test_client.post(f'/users/{new_user_id}/permissions/', json=new_perm)
    assert response.status_code == 400, \
        f'Incorrect status code {response.status_code} after adding an existing permission type to user'


''' Test revoking permission from user '''
def test_remove_user_permission(test_client):

    # Adding a sample user: 
    new_user = pytest.sample_users[0]
    response = test_client.post('/users/', json=new_user)
    assert response.status_code == 200, \
        f'Incorrect status code {response.status_code} after adding a valid user'
    new_user_id = response.json.get('id')

    # Adding a permission to user:
    new_perm = {
        'type': 'BASIC'
    }
    response = test_client.post(f'/users/{new_user_id}/permissions/', json=new_perm)
    assert response.status_code == 200, \
        f'Incorrect status code {response.status_code} after adding a permission to user'
    
    # Removing a permission type from user, expecting the removed user permission returned:
    response = test_client.delete(f'/users/{new_user_id}/permissions/{new_perm["type"]}')
    assert response.status_code == 200, \
        f'Incorrect status code {response.status_code} after removing a permission type from user'
    assert response.json.get('user_id') == new_user_id, \
        f'Incorrect user id {response.json.get("user_id")} after removing a permission type from user'
    assert response.json.get('type') == new_perm['type'], \
        f'Incorrect type {response.json.get("type")} after removing a permission type from user'

    # Removing a non-existing permission type from user, expecting an error:
    response = test_client.delete(f'/users/{new_user_id}/permissions/{new_perm["type"]}')
    assert response.status_code == 400, \
        f'Incorrect status code {response.status_code} after removing a non-existing permission type from user'
