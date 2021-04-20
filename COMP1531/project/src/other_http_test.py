import json
import requests
from other import clear
from helper_server_tests import *

# Flockr permissions
FLOCKR_OWNER = 1
FLOCKR_MEMBER = 2


##########################################################################################
###                                   USERS/ALL TESTS                                  ###
##########################################################################################
def test_users_all_invalid_token(url):
    '''
    Test 1: Add 3 users
    Use an invalid token to get all users
    Assert that response is not 200(OK)
    '''
    http_register(url, 'Bob')
    http_register(url, 'Alice')
    token = http_register(url, 'George')['token']
    parameters = {
        'token': token + 'a'
    }
    response = requests.get(url + '/users/all', params=parameters)
    assert response.status_code == 400


def test_users_all_valid(url):
    '''
    Test 2: Add 3 users
    Use an valid token to get all users
    Assert that messages has length 3
    '''
    http_register(url, 'Bob')
    http_register(url, 'Alice')
    token = http_register(url, 'George')['token']
    parameters = {
        'token': token
    }
    response = requests.get(url + '/users/all', params=parameters)
    assert response.ok
    data = response.json()
    assert len(data['users']) == 3


##########################################################################################
###                                    SEARCH TESTS                                    ###
##########################################################################################
def test_search_invalid_token(url):
    '''
    Test 1: If an invalid token is input
    Raise AccessError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.get(url + '/search', \
        params={'token': token + 'a', 'query_str': 'Hi'})
    assert resp.status_code == 400


def test_search_empty_member(url):
    '''
    Test 2: If a member tries to search with an empty query_str
    Return empty messages list
    '''
    clear()
    u_id, token = http_register(url, 'Bobx').values()
    load_messages = http_load_message(url, 'Boby')
    owner_token = load_messages['user']['token']
    channel_publ = load_messages['public']
    channel_priv = load_messages['private']
    requests.post(url + '/channel/invite', \
        json={
            'token': owner_token,
            'channel_id': channel_priv,
            'u_id': u_id
        })
    requests.post(url + '/channel/invite', \
        json={
            'token': owner_token,
            'channel_id': channel_publ,
            'u_id': u_id
        })

    resp = requests.get(url + '/search', \
        params={'token': token, 'query_str': ''})
    assert resp.status_code == 200
    assert json.loads(resp.text) == {'messages':[]}

def test_search_channels_none(url):
    '''
    Test 3: Member tries to search for messages when no channels exist
    Return empty messages list
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.get(url + '/search', \
        params={'token': token, 'query_str': 'nothing exists'})
    response = resp.json()
    assert resp.status_code == 200
    assert response['messages'] == []

def test_search_member_public(url):
    '''
    Test 4: Register an owner and a member
    Ensure correct messages are returned when member tries to search for them
    '''
    load_messages = http_load_message(url, 'Bob')
    u_id, token = http_register(url, 'Alice').values()
    owner_token = load_messages['user']['token']
    channel_id = load_messages['public']

    requests.post(url + '/channel/invite', \
        json={
            'token': owner_token,
            'channel_id': channel_id,
            'u_id': u_id
        })

    resp = requests.get(url + '/search', \
        params={'token':token, 'query_str':'a'})
    assert resp.status_code == 200

    messages = resp.json()['messages']
    assert len(messages) == 2
    assert messages[0]['message'] == 'a'
    assert messages[1]['message'] == 'a'


##########################################################################################
###                          ADMIN/USERPERMISSION/CHANGE TESTS                         ###
##########################################################################################

def test_admin_userpermission_change_invalid_user_id(url):
    '''
    Test 1 - Input error when invalid uid
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    resp = requests.post(url + 'admin/userpermission/change', \
        json={
            'token': token,
            'u_id': "invalid_uid",
            'permission_id': FLOCKR_OWNER
        })
    assert resp.status_code == 400


def test_admin_userpermission_change_invalid_permission_id(url):
    '''
    Test 2 - Input error when invalid permission id
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    u_id2 = http_register(url, 'Sally')['u_id']
    resp = requests.post(url + 'admin/userpermission/change', \
        json={
            'token': token1,
            'u_id': u_id2,
            'permission_id': "invalid_permissionId"
        })
    assert resp.status_code == 400

def test_admin_userpermission_change_invalid_token(url):
    '''
    Test 3 - Access error when invalid token
    '''
    clear()
    http_register(url, 'Bob')['token']
    u_id2 = http_register(url, 'Sally')['token']
    resp = requests.post(url + '/admin/userpermission/change', \
        json={
            'token': "invalid_token",
            'u_id': u_id2,
            'permission_id': FLOCKR_OWNER
        })
    assert resp.status_code == 400


def test_admin_userpermission_is_owner(url):
    '''
    Test 4 - change permission id of user to member
    '''
    clear()
    owner_id, owner_token = http_register(url, 'Bob').values()
    owner_info = {
        'u_id': owner_id,
        'name_first': 'Bob',
        'name_last': 'Bob',
        'profile_img_url': ''
    }
    member_id, member_token = http_register(url, 'Alice').values()
    member_info = {
        'u_id': member_id,
        'name_first': 'Alice',
        'name_last': 'Alice',
        'profile_img_url': ''
    }

    payload = {
        'token': owner_token,
        'u_id': member_id,
        'permission_id': FLOCKR_OWNER
    }
    response = requests.post(url + 'admin/userpermission/change', json=payload)
    assert response.ok

    new_id, new_token = http_register(url, 'Greg').values()
    new_info = {
        'u_id': new_id,
        'name_first': 'Greg',
        'name_last': 'Greg',
        'profile_img_url': ''
    }

    channel_1 = http_create_public_channel(url, owner_token, 'a')

    payload = {'token': member_token, 'channel_id': channel_1}
    response = requests.post(url + 'channel/join', json=payload)
    assert response.ok

    payload = {'token': new_token, 'channel_id': channel_1}
    response = requests.post(url + 'channel/join', json=payload)
    assert response.ok

    payload = {
        'token': member_token,
        'channel_id': channel_1,
        'u_id': new_id
    }
    response = requests.post(url + 'channel/addowner', json=payload)
    assert response.ok

    p = {'token': member_token, 'channel_id': channel_1}
    response = requests.get(url + 'channel/details', params=p)
    assert response.ok

    owners = response.json()['owner_members']
    assert owners == [owner_info, member_info, new_info]


def test_admin_userpermission_not_owner(url):
    '''
    Test 5: user tries to change member permission id to owner but they are not an owner
    '''
    clear()
    owner_id, owner_token = http_register(url, 'Bob').values()
    owner_info = {
        'u_id': owner_id,
        'name_first': 'Bob',
        'name_last': 'Bob',
        'profile_img_url': ''
    }
    member1_id, member1_token = http_register(url, 'Alice').values()
    member1_info = {
        'u_id': member1_id,
        'name_first': 'Alice',
        'name_last': 'Alice',
        'profile_img_url': ''
    }
    member2_id, member2_token = http_register(url, 'Gaben').values()
    member2_info = {
        'u_id': member2_id,
        'name_first': 'Gaben',
        'name_last': 'Gaben',
        'profile_img_url': ''
    }

    payload = {
        'token': member1_token,
        'u_id': member2_id,
        'permission_id': FLOCKR_OWNER
    }
    response = requests.post(url + 'admin/userpermission/change', json=payload)
    assert response.status_code == 400

    payload = {
        'token': member2_token,
        'u_id': member1_id,
        'permission_id': FLOCKR_OWNER
    }
    response = requests.post(url + 'admin/userpermission/change', json=payload)
    assert response.status_code == 400

    payload = {
        'token': owner_token,
        'u_id': member1_id,
        'permission_id': FLOCKR_OWNER
    }
    response = requests.post(url + 'admin/userpermission/change', json=payload)
    assert response.ok

    channel_1 = http_create_public_channel(url, owner_token, 'a')

    payload = {'token': member2_token, 'channel_id': channel_1}
    response = requests.post(url + 'channel/join', json=payload)
    assert response.ok

    payload = {'token': member1_token, 'channel_id': channel_1}
    response = requests.post(url + 'channel/join', json=payload)
    assert response.ok

    payload = {
        'token': member1_token,
        'channel_id': channel_1,
        'u_id': member2_id
    }
    response = requests.post(url + 'channel/addowner', json=payload)
    assert response.ok

    p = {'token': member1_token, 'channel_id': channel_1}
    response = requests.get(url + 'channel/details', params=p)
    assert response.ok

    owners = response.json()['owner_members']
    assert owners == [owner_info, member1_info, member2_info]


def test_admin_userpermission_owner_to_member(url):
    '''
    Test 6: owner first make member owner, then 2nd owner make first owner into member
    '''
    clear()
    owner_id, owner_token = http_register(url, 'Bob').values()
    member_id, member_token = http_register(url, 'Alice').values()

    payload = {
        'token': owner_token,
        'u_id': member_id,
        'permission_id': FLOCKR_OWNER
    }
    response = requests.post(url + 'admin/userpermission/change', json=payload)
    assert response.ok

    payload = {
        'token': member_token,
        'u_id': owner_id,
        'permission_id': FLOCKR_MEMBER
    }
    response = requests.post(url + 'admin/userpermission/change', json=payload)
    assert response.ok

    channel_1 = http_create_public_channel(url, member_token, 'a')

    payload = {
        'token': owner_token,
        'channel_id': channel_1,
        'u_id': member_id
    }
    response = requests.post(url + 'channel/removeowner', json=payload)
    assert response.status_code == 400
