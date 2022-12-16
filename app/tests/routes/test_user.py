import pytest


''' Test adding a new user '''
def test_add_user(test_client):

    # Adding a user with a missing field, expecting an error: 
    new_user = pytest.sample_users[0].copy()
    del new_user['last_name']
    response = test_client.post('/users/', json=new_user)
    assert response.status_code == 400, \
        f'Incorrect status code {response.status_code} after adding a user with missing last name'
    
    # Adding a user with an invalid email, expecting an error: 
    new_user['last_name'] = 'Doe'
    new_user['email'] = 'john.com'
    response = test_client.post('/users/', json=new_user)
    assert response.status_code == 400, \
        f'Incorrect status code {response.status_code} after adding a user with invalid email'

    # Adding a valid user, expecting user returned with id:
    new_user['email'] = 'john.doe@gmail.com'
    response = test_client.post('/users/', json=new_user)
    assert response.status_code == 200, \
        f'Incorrect status code {response.status_code} after adding a valid user'
    assert response.json.get('id'), \
        'Empty id after adding a valid user'

    # Adding a user with an existing email, expecting an error: 
    response = test_client.post('/users/', json=new_user)
    assert response.status_code == 400, \
        f'Incorrect status code {response.status_code} after adding a user with existing email'


''' Test getting a user by id '''
def test_get_user(test_client):

    # Adding a sample user: 
    new_user = pytest.sample_users[0]
    response = test_client.post('/users/', json=new_user)
    assert response.status_code == 200, \
        f'Incorrect status code {response.status_code} after adding a valid user'
    new_user_id = response.json.get('id')

    # Getting the existing user by id, expecting user returned:
    response = test_client.get(f'/users/{new_user_id}')
    assert response.status_code == 200, \
        f'Incorrect status code {response.status_code} after getting an existing user'
    assert response.json.get('id') == new_user_id, \
        f'Incorrect id {response.json.get("id")} after getting an existing user'
    assert response.json.get('first_name') == new_user['first_name'], \
        f'Incorrect first_name {response.json.get("first_name")} after getting an existing user'
    assert response.json.get('last_name') == new_user['last_name'], \
        f'Incorrect last_name {response.json.get("last_name")} after getting an existing user'
    assert response.json.get('email') == new_user['email'], \
        f'Incorrect email {response.json.get("email")} after getting an existing user'
    assert response.json.get('birth_date', '').startswith(new_user['birth_date']), \
        f'Incorrect birth_date {response.json.get("birth_date")} after getting an existing user'

    # Getting a non-existing user by id, expecting an error: 
    response = test_client.get(f'/users/{new_user_id+1}')
    assert response.status_code == 400, \
        f'Incorrect status code {response.status_code} after getting a non-existing user'


''' Test listing users and searching by name '''
def test_list_users(test_client):

    # Adding two sample users:
    new_user = pytest.sample_users[0]
    response = test_client.post('/users/', json=new_user)
    assert response.status_code == 200, \
        f'Incorrect status code {response.status_code} after adding a valid user'

    new_user2 = pytest.sample_users[1]
    response = test_client.post('/users/', json=new_user2)
    assert response.status_code == 200, \
        f'Incorrect status code {response.status_code} after adding a valid user'

    # Getting list of users, expecting two users returned ordered by last name:
    response = test_client.get('/users/')
    assert response.status_code == 200, \
        f'Incorrect status code {response.status_code} after getting the list of users'
    assert len(response.json) == 2, \
        f'Incorrect list length {len(response.json)} after getting the list of users'
    assert response.json[0]['last_name'] == 'Baker', \
        f'Incorrect last name of first user {response.json[0]["last_name"]} after getting the list of users'

    # Searching user by last name, expecting a specific user returned:
    response = test_client.get('/users/', query_string={'last_name': 'Doe'})
    assert response.status_code == 200, \
        f'Incorrect status code {response.status_code} after searching users by last name'
    assert len(response.json) == 1, \
        f'Incorrect list length {len(response.json)} after searching users by last name'
    assert response.json[0]["first_name"] == 'John', \
        f'Incorrect first name of user {response.json[0]["first_name"]} after searching users by last name'


''' Test removing user by id '''
def test_remove_user(test_client):

    # Adding a sample user: 
    new_user = pytest.sample_users[0]
    response = test_client.post('/users/', json=new_user)
    assert response.status_code == 200, \
        f'Incorrect status code {response.status_code} after adding a valid user'
    new_user_id = response.json.get('id')

    # Removing the existing user, expecting user returned:
    response = test_client.delete(f'/users/{new_user_id}')
    assert response.status_code == 200, \
        f'Incorrect status code {response.status_code} after removing an existing user'
    assert response.json.get('id') == new_user_id, \
        f'Incorrect id {response.json.get("id")} after removing an existing user'

    # Getting the removed user by id, expecting an error:
    response = test_client.get(f'/users/{new_user_id}')
    assert response.status_code == 400, \
        f'Incorrect status code {response.status_code} after getting the removed user'
