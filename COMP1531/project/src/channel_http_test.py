'''
http server tests for channel routes in server.py
'''
import json
import requests
from other import clear
from helper_server_tests import http_register, http_create_private_channel, \
    http_create_public_channel
from auth import *
from channel import *
from user import *

##########################################################################################
###                ✨ ✨ ✨ CHANNEL/INVITE HTTP TESTS ✨ ✨ ✨                      ###
##########################################################################################
def test_channel_invite_invalid_token(url):
    '''
    Test 1:
    Use invalid token to invite another user
    Asserts that response is 400
    '''
    clear()
    route = url + 'channel/invite'
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')
    u_id = http_register(url, 'Alice')['u_id']

    payload = {
        'token': token + 'a',
        'channel_id': '',
        'u_id': u_id
    }

    payload['channel_id'] = public
    response = requests.post(route, json=payload)
    assert response.status_code == 400

    payload['channel_id'] = private
    response = requests.post(route, json=payload)
    assert response.status_code == 400


def test_channel_invite_invalid_channel_id(url):
    '''
    Test 2:
    Use invalid channel id to invite another user
    Asserts that response is 400
    '''
    clear()
    route = url + 'channel/invite'
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')
    u_id = http_register(url, 'Alice')['u_id']

    payload = {
        'token': token,
        'channel_id': '',
        'u_id': u_id
    }

    payload['channel_id'] = public + 100
    response = requests.post(route, json=payload)
    assert response.status_code == 400

    payload['channel_id'] = private + 100
    response = requests.post(route, json=payload)
    assert response.status_code == 400


def test_channel_invite_invalid_uid(url):
    '''
    Test 3:
    Invite someone that has doesn't exist (invalid u_id)
    Assert that response is 400
    '''
    clear()
    route = url + 'channel/invite'
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')
    u_id = http_register(url, 'Alice')['u_id']

    payload = {
        'token': token,
        'channel_id': '',
        'u_id': u_id + 100
    }

    payload['channel_id'] = public
    response = requests.post(route, json=payload)
    assert response.status_code == 400

    payload['channel_id'] = private
    response = requests.post(route, json=payload)
    assert response.status_code == 400


def test_channel_invite_authorised_user_not_in_channel(url):
    '''
    Test 4:
    Use a token from a user not in channel to invite another
    user that is not in channel
    Assert that response is not 200 (OK)
    '''
    clear()
    route = url + 'channel/invite'
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')

    token = http_register(url, 'Toby')['token']
    u_id = http_register(url, 'Alice')['u_id']

    payload = {
        'token': token,
        'channel_id': '',
        'u_id': u_id
    }

    payload['channel_id'] = public
    response = requests.post(route, json=payload)
    assert response.status_code == 400

    payload['channel_id'] = private
    response = requests.post(route, json=payload)
    assert response.status_code == 400


def test_channel_invite_valid(url):
    '''
    Test 5:
    Invite another user into the channel,
    tests for both private and public channel
    Check with `channel/details` route to ensure
    added u_id is present
    '''
    clear()
    route = url + 'channel/invite'
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')
    u_id = http_register(url, 'Alice')['u_id']

    payload = {
        'token': token,
        'channel_id': '',
        'u_id': u_id
    }

    detail_route = url + 'channel/details'

    payload['channel_id'] = public
    response = requests.post(route, json=payload)
    assert response.ok
    parameters = {'token': token, 'channel_id': public}
    response = requests.get(detail_route, params=parameters)
    assert response.ok
    assert u_id in [x['u_id'] for x in response.json()['all_members']]

    payload['channel_id'] = private
    response = requests.post(route, json=payload)
    assert response.ok
    parameters = {'token': token, 'channel_id': private}
    response = requests.get(detail_route, params=parameters)
    assert response.ok
    assert u_id in [x['u_id'] for x in response.json()['all_members']]


##########################################################################################
###                       ✨ ✨ ✨ CHANNEL/DETAILS HTTP TESTS ✨ ✨ ✨                     ###
##########################################################################################

def test_channel_details_invalid_token(url):
    '''
    Test 1:
    Add private, and public channel
    Add another user in
    Get channel details using invalid token
    Asserts that response is 400
    '''
    clear()
    route = url + 'channel/invite'
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')
    u_id = http_register(url, 'Alice')['u_id']

    payload = {
        'token': token,
        'channel_id': '',
        'u_id': u_id
    }

    payload['channel_id'] = public
    response = requests.post(route, json=payload)
    assert response.ok

    payload['channel_id'] = private
    response = requests.post(route, json=payload)
    assert response.ok

    parameters = {
        'token': token + '1',
        'channel_id':''
    }

    route = url + 'channel/details'

    parameters['channel_id'] = public
    response = requests.get(route, params=parameters)
    assert response.status_code == 400

    parameters['channel_id'] = private
    response = requests.get(route, params=parameters)
    assert response.status_code == 400


def test_channel_details_invalid_channel_id(url):
    '''
    Test 2:
    Add private, and public channel
    Add another user in
    Get channel details with invalid channel id
    Asserts that response is 400
    '''
    clear()
    route = url + 'channel/invite'
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')
    u_id = http_register(url, 'Alice')['u_id']

    payload = {
        'token': token,
        'channel_id': '',
        'u_id': u_id
    }

    payload['channel_id'] = public
    response = requests.post(route, json=payload)
    assert response.ok

    payload['channel_id'] = private
    response = requests.post(route, json=payload)
    assert response.ok

    parameters = {
        'token': token,
        'channel_id':''
    }

    route = url + 'channel/details'

    parameters['channel_id'] = public + 300
    response = requests.get(route, params=parameters)
    assert response.status_code == 400

    parameters['channel_id'] = private + 300
    response = requests.get(route, params=parameters)
    assert response.status_code == 400


def test_channel_details_authorised_user_not_in_channel(url):
    '''
    Test 3:
    Add private, and public channel
    Add another user in
    Get channel details using token of a user thats not a member
    of the channel
    Asserts that response is 400
    '''
    clear()
    route = url + 'channel/invite'
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')
    u_id = http_register(url, 'Alice')['u_id']

    payload = {
        'token': token,
        'channel_id': '',
        'u_id': u_id
    }

    payload['channel_id'] = public
    response = requests.post(route, json=payload)
    assert response.ok

    payload['channel_id'] = private
    response = requests.post(route, json=payload)
    assert response.ok

    parameters = {
        'token': http_register(url, 'Elon')['token'],
        'channel_id':''
    }

    route = url + 'channel/details'

    parameters['channel_id'] = public
    response = requests.get(route, params=parameters)
    assert response.status_code == 400

    parameters['channel_id'] = private
    response = requests.get(route, params=parameters)
    assert response.status_code == 400


def test_channel_details_valid(url):
    '''
    Test 4:
    Valid channel details test
    Asserts that response400
    Asserts that details contains the correct u_id(s)
    '''
    clear()
    route = url + 'channel/invite'
    owner_id, token = http_register(url, 'Bob').values()
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')
    u_id = http_register(url, 'Alice')['u_id']

    payload = {
        'token': token,
        'channel_id': '',
        'u_id': u_id
    }

    payload['channel_id'] = public
    response = requests.post(route, json=payload)
    assert response.ok

    payload['channel_id'] = private
    response = requests.post(route, json=payload)
    assert response.ok

    parameters = {
        'token': token,
        'channel_id':''
    }

    route = url + 'channel/details'

    parameters['channel_id'] = public
    response = requests.get(route, params=parameters)
    assert response.ok
    assert owner_id in [x['u_id'] for x in response.json()['owner_members']]
    assert u_id in [x['u_id'] for x in response.json()['all_members']]

    parameters['channel_id'] = private
    response = requests.get(route, params=parameters)
    assert response.ok
    assert owner_id in [x['u_id'] for x in response.json()['owner_members']]
    assert u_id in [x['u_id'] for x in response.json()['all_members']]


##########################################################################################
###                       ✨ ✨ ✨ CHANNEL/MESSAGES HTTP TESTS ✨ ✨ ✨                    ###
##########################################################################################

def test_channel_messages_invalid_token(url):
    '''
    Test 1:
    Make channels, send messages
    Then use invalid token to get messages from channel
    Asserts that response is 400
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')

    parameters = {
        'token': token + 'a',
        'channel_id': '',
        'start': 1
    }

    data = {'token': token, 'channel_id':'', 'message':''}
    for msg in 'qwertyqwop':
        data['message'] = msg

        data['channel_id'] = public
        response = requests.post(url + 'message/send', json=data)
        assert response.ok

        data['channel_id'] = private
        response = requests.post(url + 'message/send', json=data)
        assert response.ok

    parameters['channel_id'] = public
    response = requests.get(url + 'channel/messages', params=parameters)
    assert response.status_code == 400

    parameters['channel_id'] = private
    response = requests.get(url + 'channel/messages', params=parameters)
    assert response.status_code == 400


def test_channel_messages_invalid_channel_id(url):
    '''
    Test 2:
    Make channels, send messages
    Then use invalid channel id to get messages from channel
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')

    parameters = {
        'token': token,
        'channel_id': '',
        'start': 1
    }

    data = {'token': token, 'channel_id':'', 'message':''}
    for msg in 'qwertyqwop':
        data['message'] = msg

        data['channel_id'] = public
        response = requests.post(url + 'message/send', json=data)
        assert response.ok

        data['channel_id'] = private
        response = requests.post(url + 'message/send', json=data)
        assert response.ok

    parameters['channel_id'] = public + 30
    response = requests.get(url + 'channel/messages', params=parameters)
    assert response.status_code == 400

    parameters['channel_id'] = private + 25
    response = requests.get(url + 'channel/messages', params=parameters)
    assert response.status_code == 400


def test_channel_messages_start_more_than_messages_in_channel(url):
    '''
    Test 3:
    Make channels, send messages
    Then get messages with start greater than total messages
    Asserts that response is 400
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')

    parameters = {
        'token': token,
        'channel_id': '',
        'start': 1000
    }

    data = {'token': token, 'channel_id':'', 'message':''}
    for msg in 'qwertyqwop':
        data['message'] = msg

        data['channel_id'] = public
        response = requests.post(url + 'message/send', json=data)
        assert response.ok

        data['channel_id'] = private
        response = requests.post(url + 'message/send', json=data)
        assert response.ok

    parameters['channel_id'] = public
    response = requests.get(url + 'channel/messages', params=parameters)
    assert response.status_code == 400

    parameters['channel_id'] = private
    response = requests.get(url + 'channel/messages', params=parameters)
    assert response.status_code == 400


def test_channel_messages_authorised_user_not_in_channel(url):
    '''
    Test 4:
    Make channels, send messages
    Get messages in channel using token from a user not in the channel
    Asserts that response is 400
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')

    parameters = {
        'token': http_register(url, 'Alice')['token'],
        'channel_id': '',
        'start': 1
    }

    data = {'token': token, 'channel_id':'', 'message':''}
    for msg in 'qwertyqwop':
        data['message'] = msg

        data['channel_id'] = public
        response = requests.post(url + 'message/send', json=data)
        assert response.ok

        data['channel_id'] = private
        response = requests.post(url + 'message/send', json=data)
        assert response.ok

    parameters['channel_id'] = public
    response = requests.get(url + 'channel/messages', params=parameters)
    assert response.status_code == 400

    parameters['channel_id'] = private
    response = requests.get(url + 'channel/messages', params=parameters)
    assert response.status_code == 400


def test_channel_messages_valid(url):
    '''
    Test 5:
    Make channels, send messages
    Get messages in channel
    Assert that reponse400
    Check that all messages are sent
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')

    parameters = {
        'token': token,
        'channel_id': '',
        'start': 0
    }

    data = {'token': token, 'channel_id':'', 'message':''}
    for msg in 'qwertyqwop':
        data['message'] = msg

        data['channel_id'] = public
        response = requests.post(url + 'message/send', json=data)
        assert response.ok

        data['channel_id'] = private
        response = requests.post(url + 'message/send', json=data)
        assert response.ok

    all_msg = 'qwertyqwop'[::-1]

    parameters['channel_id'] = public
    response = requests.get(url + 'channel/messages', params=parameters)
    assert response.ok
    assert response.json()['end'] == -1
    messages = response.json()['messages']
    assert all_msg == ''.join([x['message'] for x in messages])

    parameters['channel_id'] = private
    response = requests.get(url + 'channel/messages', params=parameters)
    assert response.ok
    assert response.json()['end'] == -1
    messages = response.json()['messages']
    assert all_msg == ''.join([x['message'] for x in messages])


##########################################################################################
###                        ✨ ✨ ✨ CHANNEL/LEAVE HTTP TESTS ✨ ✨ ✨                      ###
##########################################################################################

def test_channel_leave_invalid_token(url):
    '''
    Test 1:
    Create channel, add user
    User tries to leave using an invalid token
    Assert that response is 400
    '''
    clear()
    route = url + 'channel/invite'
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')
    u_id, user_token = http_register(url, 'Alice').values()

    payload = {
        'token': token,
        'channel_id': '',
        'u_id': u_id
    }

    data = {
        'token': user_token + 'a',
        'channel_id': ''
    }

    payload['channel_id'] = public
    response = requests.post(route, json=payload)
    assert response.ok
    data['channel_id'] = public
    response = requests.post(url + 'channel/leave', json=data)
    assert response.status_code == 400

    payload['channel_id'] = private
    response = requests.post(route, json=payload)
    assert response.ok
    data['channel_id'] = private
    response = requests.post(url + 'channel/leave', json=data)
    assert response.status_code == 400


def test_channel_leave_invalid_channel_id(url):
    '''
    Test 2:
    Create channel, add user
    User tries to leave using an invalid channel id
    Asserts that response is 400
    '''
    clear()
    route = url + 'channel/invite'
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')
    u_id, user_token = http_register(url, 'Alice').values()

    payload = {
        'token': token,
        'channel_id': '',
        'u_id': u_id
    }

    data = {
        'token': user_token,
        'channel_id': ''
    }

    payload['channel_id'] = public
    response = requests.post(route, json=payload)
    assert response.ok
    data['channel_id'] = public + 30
    response = requests.post(url + 'channel/leave', json=data)
    assert response.status_code == 400

    payload['channel_id'] = private
    response = requests.post(route, json=payload)
    assert response.ok
    data['channel_id'] = private + 30
    response = requests.post(url + 'channel/leave', json=data)
    assert response.status_code == 400


def test_channel_leave_authorised_user_not_in_channel(url):
    '''
    Test 3:
    Create channel, add user
    User tries to leave when user not in channel
    Asserts that response is 400
    '''
    clear()
    route = url + 'channel/invite'
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')
    u_id = http_register(url, 'Alice')['u_id']

    payload = {
        'token': token,
        'channel_id': '',
        'u_id': u_id
    }

    data = {
        'token': http_register(url, 'Elon')['token'],
        'channel_id': ''
    }

    payload['channel_id'] = public
    response = requests.post(route, json=payload)
    assert response.ok
    data['channel_id'] = public
    response = requests.post(url + 'channel/leave', json=data)
    assert response.status_code == 400

    payload['channel_id'] = private
    response = requests.post(route, json=payload)
    assert response.ok
    data['channel_id'] = private
    response = requests.post(url + 'channel/leave', json=data)
    assert response.status_code == 400


def test_channel_leave_valid(url):
    '''
    Test 4:
    Create channel, add user
    User leaves channel
    Asserts that response400
    '''
    clear()
    route = url + 'channel/invite'
    token = http_register(url, 'Bob')['token']
    public = http_create_public_channel(url, token, 'test')
    private = http_create_private_channel(url, token, 'test')
    u_id, user_token = http_register(url, 'Alice').values()

    payload = {
        'token': token,
        'channel_id': '',
        'u_id': u_id
    }

    data = {
        'token': user_token,
        'channel_id': ''
    }

    payload['channel_id'] = public
    response = requests.post(route, json=payload)
    assert response.ok
    data['channel_id'] = public
    response = requests.post(url + 'channel/leave', json=data)
    assert response.ok

    payload['channel_id'] = private
    response = requests.post(route, json=payload)
    assert response.ok
    data['channel_id'] = private
    response = requests.post(url + 'channel/leave', json=data)
    assert response.ok


##########################################################################################
###                         ✨ ✨ ✨ CHANNEL/JOIN HTTP TESTS ✨ ✨ ✨                      ###
##########################################################################################

def test_server_join_invalid_token(url):
    '''
    Test 1: invalid token, raise AccessError
    '''
    clear()
    token = http_register(url, "Bob")['token']
    channel_id = http_create_public_channel(url, token, 'Channel1')
    requests.post(url + '/auth/logout', json={'token': token})

    response = requests.post(url + '/channel/join', json={'token': token, 'channel_id': channel_id})
    assert response.status_code == 400


def test_server_join_invalid_channel_id(url):
    '''
    Test 2: invalid channel_id, raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    response = requests.post(url + '/channel/join', json={'token': token, 'channel_id': 1})
    assert response.status_code == 400


def test_server_join_access_error(url):
    '''
    Test 3: user tries to join private channel, raise AccessError
    '''

    clear()
    token1 = http_register(url, 'Bob')['token']
    token2 = http_register(url, 'Tim')['token']
    channel_id = http_create_private_channel(url, token1, 'Channel1')

    response = requests.post(url + '/channel/join', json={'token': token2, \
        'channel_id': channel_id})
    assert response.status_code == 400


def test_server_join_valid_one_channel(url):
    '''
    Test 4: test with one channel
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    token2 = http_register(url, 'Tim')['token']
    channel_id = http_create_public_channel(url, token1, 'Channel1')

    requests.post(url + '/channel/join', json={'token': token2, 'channel_id': channel_id})

    response = requests.get(url + '/channel/details', params={'token': token2, \
        'channel_id': channel_id})
    assert len(json.loads(response.text)['all_members']) == 2


def test_server_join_valid_multiple_channels(url):
    '''
    Test 5: test with multiple channels
    '''
    clear()
    u_id1, token1 = http_register(url, 'Bob').values()
    u_id2, token2 = http_register(url, 'Tim').values()
    u_id3, token3 = http_register(url, 'John').values()

    member1 = requests.get(url + '/user/profile', params={'token': token1, \
        'u_id': u_id1}).json()['user']
    member2 = requests.get(url + '/user/profile', params={'token': token2, \
        'u_id': u_id2}).json()['user']
    member3 = requests.get(url + '/user/profile', params={'token': token3, \
        'u_id': u_id3}).json()['user']

    # channel1 - user1, channel2 - user2
    channel_id1 = http_create_public_channel(url, token1, 'Channel1')
    channel_id2 = http_create_public_channel(url, token2, 'Channel2')
    # channel1 - user1, user3
    # channel2 - user2, user1
    requests.post(url + '/channel/join', json={'token': token3, \
        'channel_id': channel_id1})
    requests.post(url + '/channel/join', json={'token': token1, \
        'channel_id': channel_id2})
    # check users joined successfully
    response = requests.get(url + '/channel/details', params={'token': token1, \
        'channel_id': channel_id1})
    name_list = []
    for i in json.loads(response.text)['all_members']:
        name_list.append(i['name_first'])
    assert name_list == [member1['name_first'], member3['name_first']]

    response = requests.get(url + '/channel/details', params={'token': token2, \
        'channel_id': channel_id2})
    name_list2 = []
    for i in json.loads(response.text)['all_members']:
        name_list2.append(i['name_first'])
    assert name_list2 == [member2['name_first'], member1['name_first']]


def test_server_join_private_channel_global_owner(url):
    '''
    Test 6: global owner joins private channel
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    token2 = http_register(url, 'Tim')['token']
    channel_id = http_create_private_channel(url, token2, 'Channel1')

    requests.post(url + '/channel/join', json={'token': token1, \
        'channel_id': channel_id})

    response = requests.get(url + '/channel/details', params={'token': token2, \
        'channel_id': channel_id})
    assert len(json.loads(response.text)['all_members']) == 2


##########################################################################################
###                        ✨ ✨ ✨ CHANNEL_ADDOWNER TESTS ✨ ✨ ✨                        ###
##########################################################################################

def addowner_invalid_token(is_public, url):
    '''
    Test 1:
    Test addowner function with invalid token.
    Will raise AccessError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''

    token1 = http_register(url, 'Bob')['token']
    u_id2 = http_register(url, 'Tim')['u_id']
    if is_public:
        channel_id = http_create_public_channel(url, token1, 'Channel1')
    else:
        channel_id = http_create_private_channel(url, token1, 'Channel1')

    response = requests.post(url + '/channel/addowner', json={'token': token1 * 2, \
        'channel_id': channel_id, 'u_id': u_id2})
    assert response.status_code == 400


def test_addowner_invalid_token_pub(url):
    '''
    Test 2:
    Test addowner function,
    with invalid token for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_invalid_token(True, url)


def test_addowner_invalid_token_priv(url):
    '''
    Test 3:
    Test addowner function,
    with invalid token for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_invalid_token(False, url)


def addowner_invalid_channel_id(is_public, url):
    '''
    Test 4:
    Test addowner function with invalid channel id.
    Will raise InputError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''

    token = http_register(url, 'Bob')['token']
    u_id1 = http_register(url, 'Tim')['u_id']
    if is_public:
        channel_id = http_create_public_channel(url, token, 'Channel1')
    else:
        channel_id = http_create_private_channel(url, token, 'Channel1')

    response = requests.post(url + '/channel/addowner', json={'token': token, \
        'channel_id': channel_id + 100, 'u_id': u_id1})
    assert response.status_code == 400


def test_addowner_invalid_channel_id_pub(url):
    '''
    Test 5:
    Test addowner function,
    with invalid channel id for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_invalid_channel_id(True, url)


def test_addowner_invalid_channel_id_priv(url):
    '''
    Test 6:
    Test addowner function,
    with invalid channel id for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_invalid_channel_id(False, url)


def addowner_invalid_uid(is_public, url):
    '''
    Test 7:
    Test addowner function with invalid user id.
    Will raise InputError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''

    token1 = http_register(url, 'Bob')['token']
    u_id2 = http_register(url, 'Tim')['u_id']
    if is_public:
        channel_id = http_create_public_channel(url, token1, 'Channel1')
    else:
        channel_id = http_create_private_channel(url, token1, 'Channel1')

    u_id2 *= 2
    response = requests.post(url + '/channel/addowner', json={'token': token1, \
        'channel_id': channel_id, 'u_id': u_id2})
    assert response.status_code == 400


def test_addowner_invalid_uid_pub(url):
    '''
    Test 8:
    Test addowner function,
    with invalid user id for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_invalid_uid(True, url)


def test_addowner_invalid_uid_priv(url):
    '''
    Test 9:
    Test addowner function,
    with invalid user id for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_invalid_uid(False, url)

def addowner_uid_is_owner(is_public, url):
    '''
    Test 10:
    Test addowner function when user is already an owner.
    Will raise InputError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''

    u_id, token = http_register(url, 'Bob').values()
    if is_public:
        channel_id = http_create_public_channel(url, token, 'Channel1')
    else:
        channel_id = http_create_private_channel(url, token, 'Channel1')

    response = requests.post(url + '/channel/addowner', json={'token': token, \
        'channel_id': channel_id, 'u_id': u_id})
    assert response.status_code == 400


def test_addowner_uid_is_owner_pub(url):
    '''
    Test 11:
    Test addowner function,
    user is already owner for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_uid_is_owner(True, url)


def test_addowner_uid_is_owner_priv(url):
    '''
    Test 12:
    Test addowner function,
    user is already owner for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_uid_is_owner(False, url)


def addowner_access_error(is_public, url):
    '''
    Test 13:
    Test addowner function when user not an owner of channel and flockr.
    Will raise AccessError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''

    http_register(url, 'Owner') # claim u_id : 0
    token1 = http_register(url, 'Bob')['token']
    u_id2, token2 = http_register(url, 'Tim').values()

    if is_public:
        channel_id = http_create_public_channel(url, token1, 'Channel1')
    else:
        channel_id = http_create_private_channel(url, token1, 'Channel1')

    response = requests.post(url + '/channel/addowner', json={'token': token2, \
        'channel_id': channel_id, 'u_id': u_id2})
    assert response.status_code == 400


def test_addowner_access_error_pub(url):
    '''
    Test 14:
    Test addowner function,
    user not channel and flockr owner public channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_access_error(True, url)


def test_addowner_access_error_priv(url):
    '''
    Test 15:
    Test addowner function,
    user not channel and flockr owner private channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_access_error(False, url)


def addowner_valid(is_public, url):
    '''
    Test 16:
    Test addowner function with valid inputs is added correctly
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''

    token1 = http_register(url, 'Bob')['token']
    u_id2, token2 = http_register(url, 'Tim').values()

    if is_public:
        channel_id = http_create_public_channel(url, token1, 'Channel1')
    else:
        channel_id = http_create_private_channel(url, token1, 'Channel1')

    requests.post(url + '/channel/invite', json={'token': token1, \
        'channel_id': channel_id, 'u_id': u_id2})
    requests.post(url + '/channel/addowner', json={'token':token1, \
        'channel_id':channel_id, 'u_id':u_id2})

    details = requests.get(url + '/channel/details', params={'token': token2, \
        'channel_id': channel_id})
    owners = json.loads(details.text)['owner_members']

    for owner in owners:
        if owner['u_id'] == u_id2:
            break
    else:
        # assert False, f"u_id({u_id2}) not in channel({channel_id})"
        assert False


def test_addowner_valid_pub(url):
    '''
    Test 17:
    Test addowner function,
    with valid input for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_valid(True, url)


def test_addowner_valid_priv(url):
    '''
    Test 18:
    Test addowner function,
    with valid input for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_valid(False, url)


# owner is added if the authorised user is a flockr owner
# authorised user is not part of the channel
# tests both public and private channels
def addowner_owns_flockr(is_public, url):
    '''
    Test 19:
    Test addowner function with owner user id is correctly added.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''

    token0 = http_register(url, 'Owner')['token']
    token1 = http_register(url, 'Bob')['token']
    u_id2 = http_register(url, 'Tim')['u_id']

    if is_public:
        c_id = http_create_public_channel(url, token1, 'Channel1')
    else:
        c_id = http_create_private_channel(url, token1, 'Channel1')

    requests.post(url + '/channel/invite', json={'token': token1, \
        'channel_id': c_id, 'u_id': u_id2})
    requests.post(url + '/channel/addowner', json={'token': token0, \
        'channel_id': c_id, 'u_id': u_id2})

    details = requests.get(url + '/channel/details', params={'token': token1, \
        'channel_id': c_id})
    owners = json.loads(details.text)['owner_members']

    for owner in owners:
        if owner['u_id'] == u_id2:
            break
    else:
        # assert False, f"u_id({u_id2} not added""
        assert False



def test_addowner_owns_flockr_pub(url):
    '''
    Test 20:
    Test addowner function,
    flockr owner adds an owner for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_owns_flockr(True, url)


def test_addowner_owns_flockr_priv(url):
    '''
    Test 21:
    Test addowner function,
    flockr owner adds an owner for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_owns_flockr(False, url)


##########################################################################################
###                        ✨ ✨ ✨ CHANNEL_REMOVEOWNER TESTS ✨ ✨ ✨                     ###
##########################################################################################

# invalid token, raise AccessError
def removeowner_invalid_token(is_public, url):
    '''
    Test 1:
    Test removeowner function with invalid token.
    Will raise AccessError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''

    u_id1, token1 = http_register(url, 'Bob').values()
    token2 = http_register(url, 'Tim')['token']

    if is_public:
        channel_id = http_create_public_channel(url, token1, 'Channel1')
    else:
        channel_id = http_create_private_channel(url, token1, 'Channel1')

    response = requests.post(url + '/channel/removeowner', json={'token': token2 * 2, \
        'channel_id': channel_id, 'u_id': u_id1})
    assert response.status_code == 400



def test_removeowner_invalid_token_pub(url):
    '''
    Test 2:
    Test removeowner function,
    with invalid token for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_invalid_token(True, url)


def test_removeowner_invalid_token_priv(url):
    '''
    Test 3:
    Test removeowner function,
    with invalid token for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_invalid_token(False, url)


# invalid channel_id, raise InputError
def removeowner_invalid_channel_id(is_public, url):
    '''
    Test 4:
    Test removeowner function with invalid channel id.
    Will raise InputError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''

    u_id, token = http_register(url, 'Bob').values()
    u_id1, token1 = http_register(url, 'Tim').values()

    if is_public:
        channel_id = http_create_public_channel(url, token, 'Channel1')
    else:
        channel_id = http_create_private_channel(url, token, 'Channel1')

    requests.post(url + '/channel/invite', json={'token': token, \
        'channel_id': channel_id, 'u_id': u_id1})
    requests.post(url + '/channel/addowner', json={'token': token, \
        'channel_id': channel_id, 'u_id': u_id1})

    response = requests.post(url + '/channel/removeowner', json={'token': token1, \
        'channel_id': channel_id + 999, 'u_id': u_id})
    assert response.status_code == 400


def test_removeowner_invalid_channel_id_pub(url):
    '''
    Test 5:
    Test removeowner function,
    with invalid channel id for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_invalid_channel_id(True, url)


def test_removeowner_invalid_channel_id_priv(url):
    '''
    Test 6:
    Test removeowner function,
    with invalid channel id for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_invalid_channel_id(False, url)


def removeowner_invalid_uid(is_public, url):
    '''
    Test 7:
    Test removeowner function with invalid user id.
    Will raise InputError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''

    token1 = http_register(url, 'Bob')['token']
    u_id2 = http_register(url, 'Tim')['u_id']

    if is_public:
        channel_id = http_create_public_channel(url, token1, 'Channel1')
    else:
        channel_id = http_create_private_channel(url, token1, 'Channel1')

    u_id2 *= 2

    response = requests.post(url + '/channel/removeowner', json={'token': token1, \
        'channel_id': channel_id, 'u_id': u_id2})
    assert response.status_code == 400


def test_removeowner_invalid_uid_pub(url):
    '''
    Test 8:
    Test removeowner function,
    with invalid user id for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_invalid_uid(True, url)


def test_removeowner_invalid_uid_priv(url):
    '''
    Test 9:
    Test removeowner function,
    with invalid user id for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_invalid_uid(False, url)


def removeowner_uid_is_not_owner(is_public, url):
    '''
    Test 10
    Test removeowner function when user id not an owner.
    Will raise InputError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''

    http_register(url, 'flockrowner')
    token1 = http_register(url, 'Bob')['token']
    u_id2 = http_register(url, 'Tim')['u_id']

    if is_public:
        channel_id = http_create_public_channel(url, token1, 'Channel1')
    else:
        channel_id = http_create_private_channel(url, token1, 'Channel1')

    requests.post(url + '/channel/invite', json={'token': token1, \
        'channel_id': channel_id, 'u_id': u_id2})

    response = requests.post(url + '/channel/removeowner', json={'token': token1, \
        'channel_id': channel_id, 'u_id': u_id2})
    assert response.status_code == 400


def test_removeowner_uid_is_not_owner_pub(url):
    '''
    Test 11:
    Test removeowner function,
    user id not an owner for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_uid_is_not_owner(True, url)


def test_removeowner_uid_is_not_owner_priv(url):
    '''
    Test 12:
    Test removeowner function,
    user id not an owner for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_uid_is_not_owner(False, url)


def removeowner_access_error(is_public, url):
    '''
    Test 13:
    Test removeowner function when user not owner of channel and flockr.
    Will raise AccessError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''

    http_register(url, 'Owner')# claim u_id : 0
    u_id1, token1 = http_register(url, 'Bob').values()
    token2 = http_register(url, 'Tim')['token']

    if is_public:
        channel_id = http_create_public_channel(url, token1, 'Channel1')
    else:
        channel_id = http_create_private_channel(url, token1, 'Channel1')

    response = requests.post(url + '/channel/removeowner', json={'token': token2, \
        'channel_id': channel_id, 'u_id': u_id1})
    assert response.status_code == 400


def test_removeowner_access_error_pub(url):
    '''
    Test 14:
    Test removeowner function,
    user does not own channel and flockr for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_access_error(True, url)


def test_removeowner_access_error_priv(url):
    '''
    Test 15:
    Test removeowner function,
    user does not own channel and flockr for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_access_error(False, url)


# owner is removed for both public and private channels
def removeowner_valid(is_public, url):
    '''
    Test 16:
    Test removeowner function with valid inputs is added correctly.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''

    u_id1, token1 = http_register(url, 'Bob').values()
    u_id2, token2 = http_register(url, 'Tim').values()

    if is_public:
        channel_id = http_create_public_channel(url, token1, 'Channel1')
    else:
        channel_id = http_create_private_channel(url, token1, 'Channel1')

    requests.post(url + '/channel/invite', json={'token': token1, \
        'channel_id': channel_id, 'u_id': u_id2})
    requests.post(url + '/channel/addowner', json={'token': token1, \
        'channel_id': channel_id, 'u_id': u_id2})

    details = requests.get(url + '/channel/details', params={'token': token2, \
        'channel_id': channel_id})
    owners = json.loads(details.text)['owner_members']
    initial_count = len(owners)

    requests.post(url + '/channel/removeowner', json={'token': token2, \
        'channel_id': channel_id, 'u_id': u_id1})
    details = requests.get(url + '/channel/details', params={'token': token2, \
        'channel_id': channel_id})
    owners = json.loads(details.text)['owner_members']
    final_count = len(owners)

    assert final_count + 1 == initial_count


def test_removeowner_pub(url):
    '''
    Test 17:
    Test removeowner function,
    with valid inputs for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_valid(True, url)


def test_removeowner_priv(url):
    '''
    Test 18:
    Test removeowner function,
    with valid inputs for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_valid(False, url)


def removeowner_owns_flockr(is_public, url):
    '''
    Test 19:
    Test removeowner function when user owns flockr but not in channel
    Checks if a channel owner is removed by the flockr owner correctly
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''

    http_register(url, 'Ownner')
    u_id1, token1 = http_register(url, 'Bob').values()
    u_id2, token2 = http_register(url, 'Tim').values()

    if is_public:
        channel_id = http_create_public_channel(url, token1, 'Channel1')
    else:
        channel_id = http_create_private_channel(url, token1, 'Channel1')

    requests.post(url + '/channel/invite', json={'token': token1, \
        'channel_id': channel_id, 'u_id': u_id2})
    requests.post(url + '/channel/addowner', json={'token': token1, \
        'channel_id': channel_id, 'u_id': u_id2})

    details = requests.get(url + '/channel/details', params={'token': token2, \
        'channel_id': channel_id})
    owners = json.loads(details.text)['owner_members']
    initial_count = len(owners)

    requests.post(url + '/channel/removeowner', json={'token': token2, \
        'channel_id': channel_id, 'u_id': u_id1})
    details = requests.get(url + '/channel/details', params={'token': token2, \
        'channel_id': channel_id})
    owners = json.loads(details.text)['owner_members']
    final_count = len(owners)

    assert final_count + 1 == initial_count


def test_removeowner_owns_flockr_pub(url):
    '''
    Test 20:
    Test removeowner function,
    when user owns flockr but not in channel removes another channel owner in a public channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_owns_flockr(True, url)


def test_removeowner_owns_flockr_priv(url):
    '''
    Test 21:
    Test removeowner function,
    when user owns flockr but not in channel removes another channel owner in a private channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_owns_flockr(False, url)
