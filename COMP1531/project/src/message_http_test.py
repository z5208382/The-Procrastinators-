from time import sleep
import requests
from message import *
from channel import *
from helper_server_tests import *
from other import clear
from server import *
from message_test import message_timestamp_compare

##########################################################################################
###                                    TEST SERVER URL                                 ###
##########################################################################################

def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")


##########################################################################################
###                                 MESSAGE_PIN TESTS                                  ###
##########################################################################################

def test_http_message_pin_invalid_message_id(url):
    '''
    Test 1: in message where message_id is invalid
    Expect InputError
    '''
    clear()
    user, _, channel_id = http_load_message(url, 'channel').values()

    parameters = {
        'token': user['token'],
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.ok
    message_id = message.json()['messages'][0]['message_id']

    data = {'token': user['token'], 'message_id': message_id + 100}
    response = requests.post(url + 'message/pin', json=data)
    assert response.status_code == 400

def test_http_message_pin_message_already_pinned(url):
    '''
    Test 2: Pin message where message is already pinned
    Expect InputError
    '''
    clear()
    user, _, channel_id = http_load_message(url, 'channel').values()

    parameters = {
        'token': user['token'],
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.ok
    message_id = message.json()['messages'][0]['message_id']

    data = {'token': user['token'], 'message_id': message_id}

    response = requests.post(url + 'message/pin', json=data)
    assert response.ok

    response = requests.post(url + 'message/pin', json=data)
    assert response.status_code == 400

def test_message_pin_invalid_token(url):
    '''
    Test 3: Pin message when token is invalid
    Expect AccessError
    '''
    clear()
    user, _, channel_id = http_load_message(url, 'channel').values()
    parameters = {
        'token': user['token'],
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.ok
    message_id = message.json()['messages'][0]['message_id']

    data = {'token': user['token'] + 'bad_token', 'message_id': message_id}

    response = requests.post(url + 'message/pin', json=data)
    assert response.status_code == 400

def test_http_message_pin_user_not_in_channel(url):
    '''
    Test 4: User who is not in the channel tries to pin a message
    Expect AccessError
    '''
    clear()
    user, _, channel_id = http_load_message(url, 'channel').values()
    parameters = {
        'token': user['token'],
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.ok
    message_id = message.json()['messages'][2]['message_id']
    token = http_register(url, 'Bob')['token']

    data = {'token': token, 'message_id': message_id}
    response = requests.post(url + 'message/pin', json=data)
    assert response.status_code == 400

def test_http_message_pin_user_not_channel_owner(url):
    '''
    Test 5: User who is in channel but not a channel owner tries to pin a message
    Expect AccessError
    '''
    clear()
    user, _, channel_id = http_load_message(url, 'channel').values()
    parameters = {
        'token': user['token'],
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.ok
    message_id = message.json()['messages'][2]['message_id']
    token = http_register(url, 'Bob')['token']

    response = requests.post(url + '/channel/join', json={'token': token, \
        'channel_id': channel_id})

    data = {'token': token, 'message_id': message_id}
    response = requests.post(url + 'message/pin', json=data)
    assert response.status_code == 400


def test_http_message_pin_user_flockr_owner_not_in_channel(url):
    '''
    Test 6: User who is not in channel but is a global owner tries to pin message
    Expect AccessError
    '''
    clear()
    user, _, channel_id = http_load_message(url, 'channel').values()
    parameters = {
        'token': user['token'],
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.ok
    message_id = message.json()['messages'][2]['message_id']

    data1 = {
        'token': user['token'],
        'channel_id': channel_id
    }
    response = requests.post(url + 'channel/leave', json=data1)
    assert response.ok

    data2 = {'token': user['token'], 'message_id': message_id}
    response = requests.post(url + 'message/pin', json=data2)
    assert response.status_code == 400

def test_http_message_pin_user_flockr_owner_member_in_channel(url):
    '''
    Test 7: User who is in channel as a normal member but is a global owner tries to pin message
    This should work
    '''
    clear()
    user, channel_id, _ = http_load_message(url, 'channel').values()
    parameters = {
        'token': user['token'],
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + '/channel/messages', params=parameters)
    assert message.ok
    message_id = message.json()['messages'][2]['message_id']

    u_id, token = http_register(url, 'Bob').values()

    response = requests.post(url + '/channel/join', json={'token': token, 'channel_id': channel_id})
    assert response.ok

    response = requests.post(url + 'channel/addowner', json={'token': user['token'], \
        'channel_id': channel_id, 'u_id': u_id})
    assert response.ok

    response = requests.post(url + 'channel/removeowner', json={'token': token, \
        'channel_id': channel_id, 'u_id': user['u_id']})
    assert response.ok

    data = {'token': user['token'], 'message_id': message_id}
    response = requests.post(url + 'message/pin', json=data)
    assert response.ok

    messages = requests.get(url + 'channel/messages', params=parameters)

    assert messages.json()['messages'][2]['is_pinned']


def test_http_message_pin_user_channel_owner(url):
    '''
    User who is a channel owner tries to pin message
    This should work
    '''
    clear()
    user, channel_id, _ = http_load_message(url, 'channel').values()

    u_id, token = http_register(url, 'Bob').values()

    response = requests.post(url + 'channel/join', json={'token': token, \
        'channel_id': channel_id})
    assert response.ok
    response = requests.post(url + 'channel/addowner', json={'token': user['token'], \
        'channel_id': channel_id, 'u_id': u_id})
    assert response.ok
    parameters = {
        'token': token,
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.ok

    message_id = message.json()['messages'][2]['message_id']
    data = {'token': token, 'message_id': message_id}
    requests.post(url + 'message/pin', json=data)

    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.json()['messages'][2]['is_pinned']


##########################################################################################
###                                 MESSAGE_UNPIN TESTS                                ###
##########################################################################################

def test_http_message_unpin_invalid_message_id(url):
    '''
    Test 1: Unpin message where message_id is invalid
    Expect InputError
    '''
    clear()
    user, _, channel_id = http_load_message(url, 'channel').values()

    parameters = {
        'token': user['token'],
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.ok
    message_id = message.json()['messages'][0]['message_id']

    data = {'token': user['token'], 'message_id': message_id}
    response = requests.post(url + 'message/pin', json=data)
    assert response.ok

    data = {'token': user['token'], 'message_id': message_id + 100}
    response = requests.post(url + 'message/unpin', json=data)
    assert response.status_code == 400


def test_http_message_unpin_message_already_unpinned(url):
    '''
    Test 2: Unpin message where message is already unpinned
    Expect InputError
    '''
    clear()
    user, _, channel_id = http_load_message(url, 'channel').values()

    parameters = {
        'token': user['token'],
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.ok
    message_id = message.json()['messages'][0]['message_id']

    data = {'token': user['token'], 'message_id': message_id}

    response = requests.post(url + 'message/pin', json=data)
    assert response.ok

    response = requests.post(url + 'message/unpin', json=data)
    assert response.ok

    response = requests.post(url + 'message/unpin', json=data)
    assert response.status_code == 400

def test_http_message_unpin_invalid_token(url):
    '''
    Test 3: Unpin message when token is invalid
    Expect AccessError
    '''
    clear()
    user, _, channel_id = http_load_message(url, 'channel').values()

    parameters = {
        'token': user['token'],
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.ok
    message_id = message.json()['messages'][0]['message_id']

    data = {'token': user['token'], 'message_id': message_id}
    response = requests.post(url + 'message/pin', json=data)
    assert response.ok

    data = {'token': user['token'] + 'bad_token', 'message_id': message_id}
    response = requests.post(url + 'message/unpin', json=data)
    assert response.status_code == 400


def test_http_message_unpin_user_not_in_channel(url):
    '''
    Test 4: User who is not in the channel tries to unpin a message
    Expect AccessError
    '''
    clear()
    user, _, channel_id = http_load_message(url, 'channel').values()
    parameters = {
        'token': user['token'],
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.ok
    message_id = message.json()['messages'][2]['message_id']

    data = {'token': user['token'], 'message_id': message_id}
    response = requests.post(url + 'message/pin', json=data)
    assert response.ok

    token = http_register(url, 'Bob')['token']
    data = {'token': token, 'message_id': message_id}
    response = requests.post(url + 'message/unpin', json=data)
    assert response.status_code == 400


def test_http_message_unpin_user_not_channel_owner(url):
    '''
    Test 5: User who is in channel but not a channel owner tries to unpin a message
    Expect AccessError
    '''
    clear()
    user, channel_id, _ = http_load_message(url, 'channel').values()
    parameters = {
        'token': user['token'],
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.ok
    message_id = message.json()['messages'][2]['message_id']

    data = {'token': user['token'], 'message_id': message_id}
    response = requests.post(url + 'message/pin', json=data)
    assert response.ok

    token = http_register(url, 'Bob')['token']

    data = {'token': token, 'channel_id': channel_id}
    response = requests.post(url + 'channel/join', json=data)
    assert response.ok

    data = {'token': token, 'message_id': message_id}
    response = requests.post(url + 'message/unpin', json=data)
    assert response.status_code == 400


def test_http_message_unpin_user_flockr_owner_not_in_channel(url):
    '''
    Test 6: User who is not in channel but is a global owner tries to unpin message
    Expect AccessError
    '''
    clear()
    user, channel_id, _ = http_load_message(url, 'channel').values()
    parameters = {
        'token': user['token'],
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.ok
    message_id = message.json()['messages'][2]['message_id']

    data = {'token': user['token'], 'message_id': message_id}
    response = requests.post(url + 'message/pin', json=data)
    assert response.ok

    data = {'token': user['token'], 'channel_id': channel_id}
    response = requests.post(url + 'channel/leave', json=data)
    assert response.ok

    data = {'token': user['token'], 'message_id': message_id}
    response = requests.post(url + 'message/unpin', json=data)
    assert response.status_code == 400


def test_http_message_unpin_user_flockr_owner_member_in_channel(url):
    '''
    Test 7: User who is in channel as a normal member but is a global owner tries to unpin message
    This should work
    '''
    clear()
    user, channel_id, _ = http_load_message(url, 'channel').values()
    parameters = {
        'token': user['token'],
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.ok
    message_id = message.json()['messages'][2]['message_id']

    data = {'token': user['token'], 'message_id': message_id}
    response = requests.post(url + 'message/pin', json=data)
    assert response.ok

    u_id, token = http_register(url, 'Bob').values()

    response = requests.post(url + 'channel/join', json={'token': token, \
        'channel_id': channel_id})
    assert response.ok

    response = requests.post(url + 'channel/addowner', json={'token': user['token'], \
        'channel_id': channel_id, 'u_id': u_id})
    assert response.ok

    response = requests.post(url + 'channel/removeowner', json={'token': token, \
        'channel_id': channel_id, 'u_id': user['u_id']})
    assert response.ok

    data = {'token': user['token'], 'message_id': message_id}
    response = requests.post(url + 'message/unpin', json=data)
    assert response.ok

    message = requests.get(url + 'channel/messages', params=parameters)
    assert not message.json()['messages'][2]['is_pinned']


def test_http_message_unpin_user_channel_owner(url):
    '''
    Test 8: User who is a channel owner tries to unpin message
    This should work
    '''
    clear()
    user, channel_id, _ = http_load_message(url, 'channel').values()
    parameters = {
        'token': user['token'],
        'channel_id': channel_id,
        'start': 0
    }
    message = requests.get(url + 'channel/messages', params=parameters)
    assert message.ok
    message_id = message.json()['messages'][2]['message_id']

    data = {'token': user['token'], 'message_id': message_id}
    response = requests.post(url + 'message/pin', json=data)
    assert response.ok

    u_id, token = http_register(url, 'Bob').values()

    response = requests.post(url + 'channel/join', json={'token': token, \
        'channel_id': channel_id})
    assert response.ok

    response = requests.post(url + 'channel/addowner', json={'token': user['token'], \
        'channel_id': channel_id, 'u_id': u_id})
    assert response.ok

    data = {'token': token, 'message_id': message_id}
    response = requests.post(url + 'message/unpin', json=data)
    assert response.ok

    message = requests.get(url + 'channel/messages', params=parameters)
    assert not message.json()['messages'][2]['is_pinned']

##########################################################################################
###                                 MESSAGE_SEND TESTS                                 ###
##########################################################################################

def test_http_send_invalid_token(url):
    '''
    Test 1: given an invalid token
    Access Error is raised
    '''
    clear()
    token = http_register(url, "Dave")['token']
    channel_id = http_create_public_channel(url, token, '1')
    requests.post(f"{url}/auth/logout", \
        json={
            'token' : token
        })
    resp = requests.post(f"{url}/message/send", \
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    assert not resp.ok

def test_http_send_input_error(url):
    '''
    Test 2: message is more than 1000 characters
    InputError is raised
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    resp = requests.post(f"{url}/message/send", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'message' : "a"*1001
        })
    assert not resp.ok

def test_http_send_access_error(url):
    '''
    Test 3: authorised user is not in the channel they are trying to post to
    AccessError is raised
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    token2 = http_register(url, "Lucy")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    resp = requests.post(f"{url}/message/send", \
        json={
            'token' : token2,
            'channel_id' : channel_id,
            'message' : "who's free today"
        })
    assert not resp.ok

def test_http_send_access_error_flockr_owner(url):
    '''
    Test 4: authorised user is a flockr owner
    and tries to post to a channel they have not joined
    AccessError is raised
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    token2 = http_register(url, "Lucy")['token']
    channel_id = http_create_public_channel(url, token2, '1')
    resp = requests.post(f"{url}/message/send", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'message' : "who's free today"
        })
    assert not resp.ok

def test_http_send_small(url):
    '''
    Test 5: send small message
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/message/send", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'message' : "who's free today"
        })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id,
            'start' : 0
        })
    messages_list = temp.json()['messages']
    assert len(messages_list) == 1
    assert messages_list[0]['message'] == "who's free today"

def test_http_send_1000_characters(url):
    '''
    Test 6: message is 1000 characters long
    InputError should not be raised
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/message/send", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'message' : "a"*1000
        })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id,
            'start' : 0
        })
    messages_list = temp.json()['messages']
    assert len(messages_list) == 1
    assert messages_list[0]['message'] == "a"*1000

def test_http_send_empty_message(url):
    '''
    Test 7: message is empty, should not send
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/message/send", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'message' : ""
        })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id,
            'start' : 0
        })
    messages_list = temp.json()['messages']
    assert len(messages_list) == 0

def test_http_send_multiple_messages(url):
    '''
    Test 8: send multiple messages by different users
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    token2 = http_register(url, "Sarah")['token']
    token3 = http_register(url, "Selina")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id
        })
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token3,
            'channel_id' : channel_id
        })
    requests.post(f"{url}/message/send", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'message' : "hello"
        })
    requests.post(f"{url}/message/send", \
        json={
            'token' : token2,
            'channel_id' : channel_id,
            'message' : "hi"
        })
    requests.post(f"{url}/message/send", \
        json={
            'token' : token2,
            'channel_id' : channel_id,
            'message' : "goodbye"
        })
    requests.post(f"{url}/message/send", \
        json={
            'token' : token3,
            'channel_id' : channel_id,
            'message' : "bye everyone"
        })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id,
            'start' : 0
        })
    messages_list = temp.json()['messages']
    assert len(messages_list) == 4
    assert messages_list[0]['message'] == "bye everyone"
    assert messages_list[1]['message'] == "goodbye"
    assert messages_list[2]['message'] == "hi"
    assert messages_list[3]['message'] == "hello"

##########################################################################################
###                                 MESSAGE_REMOVE TESTS                               ###
##########################################################################################

def test_remove_invalid_token(url):
    '''
    Test 1: given an invalid token
    AccessError is raised
    '''
    clear()
    token = http_register(url, "Dave")['token']
    channel_id = http_create_public_channel(url, token, '1')
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    message_id = temp.json()['message_id']
    requests.post(f"{url}/auth/logout", \
        json={
            'token' : token
        })
    resp = requests.delete(f"{url}/message/remove", \
        json={
            'token' : token,
            'message_id' : message_id
       })
    assert not resp.ok

def test_remove_input_error1(url):
    '''
    Test 2: message_id does not exist
    InputError is raised
    '''
    clear()
    token = http_register(url, "Dave")['token']
    channel_id = http_create_public_channel(url, token, '1')
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    message_id = temp.json()['message_id']
    resp = requests.delete(f"{url}/message/remove", \
        json={
            'token' : token,
            'message_id' : message_id + 2
       })
    assert not resp.ok

def test_remove_input_error2(url):
    '''
    Test 3: message_id no longer exists
    InputError is raised
    '''
    clear()
    token = http_register(url, "Dave")['token']
    channel_id = http_create_public_channel(url, token, '1')
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    message_id = temp.json()['message_id']
    requests.delete(f"{url}/message/remove", \
        json={
            'token' : token,
            'message_id' : message_id
       })
    resp = requests.delete(f"{url}/message/remove", \
        json={
            'token' : token,
            'message_id' : message_id
       })
    assert not resp.ok

def test_remove_access_error(url):
    '''
    Test 4: authorised user did not send the message
    and is not an owner of the channel or flockr
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    token2 = http_register(url, "Sarah")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id
        })
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    message_id = temp.json()['message_id']
    resp = requests.delete(f"{url}/message/remove", \
        json={
            'token' : token2,
            'message_id' : message_id
       })
    assert not resp.ok

def test_remove_user_sent(url):
    '''
    Test 5: authorised user is removing a message they sent
    user is not an owner of the channel or a flockr owner
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    token2 = http_register(url, "Sarah")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id
        })
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token2,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    message_id = temp.json()['message_id']
    requests.delete(f"{url}/message/remove", \
        json={
            'token' : token2,
            'message_id' : message_id
       })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id,
            'start' : 0
        })
    messages_list = temp.json()['messages']
    assert len(messages_list) == 0

def test_remove_channel_owner(url):
    '''
    Test 6: authorised user is a channel owner but not a flockr owner
    user is a removing a message they did not send
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    u_id2, token2 = http_register(url, "Sarah").values()
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id
        })
    requests.post(f"{url}/channel/addowner", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'u_id' : u_id2
        })
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    message_id = temp.json()['message_id']
    requests.delete(f"{url}/message/remove", \
        json={
            'token' : token2,
            'message_id' : message_id
       })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id,
            'start' : 0
        })
    messages_list = temp.json()['messages']
    assert len(messages_list) == 0

def test_remove_flockr_owner(url):
    '''
    Test 7: authorised user is a flockr owner
    user is removing a message they did not send
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    token2 = http_register(url, "Sarah")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id
        })
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token2,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    message_id = temp.json()['message_id']
    requests.delete(f"{url}/message/remove", \
        json={
            'token' : token1,
            'message_id' : message_id
       })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id,
            'start' : 0
        })
    messages_list = temp.json()['messages']
    assert len(messages_list) == 0

def test_remove_small(url):
    '''
    Test 8: test function removes the correct message
    '''
    clear()
    token = http_register(url, "Dave")['token']
    channel_id = http_create_public_channel(url, token, '1')
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    message_id1 = temp.json()['message_id']
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : 'hello everyone'
        })
    message_id2 = temp.json()['message_id']
    requests.delete(f"{url}/message/remove", \
        json={
            'token' : token,
            'message_id' : message_id1
       })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token,
            'channel_id' : channel_id,
            'start' : 0
        })
    messages_list = temp.json()['messages']
    assert len(messages_list) == 1
    assert messages_list[0]['message'] == 'hello everyone'
    requests.delete(f"{url}/message/remove", \
        json={
            'token' : token,
            'message_id' : message_id2
       })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token,
            'channel_id' : channel_id,
            'start' : 0
        })
    messages_list = temp.json()['messages']
    assert len(messages_list) == 0

def test_remove_multiple_channels(url):
    '''
    Test 9: removing a message when multiple channels have the same message
    '''
    clear()
    token = http_register(url, "Dave")['token']
    channel_id1 = http_create_public_channel(url, token, '1')
    channel_id2 = http_create_public_channel(url, token, '2')
    channel_id3 = http_create_public_channel(url, token, '3')
    requests.post(f"{url}/message/send", \
        json={
            'token' : token,
            'channel_id' : channel_id1,
            'message' : 'hi'
        })
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token,
            'channel_id' : channel_id2,
            'message' : 'hi'
        })
    requests.post(f"{url}/message/send", \
        json={
            'token' : token,
            'channel_id' : channel_id3,
            'message' : 'hi'
        })
    message_id2 = temp.json()['message_id']
    requests.delete(f"{url}/message/remove", \
        json={
            'token' : token,
            'message_id' : message_id2
       })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token,
            'channel_id' : channel_id1,
            'start' : 0
        })
    messages_list1 = temp.json()['messages']
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token,
            'channel_id' : channel_id2,
            'start' : 0
        })
    messages_list2 = temp.json()['messages']
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token,
            'channel_id' : channel_id3,
            'start' : 0
        })
    messages_list3 = temp.json()['messages']
    assert len(messages_list1) == 1
    assert len(messages_list2) == 0
    assert len(messages_list3) == 1

def test_remove_user_leaves(url):
    '''
    Test 10: user is no longer in a channel and removes their old message from that channel
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    token2 = http_register(url, "Sarah")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id
        })
    requests.post(f"{url}/message/send", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token2,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    message_id = temp.json()['message_id']
    requests.post(f"{url}/channel/leave", \
        json={
        'token' : token2,
        'channel_id' : channel_id
        })
    requests.delete(f"{url}/message/remove", \
        json={
            'token' : token1,
            'message_id' : message_id
       })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id,
            'start' : 0
        })
    messages_list = temp.json()['messages']
    assert len(messages_list) == 1

##########################################################################################
###                                 MESSAGE_EDIT TESTS                                 ###
##########################################################################################

def test_http_edit_invalid_token(url):
    '''
    Test 1: given an invalid token
    AccessError is raised
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    data = requests.post(f"{url}/message/send", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    message_id = data.json()['message_id']
    requests.post(f"{url}/auth/logout", \
        json={
            'token' : token1
        })
    resp = requests.put(f"{url}/message/edit", \
        json={
        'token' : token1,
        'message_id' : message_id,
        'message' : 'hello'
    })
    assert not resp.ok

def test_http_edit_removed_message(url):
    '''
    Test 2: edit when the message is already removed
    AccessError is raised
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    data = requests.post(f"{url}/message/send", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'message' : "hi"
        })
    message_id = data.json()['message_id']
    requests.delete(f"{url}/message/remove", \
        json={
            'token' : token1,
            'message_id' : message_id
        })
    resp = requests.put(f"{url}/message/edit", \
        json={
            'token' : token1,
            'message_id' : message_id,
            'message' : 'hello'
        })
    assert not resp.ok

def test_http_edit_user_sent(url):
    '''
    Test 3: user who wrote the message is able to edit
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    token2 = http_register(url, "Stacy")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id
        })
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token2,
            'channel_id' : channel_id,
            'message' :'hi'
        })
    message_id = temp.json()['message_id']
    resp = requests.put(f"{url}/message/edit", \
        json={
            'token' : token2,
            'message_id' : message_id,
            'message': "hey everyone"
        })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id,
            'start' : 0
        })
    messages_list = temp.json()['messages']
    assert resp.ok
    assert messages_list[0]['message'] == 'hey everyone'

def test_http_edit_channel_owner(url):
    '''
    Test 4: authorsied user is editing message
    user is channel owner but not flockr owner
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    u_id2, token2 = http_register(url, "Sarah").values()
    token3 = http_register(url, "Lucy")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id
        })
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token3,
            'channel_id' : channel_id
        })
    requests.post(f"{url}/channel/addowner", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'u_id' : u_id2
        })
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token3,
            'channel_id' : channel_id,
            'message' : "hi"
        })
    message_id = temp.json()['message_id']
    resp = requests.put(f"{url}/message/edit", \
        json={
            'token' : token2,
            'message_id' : message_id,
            'message' : "hey everyone"
        })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id,
            'start' : 0
        })
    messages_list = temp.json()['messages']
    assert resp.ok
    assert messages_list[0]['message'] == 'hey everyone'

def test_http_edit_flockr_owner(url):
    '''
    Test 5: authorsied user is editing message
    message written by member of channel that is not owner of channel, or flock owner
    user is flockr owner
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    u_id2, token2 = http_register(url, "Sarah").values()
    token3 = http_register(url, "Lucy")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id
        })
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token3,
            'channel_id' : channel_id
        })
    requests.post(f"{url}/channel/addowner", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'u_id' : u_id2
        })
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token2,
            'channel_id' : channel_id,
            'message' : "hi"
        })
    message_id = temp.json()['message_id']
    resp = requests.put(f"{url}/message/edit", \
        json={
            'token' : token1,
            'message_id' : message_id,
            'message' : "Howdy"
        })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id,
            'start' : 0
        })
    messages_list = temp.json()['messages']
    assert resp.ok
    assert messages_list[0]['message'] == "Howdy"

def test_http_edit_empty_message(url):
    '''
    Test 6: user who wrote the message edits to an empty message
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    token2 = http_register(url, "Lucy")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id
        })
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token2,
            'channel_id' : channel_id,
            'message' : "hi"
        })
    message_id = temp.json()['message_id']
    resp = requests.put(f"{url}/message/edit", \
        json={
            'token' : token1,
            'message_id' : message_id,
            'message' : ""
        })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id,
            'start' : 0
        })
    messages_list = temp.json()['messages']
    assert len(messages_list) == 0
    assert resp.ok

def test_http_edit_multiple_message(url):
    '''
    Test 7: authorsied user is editing message they sent
    user is editing multiple messages
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    token2 = http_register(url, "Lucy")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id
        })
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token2,
            'channel_id' : channel_id,
            'message' : "hi"
        })
    message_id1 = temp.json()['message_id']
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token2,
            'channel_id' : channel_id,
            'message' : "how is everyone"
        })
    message_id2 = temp.json()['message_id']
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token2,
            'channel_id' : channel_id,
            'message' : "who's free today"
        })
    message_id3 = temp.json()['message_id']
    requests.put(f"{url}/message/edit", \
        json={
            'token' : token1,
            'message_id' : message_id1,
            'message' : "hey everyone"
        })
    requests.put(f"{url}/message/edit", \
        json={
            'token' : token1,
            'message_id' : message_id2,
            'message' : "how y'all doing"
        })
    requests.put(f"{url}/message/edit", \
        json={
            'token' : token1,
            'message_id' : message_id3,
            'message' : ""
        })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id,
            'start' : 0
        })
    messages_list = temp.json()['messages']
    assert len(messages_list) == 2
    assert messages_list[0]['message'] == "how y'all doing"
    assert messages_list[1]['message'] == "hey everyone"

def test_edit_multiple_channel(url):
    '''
    Test 8: editing a message when multiple channels have the same message
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    token2 = http_register(url, "Lucy")['token']
    channel_id1 = http_create_public_channel(url, token1, '1')
    channel_id2 = http_create_public_channel(url, token1, '2')
    channel_id3 = http_create_public_channel(url, token1, '3')
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id1
        })
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id2
        })
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id3
        })
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token2,
            'channel_id' : channel_id1,
            'message' : "who's free today"
        })
    message_id = temp.json()['message_id']
    requests.post(f"{url}/message/send", \
        json={
            'token' : token2,
            'channel_id' : channel_id2,
            'message' : "who's free today"
        })
    requests.post(f"{url}/message/send", \
        json={
            'token' : token2,
            'channel_id' : channel_id3,
            'message' : "who's free today"
        })
    requests.put(f"{url}/message/edit", \
        json={
            'token' : token1,
            'message_id' : message_id,
            'message' : "please give me attention!"
        })
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id1,
            'start' : 0
        })
    messages_list1 = temp.json()['messages']
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id2,
            'start' : 0
        })
    messages_list2 = temp.json()['messages']
    temp = requests.get(f"{url}/channel/messages", \
        params={
            'token' : token1,
            'channel_id' : channel_id3,
            'start' : 0
        })
    messages_list3 = temp.json()['messages']
    assert len(messages_list1) == 1
    assert len(messages_list2) == 1
    assert len(messages_list3) == 1
    assert messages_list1[0]['message'] == "please give me attention!"
    assert messages_list2[0]['message'] == "who's free today"
    assert messages_list3[0]['message'] == "who's free today"

def test_edit_other_user(url):
    '''
    Test 9: authorsied user is editing message they didn't sent
    user is not channel owner or flockr owner
    AccessError is raised
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    token2 = http_register(url, "Lucy")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id
        })
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'message' : "who's free today"
        })
    message_id = temp.json()['message_id']
    resp = requests.put(f"{url}/message/edit", \
        json={
            'token' : token2,
            'message_id' : message_id,
            'message' : "please give me attention!"
        })
    assert not resp.ok

def test_edit_user_left_channel(url):
    '''
    Test 10: unauthorsied user is editing message
    user is no longer a member of the channel
    AccessError is raised
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    token2 = http_register(url, "Lucy")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id
        })
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'message' : "who's free today"
        })
    message_id = temp.json()['message_id']
    requests.post(f"{url}/channel/leave", \
        json={
            'token' : token2,
            'channel_id' : channel_id
        })
    resp = requests.put(f"{url}/message/edit", \
        json={
            'token' : token2,
            'message_id' : message_id,
            'message' : "please give me attention!"
        })
    assert not resp.ok

def test_edit_invalid_messageid(url):
    '''
    Test 11: authorsied user is editing message that doesn't exist
    AccessError is raised
    '''
    clear()
    token1 = http_register(url, "Dave")['token']
    token2 = http_register(url, "Lucy")['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(f"{url}/channel/join", \
        json={
            'token' : token2,
            'channel_id' : channel_id
        })
    temp = requests.post(f"{url}/message/send", \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'message' : "who's free today"
        })
    message_id = temp.json()['message_id']
    resp = requests.put(f"{url}/message/edit", \
        json={
            'token' : token2,
            'message_id' : message_id + 2,
            'message' : "please give me attention!"
        })
    assert not resp.ok


##########################################################################################
###                               MESSAGE_SENDLATER TESTS                              ###
##########################################################################################

def test_sendlater_input_error1(url):
    '''
    Test 1: Channel_id is not a valid channel
    Raise an InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, 'channel')
    time_second = 10
    resp = requests.post(url + '/message/sendlater', \
        json={
            'token': token,
            'channel_id': channel_id + 2,
            'message': 'a',
            'time_sent': (datetime.now() + timedelta(seconds=time_second)).timestamp()
        })
    assert resp.status_code == 400

def test_sendlater_input_error2(url):
    '''
    Test 2: message is more than 1000 characters
    Raise an InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, '1')
    time_second = 10
    resp = requests.post(url + '/message/sendlater', \
        json={
            'token': token,
            'channel_id': channel_id,
            'message': 'a'*1001,
            'time_sent': (datetime.now() + timedelta(seconds=time_second)).timestamp()
        })
    assert resp.status_code == 400

def test_sendlater_input_error3(url):
    '''
    Test 3: time_sent is a time in the past
    Raise an InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, '1')
    time_second = -10
    resp = requests.post(url + '/message/sendlater', \
        json={
            'token': token,
            'channel_id': channel_id,
            'message': 'a',
            'time_sent': (datetime.now() + timedelta(seconds=time_second)).timestamp()
        })
    assert resp.status_code == 400

def test_sendlater_access_error(url):
    '''
    Test 4: the user writing the message hasn't joined the channel
    they're trying to post
    Raise an AccessError
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    token2 = http_register(url, 'Sally')['token']
    channel_id = http_create_public_channel(url, token1, '1')
    time_second = 10
    resp = requests.post(url + '/message/sendlater', \
        json={
            'token': token2,
            'channel_id': channel_id,
            'message': 'a',
            'time_sent': (datetime.now() + timedelta(seconds=time_second)).timestamp()
        })
    assert resp.status_code == 400

def test_sendlater_user_valid(url):
    '''
    Test 5: user is not a channel owner nor a flockr owner
    user is able to send messages at a later time.
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    token2 = http_register(url, 'Sally')['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(url + '/channel/join', \
        json={
            'token': token2,
            'channel_id': channel_id,
        })
    time_second = 5
    current_time = datetime.now()
    resp = requests.post(url + '/message/sendlater', \
        json={
            'token': token2,
            'channel_id': channel_id,
            'message': 'a',
            'time_sent': (current_time + timedelta(seconds=time_second)).timestamp()
        })
    assert resp.ok

    sleep(time_second)

    channel_messages = requests.get(url + '/channel/messages', \
        params={
            'token': token1,
            'channel_id': channel_id,
            'start': 0
        })
    messages_list = channel_messages.json()['messages']
    message_timestamp_compare(messages_list, 0, current_time, time_second)
    assert len(messages_list) == 1
    assert messages_list[0]['message'] == "a"

def test_sendlater_channel_owner(url):
    '''
    Test 6: user is a channel owner but not a flockr owner
    user is able to send messages at a later time.
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    u_id2, token2 = http_register(url, 'Sally').values()
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(url + '/channel/join', \
        json={
            'token': token2,
            'channel_id': channel_id,
        })
    requests.post(url + '/channel/addowner', \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'u_id' : u_id2
        })
    time_second = 5
    current_time = datetime.now()
    resp = requests.post(url + '/message/sendlater', \
        json={
            'token': token2,
            'channel_id': channel_id,
            'message': 'a',
            'time_sent': (current_time + timedelta(seconds=time_second)).timestamp()
        })
    assert resp.ok

    sleep(time_second)

    channel_messages = requests.get(url + '/channel/messages', \
        params={
            'token': token1,
            'channel_id': channel_id,
            'start': 0
        })
    messages_list = channel_messages.json()['messages']
    message_timestamp_compare(messages_list, 0, current_time, time_second)
    assert len(messages_list) == 1
    assert len(messages_list) == 1
    assert messages_list[0]['message'] == "a"

def test_sendlater_flockr_owner(url):
    '''
    Test 7: user is a flockr owner
    user is able to send messages at a later time.
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, '1')
    time_second = 5
    current_time = datetime.now()
    resp = requests.post(url + '/message/sendlater', \
        json={
            'token': token,
            'channel_id': channel_id,
            'message': 'a',
            'time_sent': (current_time + timedelta(seconds=time_second)).timestamp()
        })
    assert resp.ok

    sleep(time_second)
    channel_messages = requests.get(url + '/channel/messages', \
        params={
            'token': token,
            'channel_id': channel_id,
            'start': 0
        })
    messages_list = channel_messages.json()['messages']
    message_timestamp_compare(messages_list, 0, current_time, time_second)
    assert len(messages_list) == 1
    assert messages_list[0]['message'] == "a"

def test_sendlater_multi_time(url):
    '''
    Test 8: messages are scheduled to be sent at multiple
    different times
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    token2 = http_register(url, 'Sally')['token']
    channel_id = http_create_public_channel(url, token1, '1')
    requests.post(url + '/channel/join', \
        json={
            'token': token2,
            'channel_id': channel_id,
        })
    current_time = datetime.now()
    time_messages = [(1, 'a'), (2, 'b'), (3, 'c')]
    for i in time_messages:
        time_second, message = i
        resp = requests.post(url + '/message/sendlater', \
            json={
                'token': token2,
                'channel_id': channel_id,
                'message': message,
                'time_sent': (current_time + timedelta(seconds=time_second)).timestamp()
            })
        assert resp.ok

    sleep(6)
    channel_messages = requests.get(url + '/channel/messages', \
        params={
            'token': token1,
            'channel_id': channel_id,
            'start': 0
        })
    messages_list = channel_messages.json()['messages']
    assert len(messages_list) == 3
    for i in range(3):
        time_second, message = time_messages[len(time_messages)-i-1]
        message_timestamp_compare(messages_list, i, current_time, time_second)
        assert messages_list[i]['message'] == message

def test_sendlater_multi_channel(url):
    '''
    Test 9: messages are scheduled to be sent in multiple
    different channels at the same scheduled time
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    token2 = http_register(url, 'Sally')['token']
    channel_ids = []
    for i in range(3):
        channel_id = http_create_public_channel(url, token1, str(i))
        channel_ids.append(channel_id)
        requests.post(url + '/channel/join', \
            json={
                'token': token2,
                'channel_id': channel_id,
            })

    time_second = 5
    current_time = datetime.now()
    messages = ['a', 'b', 'c']
    for i in range(3):
        resp = requests.post(url + '/message/sendlater', \
            json={
                'token': token2,
                'channel_id': channel_ids[i],
                'message': messages[i],
                'time_sent': (current_time + timedelta(seconds=time_second)).timestamp()
            })
        assert resp.ok

    sleep(time_second)
    for i in range(3):
        channel_messages = requests.get(url + '/channel/messages', \
            params={
                'token': token1,
                'channel_id': channel_ids[i],
                'start': 0
            })
        messages_list = channel_messages.json()['messages']
        message_timestamp_compare(messages_list, 0, current_time, time_second)
        assert len(messages_list) == 1
        assert messages_list[0]['message'] == messages[i]


def test_sendlater_multi_user1(url):
    '''
    Test 10: messages are scheduled to be sent by multiple
    different users, all planning to sent at the same time
    '''
    clear()
    tokens = []
    for i in range(3):
        token = http_register(url, 'Bob' + 'b'*i)['token']
        tokens.append(token)
    channel_id = http_create_public_channel(url, tokens[0], '1')
    for i in range(2):
        requests.post(url + '/channel/join', \
            json={
                'token': tokens[i+1],
                'channel_id': channel_id,
            })

    time_second = 5
    messages = ['a', 'b', 'c']
    current_times = []

    for i in range(3):
        current_times.append(datetime.now())
        resp = requests.post(url + '/message/sendlater', \
            json={
                'token': tokens[i],
                'channel_id': channel_id,
                'message': messages[i],
                'time_sent': (current_times[i] + timedelta(seconds=time_second)).timestamp()
            })
        assert resp.ok

    m = requests.get(url + '/channel/messages', \
        params={
            'token': tokens[0],
            'channel_id': channel_id,
            'start': 0
        })
    messages_list = m.json()['messages']
    assert len(messages_list) == 0

    sleep(time_second)
    m = requests.get(url + '/channel/messages', \
            params={
            'token': tokens[0],
            'channel_id': channel_id,
            'start': 0
        })
    messages_list = m.json()['messages']
    assert len(messages_list) == len(messages)

    for i in range(3):
        message_timestamp_compare(messages_list, i, current_times[i], time_second)
        assert messages_list[i]['message'] == messages[len(messages) - (i+1)]

def test_sendlater_multi_user2(url):
    '''
    Test 11: messages are scheduled to be sent by multiple
    different users, planned at different times
    '''
    clear()
    tokens = []
    for i in range(3):
        token = http_register(url, 'Bob' + 'b'*i)['token']
        tokens.append(token)

    channel_id = http_create_public_channel(url, tokens[0], '1')
    for i in range(2):
        requests.post(url + '/channel/join', \
        json={
            'token': tokens[i+1],
            'channel_id': channel_id,
        })

    time_second = [5, 10, 15]
    messages = ['a', 'b', 'c']
    current_times = []

    for i in range(3):
        current_times.append(datetime.now())
        resp = requests.post(url + '/message/sendlater', \
        json={
            'token': tokens[i],
            'channel_id': channel_id,
            'message': messages[i],
            'time_sent': (current_times[i] + timedelta(seconds=time_second[i])).timestamp()
        })
        assert resp.ok

    for i in range(4):
        m = requests.get(url + '/channel/messages', \
            params={
                'token': tokens[0],
                'channel_id': channel_id,
                'start': 0
            })
        messages_list = m.json()['messages']
        assert len(messages_list) == i
        for j in range(i):
            assert messages_list[j]['message'] == messages[i - (j+1)]
            message_timestamp_compare(messages_list, j, current_times[i-(j+1)], \
                time_second[i-(j+1)])
        sleep(time_second[0])


##########################################################################################
###                                 MESSAGE_REACT TESTS                                ###
##########################################################################################

def test_message_react_invalid(url):
    '''
    Test 1: Input Error when message_id is not a valid message
    within a channel that the authorised user has joined
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, '1')
    requests.post(url + '/message/send', \
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : 'hi'
        })

    requests.post(url + '/message/send', \
            json={
                'token' : token,
                'channel_id' : channel_id,
                'message' : 'hi'
            })

    resp = requests.post(url + '/message/react', \
        json={
            'token': token,
            'message_id': 'invalidmessage_id',
            'react_id': 1
        })
    assert resp.status_code == 400

def test_messageid_react_wrongchannel(url):
    '''
    Test 2: Access Error when message_id is not a valid message
    within a channel that the authorised user has joined
    '''
    clear()
    tokens = []
    message_ids = []
    for i in range(2):
        tokens.append(http_register(url, 'Bob' + 'b'*i)['token'])
        channel_id = http_create_public_channel(url, tokens[i], '1')
        message = requests.post(url + '/message/send', \
            json={
                'token' : tokens[i],
                'channel_id' : channel_id,
                'message' : 'hi'
            })
        message_ids.append(message.json()['message_id'])

    # Error when user trying to react to message they are not a member of
    resp = requests.post(url + '/message/react', \
        json={
            'token': tokens[1],
            'message_id': message_ids[0],
            'react_id': 1
        })
    assert resp.status_code == 400


def test_react_invalid_reactid(url):
    '''
    Test 3: Input Error when react_id is invalid (aka not 1)
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, '1')
    data = requests.post(url + '/message/send', \
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    message_id = data.json()['message_id']
    assert data.ok

    resp = requests.post(url + '/message/react', \
        json={
            'token': token,
            'message_id': message_id,
            'react_id': "invalid_react_id"
        })
    assert resp.status_code == 400


def test_react_already_reacted(url):
    '''
    Test 4: Input Error when message_id already contains an active
    React with ID react_id from the authorised user
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, '1')
    data = requests.post(url + '/message/send', \
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    message_id = data.json()['message_id']

    resp1 = requests.post(url + '/message/react', \
        json={
            'token': token,
            'message_id': message_id,
            'react_id': 1
        })
    assert resp1.ok

    resp2 = requests.post(url + '/message/react', \
        json={
            'token': token,
            'message_id': message_id,
            'react_id': 1
        })
    assert resp2.status_code == 400


def test_react_user_invalid(url):
    '''
    Test 5: Unauthorised user of channel trying to react to a message
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token1, '1')
    data = requests.post(url + '/message/send', \
        json={
            'token' : token1,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    message_id = data.json()['message_id']

    token2 = http_register(url, 'Sally')['token']
    resp = requests.post(url + '/message/react', \
        json={
            'token': token2,
            'message_id': message_id,
            'react_id': 1
        })
    assert resp.status_code == 400

def test_react_self_valid(url):
    '''
    Test 6: User successfully reacts to their own message
    Valid - should return empty list
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, '1')

    data = requests.post(url + '/message/send', \
        json={
            'token' : token,
            'channel_id' : channel_id,
            'message' : 'hi'
        })
    message_id = data.json()['message_id']

    resp = requests.post(url + '/message/react', \
        json={
            'token': token,
            'message_id': message_id,
            'react_id': 1
        })
    assert resp.ok
    assert resp.json() == {}


def test_message_react_others_valid(url):
    '''
    Test 7: User validly reacts to multiple other user's message
    This should work
    '''
    clear()
    user, priv, pub = http_load_message(url, 'Bob').values()
    u_id, token = http_register(url, 'Sally').values()
    channel_ids = [pub, priv]

    for channel_id in channel_ids:
        requests.post(url + '/channel/invite', \
            json={
                'token': user['token'],
                'channel_id': channel_id,
                'u_id': u_id
            })
        resp_messages1 = requests.get(url + '/channel/messages', \
            params={
                'token': user['token'],
                'channel_id': channel_id,
                'start': 0
            })
        message_id = resp_messages1.json()['messages'][1]['message_id']

        resp_react = requests.post(url + '/message/react', \
            json={
                'token': token,
                'message_id': message_id,
                'react_id': 1
            })
        assert resp_react.ok
        assert resp_react.json() == {}

        resp_user_not_react = requests.get(url + '/channel/messages', \
            params={
                'token': user['token'],
                'channel_id': channel_id,
                'start': 0
            })
        reacts1 = resp_user_not_react.json()['messages'][1]['reacts'][0]
        assert reacts1['react_id'] == 1
        assert reacts1['u_ids'] == [u_id]
        assert not reacts1['is_this_user_reacted']

        resp_user_react = requests.get(url + '/channel/messages', \
            params={
                'token': token,
                'channel_id': channel_id,
                'start': 0
            })
        reacts2 = resp_user_react.json()['messages'][1]['reacts'][0]
        assert reacts2['react_id'] == 1
        assert reacts2['u_ids'] == [u_id]
        assert reacts2['is_this_user_reacted']

################################################################################
###                            MESSAGE/UNREACT TESTS                         ###
################################################################################
def test_unreact_messageid_invalid(url):
    '''
    Test 1: If message_id is not a valid message in channel that user has joined
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_one = http_create_public_channel(url, token, '1')
    requests.post(url + 'message/send',\
            json={'token': token, 'channel_id': channel_one, 'message': "Hi"})
    resp = requests.post(url + 'message/unreact',\
        json={'token': token, 'message_id': "invalidmessage_id", 'react_id': 1})

    assert resp.status_code == 400

def test_unreact_wrong_channel(url):
    '''
    Test 2: If message doesnt exist within a channel that the authorised user
    has joined
    Raise AccessError
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    channel_one = http_create_public_channel(url, token1, '1')
    message_one = requests.post(url + 'message/send',\
             json={'token': token1, 'channel_id': channel_one, 'message': "Hi"})
    message_id1 = message_one.json()['message_id']
    requests.post(url + 'message/react', \
                json={'token':token1, 'message_id': message_id1, 'react_id': 1})

    token2 = http_register(url, 'Bobx')['token']
    channel_two = http_create_public_channel(url, token2, '2')
    message_two = requests.post(url + 'message/send',\
             json={'token': token2, 'channel_id': channel_two, 'message': "Hi"})
    message_id2 = message_two.json()['message_id']
    requests.post(url + 'message/react', \
                json={'token':token2, 'message_id': message_id2, 'react_id': 1})

    resp = requests.post(url + 'message/unreact',\
        json={'token': token2, 'message_id': message_id1, 'react_id': 1})

    assert resp.status_code == 400

def test_unreact_reactid_invalid(url):
    '''
    Test 3: If react_id is invalid
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_one = http_create_public_channel(url, token, '1')
    message_one = requests.post(url + 'message/send',\
              json={'token': token, 'channel_id': channel_one, 'message': "Hi"})
    message_id1 = message_one.json()['message_id']

    resp = requests.post(url + 'message/unreact',\
        json={'token': token, 'message_id': message_id1,\
              'react_id': 'invalid_react_id'})
    assert resp.status_code == 400


def test_unreact_reactid_inactive(url):
    '''
    Test 4: If the message doesn't have an active react_id(user already
    unreacted to message and they try to unreact again)
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_one = http_create_public_channel(url, token, '1')
    message_one = requests.post(url + 'message/send',\
              json={'token': token, 'channel_id': channel_one, 'message': "Hi"})
    message_id1 = message_one.json()['message_id']
    requests.post(url + 'message/unreact',\
        json={'token': token, 'message_id': message_id1, 'react_id': 1})

    resp = requests.post(url + 'message/unreact',\
        json={'token': token, 'message_id': message_id1, 'react_id': 1})
    assert resp.status_code == 400

def test_unreact_not_in_channel(url):
    '''
    Test 5: If a user not in a channel tries to unreact to a message in that
    channel
    Raise AccessError
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    channel_one = http_create_public_channel(url, token1, '1')
    message_one = requests.post(url + 'message/send',\
              json={'token': token1, 'channel_id': channel_one, 'message': "Hi"})
    message_id1 = message_one.json()['message_id']

    token2 = http_register(url, 'Bobx')['token']

    resp = requests.post(url + 'message/unreact',\
        json={'token': token2, 'message_id': message_id1, 'react_id': 1})
    assert resp.status_code == 400

def test_unreact_valid(url):
    '''
    Test 6: User succesfully unreacts their own message
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_one = http_create_public_channel(url, token, '1')
    message_one = requests.post(url + 'message/send',\
              json={'token': token, 'channel_id': channel_one, 'message': 'Hi'})
    message_id1 = message_one.json()['message_id']
    requests.post(url + 'message/react',\
                json={'token': token, 'message_id': message_id1, 'react_id': 1})

    resp = requests.post(url + 'message/unreact',\
                json={'token': token, 'message_id': message_id1, 'react_id': 1})

    assert resp.ok
    assert json.loads(resp.text) == {}

def test_unreact_other_valid(url):
    '''
    Test 7: User successfully unreacts to other user's messages
    '''
    clear()
    user, priv, pub = http_load_message(url, 'Bob').values()
    u_id, token = http_register(url, 'Bobx').values()
    requests.post(url + 'channel/invite',\
                        json={'token': token, 'channel_id': priv, 'u_id': u_id})
    requests.post(url + 'channel/invite',\
                         json={'token': token, 'channel_id': pub, 'u_id': u_id})

    message_one = requests.get(url + 'channel/messages',\
                params={'token': user['token'], 'channel_id': priv, 'start': 0})
    message_id1 = message_one.json()['messages'][1]['message_id']
    requests.post(url + 'message/react',\
                json={'token': token, 'message_id': message_id1, 'react_id': 1})
    requests.post(url + 'message/unreact',\
                json={'token': token, 'message_id': message_id1, 'react_id': 1})
    react_message = requests.get(url + 'channel/messages',\
                params={'token': user['token'], 'channel_id': priv, 'start': 0})
    reacts = react_message.json()['messages'][1]['reacts']
    assert not reacts[0]['is_this_user_reacted']

    message_one = requests.get(url + 'channel/messages',\
                params={'token': user['token'], 'channel_id': pub, 'start': 0})
    message_id1 = message_one.json()['messages'][1]['message_id']
    requests.post(url + 'message/react',\
                json={'token': token, 'message_id': message_id1, 'react_id': 1})
    requests.post(url + 'message/unreact',\
                json={'token': token, 'message_id': message_id1, 'react_id': 1})
    react_message = requests.get(url + 'channel/messages',\
                params={'token': user['token'], 'channel_id': pub, 'start': 0})
    reacts = react_message.json()['messages'][1]['reacts']
    assert not reacts[0]['is_this_user_reacted']

def test_unreact_same_message(url):
    '''
    Test 8: Check that the "is_this_user_reacted" key in the reacts dictionary
    displayed True unless ALL users unreact the message
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    channel_one = http_create_public_channel(url, token1, '1')
    message_one = requests.post(url + 'message/send',\
             json={'token': token1, 'channel_id': channel_one, 'message': 'Hi'})
    message_id1 = message_one.json()['message_id']

    token2 = http_register(url, 'Bobx')['token']
    requests.post(url + 'channel/join', json={'token': token2,
                                                     'channel_id': channel_one})
    requests.post(url + 'message/react',\
               json={'token': token2, 'message_id': message_id1, 'react_id': 1})

    requests.post(url + 'message/unreact',\
               json={'token': token1, 'message_id': message_id1, 'react_id': 1})
    messages = requests.get(url + 'channel/messages',\
                params={'token': token1, 'channel_id': channel_one, 'start': 0})
    reacts = messages.json()['messages'][0]['reacts']

    assert not reacts[0]['is_this_user_reacted']

    requests.post(url + 'message/unreact',\
               json={'token': token2, 'message_id': message_id1, 'react_id': 1})
    messages = requests.get(url + 'channel/messages',\
                params={'token': token2, 'channel_id': channel_one, 'start': 0})
    reacts = messages.json()['messages'][0]['reacts']

    assert not reacts[0]['is_this_user_reacted']
