from datetime import datetime, timedelta
from time import sleep
import pytest
from helper_tests import *
from auth import *
from channel import *
from standup import *
from other import clear
from message import trivia_start, trivia_end

def run_standup_start(token, channel_id, length):
    '''
    Runs standup_start and asserts that time_finish is returned correctly
    and is approximately equal to the time started + the specified length in seconds.
    time_finish and time_start must be less than a second apart
    Parameters: token, channel_id, length
    '''
    predicted_time = (datetime.now() + timedelta(seconds=length)).timestamp()
    time_finish = standup_start(token, channel_id, length)['time_finish']
    assert time_finish - predicted_time < 0.5


#########################################################
###               STANDUP_START TESTS                 ###
#########################################################
def test_start_invalid_token():
    '''
    Test 1: given an invalid token
    raises AccessError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    auth_logout(token)
    with pytest.raises(AccessError):
        standup_start(token, channel_id, 1)

def test_start_invalid_channel():
    '''
    Test 2: given an invalid channel id
    raises InputError
    '''
    clear()
    token = register('1')[1]
    with pytest.raises(InputError):
        standup_start(token, 1, 1)

def test_start_active_standup_same_user():
    '''
    Test 3: An active standup is currently running in this channel
    The same user starts multiple standups at the same time
    raises InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    standup_start(token, channel_id, 5)
    with pytest.raises(InputError):
        standup_start(token, channel_id, 2)

def test_start_active_standup_multiple_users():
    '''
    Test 4: An active standup is currently running in this channel
    Different users starts multiple standups at the same time
    raises InputError
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    standup_start(token1, channel_id, 5)
    with pytest.raises(InputError):
        standup_start(token2, channel_id, 2)

def test_start_valid():
    '''
    Test 5: one valid startup session
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    run_standup_start(token, channel_id, 2)

def test_multiple_channels():
    '''
    Test 6: startup sessions started in multiple channels at once
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id1 = create_public_channel(token1, '1')
    channel_id2 = create_public_channel(token2, '2')
    run_standup_start(token1, channel_id1, 2)
    run_standup_start(token2, channel_id2, 2)

def test_start_length_0():
    '''
    Test 8: length is 0
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    run_standup_start(token, channel_id, 0)

def test_start_send_message():
    '''
    Test 9: test that the message sent to standup_send is only
    sent after standup finishes
    '''
    clear()
    u_id, token = register('0')
    channel_id = create_public_channel(token, '1')
    time_finish = standup_start(token, channel_id, 2)['time_finish']
    standup_send(token, channel_id, "hello standup")
    message_send(token, channel_id, "hello normal message")
    sleep(3)
    messages = channel_messages(token, channel_id, 0)['messages']
    assert messages[0]['message'] == "firstalasta: hello standup"
    assert messages[0]['time_created'] - time_finish < 1
    assert messages[0]['u_id'] == u_id
    assert messages[1]['message'] == "hello normal message"

def test_start_package_messages():
    '''
    Test 10: messages sent to standup_send are packaged and sent by
    the user who started the standup
    '''
    clear()
    u_id1, token1 = register('1')
    token2 = register('2')[1]
    token3 = register('3')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    channel_join(token3, channel_id)
    time_finish = standup_start(token1, channel_id, 2)['time_finish']
    standup_send(token1, channel_id, "hello")
    standup_send(token2, channel_id, "hello")
    standup_send(token3, channel_id, "hello")
    sleep(3)
    messages = channel_messages(token1, channel_id, 0)['messages']
    assert len(messages) == 1
    assert messages[0]['message'] == \
        "firstblastb: hello\nfirstclastc: hello\nfirstdlastd: hello"
    assert messages[0]['u_id'] == u_id1
    assert messages[0]['time_created'] - time_finish < 1

def test_trivia_active():
    '''
    Test 11: Cannot start standup when trivia is currently active
    Raises InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    trivia_start(token, channel_id, 'default_UNSW')

    with pytest.raises(InputError):
        standup_start(token, channel_id, 5)
    trivia_end(token, channel_id, 'default_UNSW')


#########################################################
###               STANDUP_ACTIVE TESTS                ###
#########################################################
def test_active_invalid_token():
    '''
    Test 1: given an invalid token
    raises AccessError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    auth_logout(token)
    with pytest.raises(AccessError):
        standup_active(token, channel_id)

def test_active_invalid_channel():
    '''
    Test 2: given an invalid channel id
    raises InputError
    '''
    clear()
    token = register('1')[1]
    with pytest.raises(InputError):
        standup_active(token, 1)

def test_active_currently_active():
    '''
    Test 3: standup in channel is active
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    time_finish = standup_start(token, channel_id, 5)['time_finish']
    data = standup_active(token, channel_id)
    assert data['is_active']
    assert data['time_finish'] == time_finish

def test_active_currently_inactive():
    '''
    Test 4: standup in channel is inactive
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    data = standup_active(token, channel_id)
    assert not data['is_active']
    assert data['time_finish'] is None

def test_active_multiple_standups():
    '''
    Test 5: multiple standups in a channel
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    standup_start(token, channel_id, 5)
    assert standup_active(token, channel_id)['is_active']
    sleep(5)
    assert not standup_active(token, channel_id)['is_active']
    standup_start(token, channel_id, 5)
    assert standup_active(token, channel_id)['is_active']
    sleep(5)
    assert not standup_active(token, channel_id)['is_active']

def test_active_multiple_channels():
    '''
    Test 6: standups are active in multiple channels
    '''
    clear()
    token = register('1')[1]
    channel_id1 = create_public_channel(token, '1')
    channel_id2 = create_private_channel(token, '2')
    channel_id3 = create_private_channel(token, '3')
    time_finish1 = standup_start(token, channel_id1, 5)['time_finish']
    time_finish3 = standup_start(token, channel_id3, 5)['time_finish']
    data1 = standup_active(token, channel_id1)
    assert data1['is_active']
    assert data1['time_finish'] == time_finish1
    data2 = standup_active(token, channel_id2)
    assert not data2['is_active']
    assert data2['time_finish'] is None
    data3 = standup_active(token, channel_id3)
    assert data3['is_active']
    assert data3['time_finish'] == time_finish3

################################################################################
###                            STANDUP_SEND TESTS                            ###
################################################################################

def test_send_invalid_token():
    '''
    Test 1: Invalid token is input
    Raise AccessError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    standup_start(token, channel_id, 5)
    auth_logout(token)
    with pytest.raises(AccessError):
        standup_send(token, channel_id, "Hello")

def test_send_invalid_channel_id():
    '''
    Test 2: Invalid channel_id is input
    Raise InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    standup_start(token, channel_id, 5)
    with pytest.raises(InputError):
        standup_send(token, "invalid_channel_id", "Hello")

def test_send_standup_large():
    '''
    Test 3: Message is more than 1000 characters long
    Raise InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    standup_start(token, channel_id, 1)
    with pytest.raises(InputError):
        standup_send(token, channel_id, "x"*1001)

def test_send_standup_empty():
    '''
    Test 4: Message being sent is empty
    Raise InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    standup_start(token, channel_id, 1)
    with pytest.raises(InputError):
        standup_send(token, channel_id, "")

def test_send_standup_not_active():
    '''
    Test 5: A standup is not currently active in the channel
    Raise InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    with pytest.raises(InputError):
        standup_send(token, channel_id, "Hello")

def test_send_not_in_channel():
    '''
    Test 6: Authorised user is not a member of the channel that the message is in
    Raise AccessError
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    standup_start(token1, channel_id, 1)
    with pytest.raises(AccessError):
        standup_send(token2, channel_id, "Hello")

def test_send_valid():
    '''
    Test 7: A message is sent through standup_send by starter of standup
    Check that the message exists inside standup_messages
    '''
    clear()
    token = register('1')[1]
    # create_public_channel(token, 'dummy')
    channel_id = create_public_channel(token, '1')
    standup_start(token, channel_id, 5)
    standup_send(token, channel_id, "Hello")
    sleep(6)
    standup_messages = channel_messages(token, channel_id, 0)['messages']
    assert standup_messages[0]['message'] == "firstblastb: Hello"

def test_send_multiple_people():
    '''
    Test 8: Multiple messages are sent by multiple people through standup_send
    Check that all messages exist in standup_messages
    '''
    clear()
    token1 = register('1')[1]
    u_id2, token2 = register('2')
    u_id3, token3 = register('3')
    channel_id = create_public_channel(token1, '1')
    channel_invite(token1, channel_id, u_id2)
    channel_invite(token1, channel_id, u_id3)
    standup_start(token1, channel_id, 5)
    standup_send(token1, channel_id, "Hello")
    standup_send(token2, channel_id, "World")
    standup_send(token3, channel_id, "!")
    sleep(6)
    standup_messages = channel_messages(token1, channel_id, 0)['messages']
    assert standup_messages[0]['message'] == \
        "firstblastb: Hello\nfirstclastc: World\nfirstdlastd: !"

def test_send_multiple_channels():
    '''
    Test 9: messages are sent through standup in multiple
    channels at once
    '''
    clear()
    tokens = []
    channels = []
    for i in range(3):
        tokens.append(register(str(i))[1])
        channels.append(create_public_channel(tokens[i], '1'))
        standup_start(tokens[i], channels[i], 5)
        standup_send(tokens[i], channels[i], str(i))
    sleep(6)
    letter_names = ['a', 'b', 'c']
    for i in range(3):
        messages = channel_messages(tokens[i], channels[i], 0)['messages']
        assert messages[0]['message'] == f"first{letter_names[i]}last{letter_names[i]}: {i}"

def test_send_trivia():
    '''
    Test 10: '/trivia' is sent
    Input error is raised
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    standup_start(token, channel_id, 5)
    with pytest.raises(InputError):
        standup_send(token, channel_id, "/trivia")
