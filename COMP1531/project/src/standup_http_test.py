from datetime import datetime, timedelta
from time import sleep
import requests
from helper_server_tests import *
from other import clear


def http_standup_start(token, channel_id, length, url):
    '''
    Calculate expected time_length value: length + current time
    Ensure that time_length is equal to expected time
    Disregarding microseconds to account for execution speed
    Parameters:
        token, channel_id, length, url
    '''
    time_expected = (datetime.now() + timedelta(seconds=length)).timestamp()

    res = requests.post(f'{url}standup/start', json={
        'token': token,
        'channel_id': channel_id,
        'length': length
    })
    assert res.ok

    time_finish = res.json()['time_finish']
    assert time_finish - time_expected < 0.5

####################################################################
#                      standup_start tests                         #
####################################################################
def test_start_invalid_token(url):
    '''
    Test 1: Token is invalid
    raise: AccessError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, '1')

    assert requests.post(f'{url}auth/logout', json={
        'token' : token
    }).ok

    res = requests.post(f'{url}standup/start', json={
        'token': token,
        'channel_id': channel_id
    })
    assert res.status_code == 400


def test_start_invalid_channel(url):
    '''
    Test 2: Invalid channel id
    raise: InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']

    res = requests.post(f'{url}standup/start', json={
        'token': token,
        'channel_id': 1,
        'length': 1
    })
    assert res.status_code == 400


def test_start_active_standup_same_user(url):
    '''
    Test 3: active standup already running in channel
    Same user starts multiple standups at the same time in channel
    raise: InputError
    '''
    clear()
    token = http_register(url, 'Bro')['token']
    channel_id = http_create_public_channel(url, token, 'Yo')

    assert requests.post(f'{url}standup/start', json={
        'token': token,
        'channel_id': channel_id,
        'length': 5
    }).ok

    res = requests.post(f'{url}standup/start', json={
        'token': token,
        'channel_id': channel_id,
        'length': 2
    })
    assert res.status_code == 400


def test_start_active_standup_multi_user(url):
    '''
    Test 4: Active standup currently running in channel
    Different users starts multiple standups at the same time
    raise: InputError
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    token2 = http_register(url, 'Alice')['token']
    channel_id = http_create_public_channel(url, token1, 'Hey')
    assert requests.post(f'{url}channel/join', json={
        'token': token2,
        'channel_id': channel_id
    }).ok

    assert requests.post(f'{url}standup/start', json={
        'token': token1,
        'channel_id': channel_id,
        'length': 5
    }).ok

    res = requests.post(f'{url}standup/start', json={
        'token': token2,
        'channel_id': channel_id,
        'length': 2
    })
    assert res.status_code == 400


def test_start_valid(url):
    '''
    Test 5: one valid standup session
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, 'Yo')
    http_standup_start(token, channel_id, 5, url)


def test_multi_channel(url):
    '''
    Test 6: startup sessions started in multiple channels at once
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    token2 = http_register(url, 'Alice')['token']
    channel_id1 = http_create_public_channel(url, token1, '1')
    channel_id2 = http_create_public_channel(url, token2, '2')
    http_standup_start(token1, channel_id1, 5, url)
    http_standup_start(token2, channel_id2, 5, url)


def test_length_0(url):
    '''
    Test 7: length is 0
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, '1')
    http_standup_start(token, channel_id, 0, url)


def test_start_send_message(url):
    '''
    Test 9: test that the message sent to standup_send is only
    sent after standup finishes
    '''
    clear()
    u_id, token = http_register(url, 'Bob').values()
    channel_id = http_create_public_channel(url, token, '1')

    assert requests.post(f'{url}message/send', json={
        'token': token,
        'channel_id': channel_id,
        'message': 'hello normal message'
    })

    res = requests.post(f'{url}standup/start', json={
        'token': token,
        'channel_id': channel_id,
        'length': 5
    })
    assert res.ok
    time_finish = res.json()['time_finish']

    assert requests.post(f'{url}standup/send', json={
        'token': token,
        'channel_id': channel_id,
        'message': 'hello standup'
    }).ok

    sleep(5)
    messages = requests.get(f'{url}channel/messages', params={
        'token': token,
        'channel_id': channel_id,
        'start': 0
    }).json()['messages']

    assert messages[0]['message'] == "bobbob: hello standup"
    assert messages[0]['time_created'] - time_finish < 1
    assert messages[0]['u_id'] == u_id
    assert messages[1]['message'] == "hello normal message"


def test_start_package_messages(url):
    '''
    Test 10: messages sent to standup_send are packaged and sent by
    the user who started the standup
    '''
    clear()
    u_id1, token1 = http_register(url, 'Bro').values()
    token2 = http_register(url, 'Bruv')['token']
    token3 = http_register(url, 'Woah')['token']
    channel_id = http_create_public_channel(url, token1, '1')

    assert requests.post(f'{url}channel/join', json={
        'token': token2,
        'channel_id': channel_id
    }).ok
    assert requests.post(f'{url}channel/join', json={
        'token': token3,
        'channel_id': channel_id
    }).ok

    res = requests.post(f'{url}standup/start', json={
        'token': token1,
        'channel_id': channel_id,
        'length': 5
    })
    assert res.ok
    time_finish = res.json()['time_finish']

    for token in [token1, token2, token3]:
        assert requests.post(f'{url}standup/send', json={
            'token': token,
            'channel_id': channel_id,
            'message': 'hello'
        }).ok

    sleep(5)

    messages = requests.get(f'{url}channel/messages', params={
        'token': token1,
        'channel_id': channel_id,
        'start': 0
    }).json()['messages']

    assert len(messages) == 1
    assert messages[0]['message'] == \
        "brobro: hello\nbruvbruv: hello\nwoahwoah: hello"
    assert messages[0]['u_id'] == u_id1
    assert messages[0]['time_created'] - time_finish < 1


####################################################################
#                     standup_active tests                         #
####################################################################
def test_active_invalid_token(url):
    '''
    Test 1: given an invalid token
    raises AccessError
    '''
    clear()
    token = http_register(url, 'Bro')['token']
    channel_id = http_create_public_channel(url, token, '1')

    assert requests.post(f'{url}auth/logout', json={'token': token}).ok

    res = requests.get(f'{url}standup/active', params={
        'token': token,
        'channel_id': channel_id
    })
    assert res.status_code == 400


def test_active_invalid_channel(url):
    '''
    Test 2: given an invalid channel id
    raises InputError
    '''
    clear()
    token = http_register(url, 'Bro')['token']

    res = requests.get(f'{url}standup/active', params={
        'token': token,
        'channel_id': 1
    })
    assert res.status_code == 400


def test_active_currently_active(url):
    '''
    Test 3: standup in channel is active
    '''
    clear()
    token = http_register(url, 'Yo')['token']
    channel_id = http_create_public_channel(url, token, '1')

    res = requests.post(f'{url}standup/start', json={
        'token': token,
        'channel_id': channel_id,
        'length': 10
    })
    assert res.ok
    time_finish = res.json()['time_finish']

    res = requests.get(f'{url}standup/active', params={
        'token': token,
        'channel_id': channel_id,
    })
    assert res.ok
    data = res.json()
    assert data['is_active']
    assert data['time_finish'] == time_finish


def test_active_currently_inactive(url):
    '''
    Test 4: standup in channel is inactive
    '''
    clear()
    token = http_register(url, 'Bread')['token']
    channel_id = http_create_public_channel(url, token, '1')

    res = requests.get(f'{url}standup/active', params={
        'token': token,
        'channel_id': channel_id,
    })
    assert res.ok
    data = res.json()
    assert not data['is_active']
    assert data['time_finish'] is None


def test_active_multiple_channels(url):
    '''
    Test 5: standups are active in multiple channels
    '''
    clear()
    token = http_register(url, 'Butter')['token']
    channel_id1 = http_create_public_channel(url, token, '1')
    channel_id2 = http_create_public_channel(url, token, '2')
    channel_id3 = http_create_public_channel(url, token, '3')

    res = requests.post(f'{url}standup/start', json={
        'token': token,
        'channel_id': channel_id1,
        'length': 10
    })
    assert res.ok
    time_finish1 = res.json()['time_finish']

    res = requests.post(f'{url}standup/start', json={
        'token': token,
        'channel_id': channel_id3,
        'length': 10
    })
    assert res.ok
    time_finish3 = res.json()['time_finish']

    res = requests.get(f'{url}standup/active', params={
        'token': token,
        'channel_id': channel_id1,
    })
    assert res.ok
    data1 = res.json()
    assert data1['is_active']
    assert data1['time_finish'] == time_finish1

    res = requests.get(f'{url}standup/active', params={
        'token': token,
        'channel_id': channel_id2,
    })
    assert res.ok
    data2 = res.json()
    assert not data2['is_active']
    assert data2['time_finish'] is None

    res = requests.get(f'{url}standup/active', params={
        'token': token,
        'channel_id': channel_id3,
    })
    assert res.ok
    data3 = res.json()
    assert data3['is_active']
    assert data3['time_finish'] == time_finish3



################################################################################
###                          STANDUP_SEND HTTP TESTS                         ###
################################################################################

def test_http_send_invalid_token(url):
    '''
    Test 1: Invalid token is input
    Raise AccessError
    '''
    clear()

    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, 'channel')

    data = {'token': token, 'channel_id': channel_id, 'length': 5}
    response = requests.post(url + '/standup/start', json=data)
    assert response.ok

    data = {'token': token}
    response = requests.post(url + '/auth/logout', json=data)

    data = {'token': token, 'channel_id': channel_id, 'message': 'Hello'}
    response = requests.post(url + '/standup/send', json=data)
    assert response.status_code == 400


def test_http_send_invalid_channel_id(url):
    '''
    Test 2: Invalid channel_id is input
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, 'channel')

    data = {'token': token, 'channel_id': channel_id, 'length': 5}
    response = requests.post(url + '/standup/start', json=data)
    assert response.ok

    data = {'token': token, 'channel_id': 'invalid_channel_id', 'message': 'Hello'}
    response = requests.post(url + '/standup/send', json=data)
    assert response.status_code == 400


def test_http_send_standup_large(url):
    '''
    Test 3: Message is more than 1000 characters long
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, 'channel')

    data = {'token': token, 'channel_id': channel_id, 'length': 1}
    response = requests.post(url + '/standup/start', json=data)
    assert response.ok

    data = {'token': token, 'channel_id': channel_id, 'message': 'x'*1001}
    response = requests.post(url + '/standup/send', json=data)
    assert response.status_code == 400


def test_http_send_standup_empty(url):
    '''
    Test 4: Message being sent is empty
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, 'channel')

    data = {'token': token, 'channel_id': channel_id, 'length': 1}
    response = requests.post(url + '/standup/start', json=data)
    assert response.ok

    data = {'token': token, 'channel_id': channel_id, 'message': ''}
    response = requests.post(url + '/standup/send', json=data)
    assert response.status_code == 400

def test_http_send_standup_not_active(url):
    '''
    Test 5: A standup is not currently active in the channel
    Raise InputError
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, 'channel')

    data = {'token': token, 'channel_id': channel_id, 'message': 'Hello'}
    response = requests.post(url + '/standup/send', json=data)
    assert response.status_code == 400


def test_http_send_not_in_channel(url):
    '''
    Test 6: Authorised user is not a member of the channel that the message is in
    Raise AccessError
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    token2 = http_register(url, 'Alice')['token']

    channel_id = http_create_public_channel(url, token1, 'channel')

    data = {'token': token1, 'channel_id': channel_id, 'length': 1}
    response = requests.post(url + '/standup/start', json=data)
    assert response.ok

    data = {'token': token2, 'channel_id': channel_id, 'message': 'Hello'}
    response = requests.post(url + '/standup/send', json=data)
    assert response.status_code == 400


def test_http_send_valid(url):
    '''
    Test 7: A message is sent through standup_send by starter of standup
    Check that the message exists inside standup_messages
    '''
    clear()
    token = http_register(url, 'Bob')['token']
    channel_id = http_create_public_channel(url, token, 'channel')

    data = {'token': token, 'channel_id': channel_id, 'length': 5}
    response = requests.post(url + '/standup/start', json=data)
    assert response.ok

    data2 = {'token': token, 'channel_id': channel_id, 'message': 'Hello'}
    response2 = requests.post(url + '/standup/send', json=data2)
    assert response2.ok

    sleep(5)

    parameters = {'token': token, 'channel_id': channel_id, 'start': 0}
    standup_messages = requests.get(url + '/channel/messages', params=parameters)
    assert standup_messages.json()['messages'][0]['message'] == "bobbob: Hello"


def test_http_send_multiple(url):
    '''
    Test 8: Multiple messages are sent by multiple people through standup_send
    Check that all messages exist in standup_messages
    '''
    clear()
    token1 = http_register(url, 'Bob')['token']
    u_id2, token2 = http_register(url, 'Alice').values()
    u_id3, token3 = http_register(url, 'Peter').values()

    channel_id = http_create_public_channel(url, token1, 'channel')

    data = {'token': token1, 'channel_id': channel_id, 'u_id': u_id2}
    response = requests.post(url + '/channel/invite', json=data)
    assert response.ok

    data = {'token': token1, 'channel_id': channel_id, 'u_id': u_id3}
    response = requests.post(url + '/channel/invite', json=data)
    assert response.text

    data = {'token': token1, 'channel_id': channel_id, 'length': 5}
    response = requests.post(url + '/standup/start', json=data)
    assert response.ok

    data = {'token': token1, 'channel_id': channel_id, 'message': 'Hello'}
    response = requests.post(url + '/standup/send', json=data)
    assert response.ok

    data = {'token': token2, 'channel_id': channel_id, 'message': 'World'}
    response = requests.post(url + '/standup/send', json=data)
    assert response.ok

    data = {'token': token3, 'channel_id': channel_id, 'message': '!'}
    response = requests.post(url + '/standup/send', json=data)
    assert response.ok

    sleep(5)

    parameters = {'token': token1, 'channel_id': channel_id, 'start': 0}
    standup_messages = requests.get(url + '/channel/messages', params=parameters)
    assert standup_messages.json()['messages'][0]['message'] == \
        "bobbob: Hello\nalicealice: World\npeterpeter: !"
