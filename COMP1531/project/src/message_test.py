from datetime import datetime, timedelta
from time import sleep
import pytest
from message import *
from helper_tests import *
from channel import *
from auth import *
from error import *
from other import clear


##########################################################################################
###                                 MESSAGE_REACT TESTS                                ###
##########################################################################################

def test_message_react_invalid():
    '''
    Test 1: Input Error when message_id is not a valid message
    within a channel that the authorised user has joined
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_send(token, channel_id, "hi")

    with pytest.raises(InputError):
        message_react(token, "invalidmessage_id", 1)

def test_messageid_react_wrongchannel():
    '''
    Test 2: Access Error when message_id is not a valid message
    within a channel that the authorised user has joined
    '''
    clear()
    token1 = register('1')[1]
    channel_id1 = create_public_channel(token1, '1')
    message_id1 = message_send(token1, channel_id1, "hi")['message_id']

    token2 = register('2')[1]
    channel_id2 = create_public_channel(token2, '2')
    message_send(token2, channel_id2, "hello")

    # Error when user trying to react to message they are not a member of
    with pytest.raises(AccessError):
        message_react(token2, message_id1, 1)


def test_react_invalid_reactid():
    '''
    Test 3: Input Error when react_id is invalid (aka not 1)
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_id = message_send(token, channel_id, "hi")['message_id']

    with pytest.raises(InputError):
        message_react(token, message_id, "invalid_react_id")


def test_react_already_reacted():
    '''
    Test 4: Input Error when message_id already contains an active
    React with ID react_id from the authorised user
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_id = message_send(token, channel_id, "hi")['message_id']

    message_react(token, message_id, 1)

    with pytest.raises(InputError):
        message_react(token, message_id, 1)

def test_react_user_invalid():
    '''
    Test 5: Unauthorised user of channel trying to react to a message
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_id = message_send(token, channel_id, "hi")['message_id']

    token2 = register('2')[1]
    with pytest.raises(AccessError):
        message_react(token2, message_id, 1)

def test_react_self_valid():
    '''
    Test 6: User successfully reacts to their own message
    Valid - should return empty list
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_id = message_send(token, channel_id, "hi")['message_id']

    assert message_react(token, message_id, 1) == {}


def test_message_react_others_valid():
    '''
    Test 7: User validly reacts to multiple other user's message
    This should work
    '''
    clear()
    user, priv, pub = load_message().values()
    u_id, token = register('1')
    channel_invite(user['token'], priv, u_id)
    channel_invite(user['token'], pub, u_id)

    message_id = channel_messages(user['token'], priv, 0)['messages'][1]['message_id']
    message_react(token, message_id, 1)

    reacts = channel_messages(user['token'], priv, 0)['messages'][1]['reacts'][0]
    assert reacts['react_id'] == 1
    assert reacts['u_ids'] == [u_id]
    assert not reacts['is_this_user_reacted']

    reacts = channel_messages(token, priv, 0)['messages'][1]['reacts'][0]
    assert reacts['react_id'] == 1
    assert reacts['u_ids'] == [u_id]
    assert reacts['is_this_user_reacted']

    message_id = channel_messages(user['token'], pub, 0)['messages'][1]['message_id']
    message_react(token, message_id, 1)

    reacts = channel_messages(user['token'], pub, 0)['messages'][1]['reacts'][0]
    assert reacts['react_id'] == 1
    assert reacts['u_ids'] == [u_id]
    assert not reacts['is_this_user_reacted']

    reacts = channel_messages(token, pub, 0)['messages'][1]['reacts'][0]
    assert reacts['react_id'] == 1
    assert reacts['u_ids'] == [u_id]
    assert reacts['is_this_user_reacted']

##########################################################################################
###                                MESSAGE_UNREACT TESTS                               ###
##########################################################################################

def test_message_unreact_invalid():
    '''
    Test 1: Input Error when message_id is not a valid message
    within a channel that the authorised user has joined
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_send(token, channel_id, "hi")

    with pytest.raises(InputError):
        message_unreact(token, "invalidmessage_id", 1)

def test_messageid_unreact_wrongchannel():
    '''
    Test 2: Access Error when message_id is not a valid message
    within a channel that the authorised user has joined
    '''
    clear()
    token1 = register('1')[1]
    channel_id1 = create_public_channel(token1, '1')
    message_id1 = message_send(token1, channel_id1, "hi")['message_id']
    message_react(token1, message_id1, 1)

    token2 = register('2')[1]
    channel_id2 = create_public_channel(token2, '2')
    message_id2 = message_send(token2, channel_id2, "hello")['message_id']
    message_react(token2, message_id2, 1)

    # Error when user trying to react to message they are not a member of
    with pytest.raises(AccessError):
        message_unreact(token2, message_id1, 1)


def test_unreact_invalid_reactid():
    '''
    Test 3: Input Error when react_id is invalid (aka not 1)
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_id = message_send(token, channel_id, "hi")['message_id']
    message_react(token, message_id, 1)

    with pytest.raises(InputError):
        message_unreact(token, message_id, "invalid_react_id")


def test_unreact_already_unreacted():
    '''
    Test 4: Input Error when message_id does not have
    an active react_id
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_id = message_send(token, channel_id, "hi")['message_id']
    message_react(token, message_id, 1)
    message_unreact(token, message_id, 1)

    with pytest.raises(InputError):
        message_unreact(token, message_id, 1)

def test_unreact_channeluser_invalid():
    '''
    Test 5: Unauthorised user of channel trying to unreact a message
    Raises Access Error since user is not part of channel
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_id = message_send(token, channel_id, "hi")['message_id']

    token2 = register('2')[1]
    with pytest.raises(AccessError):
        message_unreact(token2, message_id, 1)

def test_unreact_self_valid():
    '''
    Test 6: User successfully unreacts their own message
    Valid - should return empty list
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_id = message_send(token, channel_id, "hi")['message_id']
    message_react(token, message_id, 1)
    assert message_unreact(token, message_id, 1) == {}

def test_message_unreact_others_valid():
    '''
    Test 7: User validly unreacts to multiple other user's message
    This should work
    '''
    clear()
    user, priv, pub = load_message().values()
    u_id, token = register('1')
    channel_invite(user['token'], priv, u_id)
    channel_invite(user['token'], pub, u_id)

    message_id = channel_messages(user['token'], priv, 0)['messages'][1]['message_id']
    message_react(token, message_id, 1)
    message_unreact(token, message_id, 1)
    reacts = channel_messages(user['token'], priv, 0)['messages'][1]['reacts'][0]
    assert not reacts['is_this_user_reacted']

    message_id = channel_messages(user['token'], pub, 0)['messages'][1]['message_id']
    message_react(token, message_id, 1)
    message_unreact(token, message_id, 1)
    reacts = channel_messages(user['token'], pub, 0)['messages'][1]['reacts'][0]
    assert not reacts['is_this_user_reacted']

def test_message_unreact_samemessage():
    '''
    Test 8: Check that the "is_this_user_reacted" key in the reacts dictionary
    displayed False unless the authorised user unreacted the message
    '''

    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_id = message_send(token, channel_id, "hi")['message_id']
    message_react(token, message_id, 1)

    token2 = register('2')[1]
    channel_join(token2, channel_id)
    message_react(token2, message_id, 1)

    message_unreact(token2, message_id, 1)
    reacts = channel_messages(token2, channel_id, 0)['messages'][0]['reacts'][0]
    assert not reacts['is_this_user_reacted']

    message_unreact(token, message_id, 1)
    reacts = channel_messages(token, channel_id, 0)['messages'][0]['reacts'][0]
    assert not reacts['is_this_user_reacted']


##########################################################################################
###                                 MESSAGE_SEND TESTS                                 ###
##########################################################################################

def test_send_invalid_token():
    '''
    Test 1: given an invalid token
    Access Error is raised
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    auth_logout(token)
    with pytest.raises(AccessError):
        message_send(token, channel_id, "hi")


def test_send_input_error():
    '''
    Test 2: message is more than 1000 characters
    InputError is raised
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    with pytest.raises(InputError):
        message_send(token, channel_id, 'a'*1001)


def test_send_access_error():
    '''
    Test 3: authorised user is not in the channel they are trying to post to
    AccessError is raised
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    with pytest.raises(AccessError):
        message_send(token2, channel_id, "hi")


def test_send_access_error_flockr_owner():
    '''
    Test 4: authorised user is a flockr owner
    and tries to post to a channel they have not joined
    AccessError is raised
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token2, '1')
    with pytest.raises(AccessError):
        message_send(token1, channel_id, "hi")


def test_send_small():
    '''
    Test 5: send small message
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_send(token, channel_id, "hi")
    list_messages = channel_messages(token, channel_id, 0)['messages']
    assert len(list_messages) == 1
    assert list_messages[0]['message'] == "hi"


def test_send_1000_characters():
    '''
    Test 6: message is 1000 characters long
    InputError should not be raised
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_send(token, channel_id, 'a'*1000)
    assert len(channel_messages(token, channel_id, 0)['messages']) == 1


def test_send_empty_message():
    '''
    Test 7: message is empty, should not send
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_send(token, channel_id, '')
    assert len(channel_messages(token, channel_id, 0)['messages']) == 0


def test_send_multiple_messages():
    '''
    Test 8: send multiple messages by different users
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    token3 = register('3')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    channel_join(token3, channel_id)
    message_send(token1, channel_id, "hello")
    message_send(token2, channel_id, "hi")
    message_send(token2, channel_id, "goodbye")
    message_send(token3, channel_id, "bye everyone")
    message_list = channel_messages(token1, channel_id, 0)['messages']
    assert len(message_list) == 4
    assert message_list[0]['message'] == "bye everyone"
    assert message_list[1]['message'] == "goodbye"
    assert message_list[2]['message'] == "hi"
    assert message_list[3]['message'] == "hello"


##########################################################################################
###                                 TRIVIA MESSAGE TESTS                               ###
##########################################################################################

def test_trivia():
    '''
    Test 1: User types in '/trivia'
    message should display all trivia commands
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_send(token, channel_id, "/trivia")
    message_list = channel_messages(token, channel_id, 0)['messages']
    assert len(message_list) == 1
    assert " ******** TRIVIA ******** " in message_list[0]['message']

def test_trivia_invalid_command():
    '''
    Test 2: User types invalid command after /trivia
    Raise InputError and send a message to show correct format
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_send(token, channel_id, "/trivia invalid_command")

    message_list = channel_messages(token, channel_id, 0)['messages']
    assert len(message_list) == 1
    message = "400 Bad Request: Invalid format. " + \
            "Type /trivia to see the commands available."
    assert message_list[0]['message'] == message

def test_trivia_create_category():
    '''
    Test 3: User creates a new trivia category
    using command /trivia create <name_of_category>
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    name = 'new'
    command = f"/trivia create {name}"
    message_send(token, channel_id, command)

    message_list = channel_messages(token, channel_id, 0)['messages']
    assert len(message_list) == 1
    message = f"Category: {name} has been succesfully created\n" + \
                "To add questions please type /trivia and follow the command for adding questions"

    assert message_list[0]['message'] == message

def test_triva_add_questions_default():
    '''
    Test 4: User adds a question to the default_UNSW category
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    command = "/trivia add_questions default_UNSW\n" + \
        "New Question\n" + \
            "Option 1\n" + \
                "Option 2"
    message_send(token, channel_id, command)

    message_list = channel_messages(token, channel_id, 0)['messages']
    assert len(message_list) == 1
    assert message_list[0]['message'] == "Question Successfully Added"

def test_trivia_add_questions_new():
    '''
    Test 4: User adds a question to a new category
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    name = 'new'
    command = f"/trivia create {name}"
    message_send(token, channel_id, command)

    message_list = channel_messages(token, channel_id, 0)['messages']
    assert len(message_list) == 1
    message1 = f"Category: {name} has been succesfully created\n" + \
                "To add questions please type /trivia and follow the command for adding questions"

    assert message_list[0]['message'] == message1

    add_command = f"/trivia add_questions {name}\n" + \
        "New Question\n" + \
            "Option 1\n" + \
                "Option 2"
    message_send(token, channel_id, add_command)

    message_list = channel_messages(token, channel_id, 0)['messages']
    assert len(message_list) == 2
    message2 = "Question Successfully Added"

    assert message_list[0]['message'] == message2
    assert message_list[1]['message'] == message1


def test_trivia_invalid_add_questions_command():
    '''
    Test 5: User types invalid command after /trivia add_questions
    Send a message to show correct format
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_send(token, channel_id, "/trivia add_questions invalid_command")

    message_list = channel_messages(token, channel_id, 0)['messages']
    assert len(message_list) == 1
    message = "400 Bad Request: invalid format: " + \
        "/trivia add_questions <name of category>\\n<question>\\n<max 4 options each on a new line>"
    assert message_list[0]['message'] == message

def test_trivia_start():
    '''
    Test 6: User successfully starts a trivia
    After all questions end, channel shows list of winners
    '''
    clear()
    token = register('Hello')[1]
    channel_id = create_public_channel(token, 'OKAY')

    name = 'new'
    command = f"/trivia create {name}"
    message_send(token, channel_id, command)

    add_command = f"/trivia add_questions {name}\n" + \
        "New Question\n" + \
            "Option 1\n" + \
                "Option 2"
    message_send(token, channel_id, add_command)

    command = f'/trivia start {name}'
    message_send(token, channel_id, command)

    sleep(1)

    message_list = channel_messages(token, channel_id, 0)['messages']
    assert len(message_list) == 6

    sleep(12)
    message_list = channel_messages(token, channel_id, 0)['messages']
    assert len(message_list) == 7

    message1 = f"Category: {name} has been succesfully created\n" + \
                "To add questions please type /trivia and follow the command for adding questions"
    message2 = "Question Successfully Added"
    message3 = "Trivia started! React to your chosen option!"
    message4 = "TRIVIA:\n\t" + \
                "New Question"
    message5 = "TRIVIA (option):\n\t" + \
                "Option 1"
    message6 = "TRIVIA (option):\n\t" + \
                "Option 2"
    message7 = "Trivia ended!\nLeaderboard:\n"

    assert message_list[0]['message'] == message7
    assert message_list[1]['message'] in [message5, message6]
    assert message_list[2]['message'] in [message5, message6]
    assert message_list[3]['message'] == message4
    assert message_list[4]['message'] == message3
    assert message_list[5]['message'] == message2
    assert message_list[6]['message'] == message1

def test_trivia_end():
    '''
    Test 7: User successfully ends the trivia
    '''
    clear()
    token = register('Hello')[1]
    channel_id = create_public_channel(token, 'OKAY')

    message_send(token, channel_id, '/trivia start default_UNSW')
    sleep(5)
    message_send(token, channel_id, '/trivia end default_UNSW')
    message_list = channel_messages(token, channel_id, 0)['messages']
    assert message_list[0]['message'] == "Trivia ended!\nLeaderboard:\n"


##########################################################################################
###                                 MESSAGE_REMOVE TESTS                               ###
##########################################################################################

def test_remove_invalid_token():
    '''
    Test 1: given an invalid token
    AccessError is raised
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_id = message_send(token, channel_id, "hi")['message_id']
    auth_logout(token)
    with pytest.raises(AccessError):
        message_remove(token, message_id)


def test_remove_input_error1():
    '''
    Test 2: message_id does not exist
    InputError is raised
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_id = message_send(token, channel_id, "hi")['message_id']
    with pytest.raises(InputError):
        message_remove(token, message_id + 2)


def test_remove_input_error2():
    '''
    Test 3: message_id no longer exists
    InputError is raised
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_id = message_send(token, channel_id, "hi")['message_id']
    message_remove(token, message_id)
    with pytest.raises(InputError):
        message_remove(token, message_id)


def test_remove_access_error():
    '''
    Test 4: authorised user did not send the message
    and is not an owner of the channel or flockr
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    message_id = message_send(token1, channel_id, "hi")['message_id']
    with pytest.raises(AccessError):
        message_remove(token2, message_id)


def test_remove_user_sent():
    '''
    Test 5: authorised user is removing a message they sent
    user is not an owner of the channel or a flockr owner
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    message_id = message_send(token2, channel_id, "hi")['message_id']
    message_remove(token2, message_id)
    assert len(channel_messages(token1, channel_id, 0)['messages']) == 0


def test_remove_channel_owner():
    '''
    Test 6: authorised user is a channel owner but not a flockr owner
    user is a removing a message they did not send
    '''
    clear()
    token1 = register('1')[1]
    u_id2, token2 = register('2')
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    channel_addowner(token1, channel_id, u_id2)
    message_id = message_send(token1, channel_id, "hi")['message_id']
    message_remove(token2, message_id)
    assert len(channel_messages(token1, channel_id, 0)['messages']) == 0


def test_remove_flockr_owner():
    '''
    Test 7: authorised user is a flockr owner
    user is removing a message they did not send
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    message_id = message_send(token2, channel_id, "hi")['message_id']
    message_remove(token1, message_id)
    assert len(channel_messages(token1, channel_id, 0)['messages']) == 0


def test_remove_small():
    '''
    Test 8: test function removes the correct message
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_id1 = message_send(token, channel_id, "hi")['message_id']
    message_id2 = message_send(token, channel_id, "hello everyone")['message_id']
    message_remove(token, message_id1)
    messages_list = channel_messages(token, channel_id, 0)['messages']
    assert messages_list[0]['message'] == "hello everyone"
    message_remove(token, message_id2)
    assert len(channel_messages(token, channel_id, 0)['messages']) == 0


def test_remove_multiple_channels():
    '''
    Test 9: removing a message when multiple channels have the same message
    '''
    clear()
    token = register('1')[1]
    channel_id1 = create_public_channel(token, '1')
    channel_id2 = create_private_channel(token, '2')
    channel_id3 = create_public_channel(token, '3')
    message_send(token, channel_id1, "hi")
    message_id2 = message_send(token, channel_id2, "hi")['message_id']
    message_send(token, channel_id3, "hi")
    message_remove(token, message_id2)
    assert len(channel_messages(token, channel_id1, 0)['messages']) == 1
    assert len(channel_messages(token, channel_id2, 0)['messages']) == 0
    assert len(channel_messages(token, channel_id3, 0)['messages']) == 1


def test_remove_user_leaves():
    '''
    Test 10: user is no longer in a channel and removes their old message from that channel
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    message_send(token1, channel_id, "hi")
    message_id = message_send(token2, channel_id, "hi")['message_id']
    channel_leave(token2, channel_id)
    message_remove(token2, message_id)
    assert len(channel_messages(token1, channel_id, 0)['messages']) == 1


##########################################################################################
###                                 MESSAGE_EDIT TESTS                                 ###
##########################################################################################

def test_edit_invalid_token():
    '''
    Test 1: given an invalid token
    AccessError is raised
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_id = message_send(token, channel_id, "hi")['message_id']
    auth_logout(token)
    with pytest.raises(AccessError):
        message_edit(token, message_id, "hello")

def test_edit_removed_message():
    '''
    Test 2: edit when the message is already removed
    AccessError is raised
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_id = message_send(token, channel_id, "hi")['message_id']
    message_remove(token, message_id)
    with pytest.raises(InputError):
        message_edit(token, message_id, "hey everyone")

def test_edit_user_sent():
    '''
    Test 3: user who wrote the message is able to edit
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    message_id = message_send(token2, channel_id, "hi")['message_id']
    message_edit(token2, message_id, "hey everyone")
    messages_list = channel_messages(token1, channel_id, 0)['messages']
    assert len(messages_list) == 1
    assert messages_list[0]['message'] == "hey everyone"

def test_edit_channel_owner():
    '''
    Test 4: authorsied user is editing message
    user is channel owner but not flockr owner
    '''
    clear()
    token1 = register('1')[1]
    u_id2, token2 = register('2')
    token3 = register('3')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    channel_join(token3, channel_id)
    channel_addowner(token1, channel_id, u_id2)
    message_id = message_send(token3, channel_id, "hi")['message_id']
    message_edit(token2, message_id, "Howdy")
    messages_list = channel_messages(token1, channel_id, 0)['messages']
    assert len(messages_list) == 1
    assert messages_list[0]['message'] == "Howdy"

def test_edit_flockr_owner():
    '''
    Test 5: authorsied user is editing message
    message written by member of channel that is not owner of channel, or flock owner
    user is flockr owner
    '''
    clear()
    token1 = register('1')[1]
    u_id2, token2 = register('2')
    token3 = register('3')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    channel_join(token3, channel_id)
    channel_addowner(token1, channel_id, u_id2)
    message_id = message_send(token3, channel_id, "hi")['message_id']
    message_edit(token1, message_id, "Howdy")
    messages_list = channel_messages(token1, channel_id, 0)['messages']
    assert len(messages_list) == 1
    assert messages_list[0]['message'] == "Howdy"

def test_edit_empty_message():
    '''
    Test 6: user who wrote the message edits to an empty message
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    message_id = message_send(token2, channel_id, "hi")['message_id']
    message_edit(token2, message_id, "")
    messages_list = channel_messages(token1, channel_id, 0)['messages']
    assert len(messages_list) == 0

def test_edit_multiple_message():
    '''
    Test 7: authorsied user is editing message they sent
    user is editing multiple messages
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    message_id1 = message_send(token2, channel_id, "hi")['message_id']
    message_id2 = message_send(token2, channel_id, "how is everyone")['message_id']
    message_id3 = message_send(token2, channel_id, "who's free today")['message_id']
    message_edit(token2, message_id1, "hey everyone")
    message_edit(token2, message_id2, "how y'all doing")
    message_edit(token2, message_id3, "")
    messages_list = channel_messages(token1, channel_id, 0)['messages']
    assert len(messages_list) == 2
    assert messages_list[0]['message'] == "how y'all doing"
    assert messages_list[1]['message'] == "hey everyone"

def test_edit_multiple_channel():
    '''
    Test 8: editing a message when multiple channels have the same message
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id1 = create_public_channel(token1, '1')
    channel_id2 = create_public_channel(token1, '2')
    channel_id3 = create_public_channel(token1, '3')
    channel_join(token2, channel_id1)
    channel_join(token2, channel_id2)
    channel_join(token2, channel_id3)
    message_id1 = message_send(token2, channel_id1, "who's free today")['message_id']
    message_send(token2, channel_id2, "who's free today")
    message_send(token2, channel_id3, "who's free today")
    message_edit(token2, message_id1, "please give me attention!")
    messages_list1 = channel_messages(token1, channel_id1, 0)['messages']
    messages_list2 = channel_messages(token1, channel_id2, 0)['messages']
    messages_list3 = channel_messages(token1, channel_id3, 0)['messages']
    assert len(messages_list1) == 1
    assert len(messages_list2) == 1
    assert len(messages_list3) == 1
    assert messages_list1[0]['message'] == "please give me attention!"
    assert messages_list2[0]['message'] == "who's free today"
    assert messages_list3[0]['message'] == "who's free today"

def test_edit_other_user():
    '''
    Test 9: authorsied user is editing message they didn't sent
    user is not channel owner or flockr owner
    AccessError is raised
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    message_id = message_send(token1, channel_id, "hi")['message_id']
    with pytest.raises(AccessError):
        message_edit(token2, message_id, "Howdy")

def test_edit_user_left_channel():
    '''
    Test 10: unauthorsied user is editing message
    user is no longer a member of the channel
    AccessError is raised
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    message_id = message_send(token2, channel_id, "hi")['message_id']
    channel_leave(token2, channel_id)
    with pytest.raises(AccessError):
        message_edit(token2, message_id, "Howdy")

def test_edit_invalid_messageid():
    '''
    Test 11: authorsied user is editing message that doesn't exist
    AccessError is raised
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    message_id = message_send(token2, channel_id, "hi")['message_id']
    with pytest.raises(InputError):
        message_edit(token2, message_id + 2, "Howdy")


##########################################################################################
###                                  MESSAGE_PIN TESTS                                 ###
##########################################################################################

def test_message_pin_invalid_message_id():
    '''
    Pin message where message_id is invalid
    Expect InputError
    '''
    clear()
    user, _, channel_id = load_message().values()
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    message_id = messages[0]['message_id']

    with pytest.raises(InputError):
        message_pin(user['token'], message_id + 100)


def test_message_pin_message_already_pinned():
    '''
    Pin message where message is already pinned
    Expect InputError
    '''
    clear()
    user, _, channel_id = load_message().values()
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    message_id = messages[0]['message_id']

    message_pin(user['token'], message_id)

    with pytest.raises(InputError):
        message_pin(user['token'], message_id)


def test_message_pin_invalid_token():
    '''
    Pin message when token is invalid
    Expect AccessError
    '''
    clear()
    user, _, channel_id = load_message().values()
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    message_id = messages[1]['message_id']

    with pytest.raises(AccessError):
        message_pin(user['token'] + 'bad_token', message_id)


def test_message_pin_user_not_in_channel():
    '''
    User who is not in the channel tries to pin a message
    Expect AccessError
    '''
    clear()
    user, _, channel_id = load_message().values()
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    message_id = messages[2]['message_id']

    token = register('1')[1]
    with pytest.raises(AccessError):
        message_pin(token, message_id)


def test_message_pin_user_not_channel_owner():
    '''
    User who is in channel but not a channel owner tries to pin a message
    Expect AccessError
    '''
    clear()
    user, _, channel_id = load_message().values()
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    message_id = messages[2]['message_id']
    token = register('1')[1]

    channel_join(token, channel_id)
    with pytest.raises(AccessError):
        message_pin(token, message_id)


def test_message_pin_user_flockr_owner_not_in_channel():
    '''
    User who is not in channel but is a global owner tries to pin message
    Expect AccessError
    '''
    clear()
    user, _, channel_id = load_message().values()
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    message_id = messages[2]['message_id']

    channel_leave(user['token'], channel_id)

    with pytest.raises(AccessError):
        message_pin(user['token'], message_id)


def test_message_pin_user_flockr_owner_member_in_channel():
    '''
    User who is in channel as a normal member but is a global owner tries to pin message
    This should work
    '''
    clear()
    user, _, channel_id = load_message().values()
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    message_id = messages[2]['message_id']

    u_id, token = register('2')
    channel_join(token, channel_id)
    channel_addowner(user['token'], channel_id, u_id)
    channel_removeowner(token, channel_id, user['u_id'])

    message_pin(user['token'], message_id)
    messages = channel_messages(user['token'], channel_id, 0)['messages']

    assert messages[2]['is_pinned']


def test_message_pin_user_channel_owner():
    '''
    User who is a channel owner tries to pin message
    This should work
    '''
    clear()
    user, _, channel_id = load_message().values()
    u_id, token = register('1')
    channel_join(token, channel_id)
    channel_addowner(user['token'], channel_id, u_id)

    messages = channel_messages(token, channel_id, 0)['messages']
    message_id = messages[2]['message_id']

    message_pin(token, message_id)

    messages = channel_messages(token, channel_id, 0)['messages']

    assert messages[2]['is_pinned']


##########################################################################################
###                                 MESSAGE_UNPIN TESTS                                ###
##########################################################################################

def test_message_unpin_invalid_message_id():
    '''
    Unpin message where message_id is invalid
    Expect InputError
    '''
    clear()
    user, _, channel_id = load_message().values()
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    message_id = messages[0]['message_id']
    message_pin(user['token'], message_id)

    with pytest.raises(InputError):
        message_unpin(user['token'], message_id + 100)


def test_message_unpin_message_already_unpinned():
    '''
    Unpin message where message is already unpinned
    Expect InputError
    '''
    clear()
    user, _, channel_id = load_message().values()
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    message_id = messages[0]['message_id']
    message_pin(user['token'], message_id)

    message_unpin(user['token'], message_id)
    with pytest.raises(InputError):
        message_unpin(user['token'], message_id)


def test_message_unpin_invalid_token():
    '''
    Unpin message when token is invalid
    Expect AccessError
    '''
    clear()
    user, _, channel_id = load_message().values()
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    message_id = messages[1]['message_id']
    message_pin(user['token'], message_id)

    with pytest.raises(AccessError):
        message_unpin(user['token']  + 'bad_token', message_id)


def test_message_unpin_user_not_in_channel():
    '''
    User who is not in the channel tries to unpin a message
    Expect AccessError
    '''
    clear()
    user, _, channel_id = load_message().values()
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    message_id = messages[1]['message_id']
    message_pin(user['token'], message_id)
    token = register('1')[1]

    with pytest.raises(AccessError):
        message_unpin(token, message_id)


def test_message_unpin_user_not_channel_owner():
    '''
    User who is in channel but not a channel owner tries to unpin a message
    Expect AccessError
    '''
    clear()
    user, _, channel_id = load_message().values()
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    message_id = messages[1]['message_id']
    message_pin(user['token'], message_id)
    token = register('1')[1]

    channel_join(token, channel_id)
    with pytest.raises(AccessError):
        message_unpin(token, message_id)


def test_message_unpin_user_flockr_owner_not_in_channel():
    '''
    User who is not in channel but is a global owner tries to unpin message
    Expect AccessError
    '''
    clear()
    user, _, channel_id = load_message().values()
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    message_id = messages[1]['message_id']
    message_pin(user['token'], message_id)

    channel_leave(user['token'], channel_id)

    with pytest.raises(AccessError):
        message_unpin(user['token'], message_id)


def test_message_unpin_user_flockr_owner_member_in_channel():
    '''
    User who is in channel as a normal member but is a global owner tries to unpin message
    This should work
    '''
    clear()
    user, _, channel_id = load_message().values()
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    message_id = messages[2]['message_id']
    message_pin(user['token'], message_id)

    u_id, token = register('2')
    channel_join(token, channel_id)
    channel_addowner(user['token'], channel_id, u_id)
    channel_removeowner(token, channel_id, user['u_id'])

    message_unpin(user['token'], message_id)
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    assert not messages[2]['is_pinned']


def test_message_unpin_user_channel_owner():
    '''
    User who is a channel owner tries to unpin message
    This should work
    '''
    clear()
    user, _, channel_id = load_message().values()
    messages = channel_messages(user['token'], channel_id, 0)['messages']
    message_id = messages[1]['message_id']
    message_pin(user['token'], message_id)

    u_id, token = register('1')

    channel_join(token, channel_id)

    channel_addowner(user['token'], channel_id, u_id)

    message_unpin(token, message_id)
    messages = channel_messages(token, channel_id, 0)['messages']
    assert not messages[1]['is_pinned']

##########################################################################################
###                               MESSAGE_SENDLATER TESTS                              ###
##########################################################################################
def message_timestamp_compare(messages_list, message_index, current_time, sent_time):
    '''
    Compares the time between the timestamp of the messages, and the predicted
    time that the message should be sent out
    Parameters:
        - messages_list: a list containing the messages
        - message_index: the index of the message in the list
        - current time: a variable that stores the 'current time'
        - sent_time: an expected delay that the function should work
    Returns:
        - True or False depending on assertion.
    '''
    predicted_time = (current_time + timedelta(seconds=sent_time)).timestamp()
    assert messages_list[message_index]['time_created'] - predicted_time < 0.5

def test_sendlater_input_error1():
    '''
    Test 1: Channel_id is not a valid channel
    Raise an InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    time_second = 10
    with pytest.raises(InputError):
        message_sendlater(token, channel_id + 2, 'a', \
            (datetime.now() + timedelta(seconds=time_second)).timestamp())

def test_sendlater_input_error2():
    '''
    Test 2: message is more than 1000 characters
    Raise an InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    time_second = 10
    with pytest.raises(InputError):
        message_sendlater(token, channel_id, 'a'*1001, \
            (datetime.now() + timedelta(seconds=time_second)).timestamp())

def test_sendlater_input_error3():
    '''
    Test 3: time_sent is a time in the past
    Raise an InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    time_second = -10
    with pytest.raises(InputError):
        message_sendlater(token, channel_id, 'a', \
            (datetime.now() + timedelta(seconds=time_second)).timestamp())

def test_sendlater_access_error():
    '''
    Test 4: the user writing the message hasn't joined the channel
    they're trying to post
    Raise an AccessError
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    time_second = 10
    with pytest.raises(AccessError):
        message_sendlater(token2, channel_id, 'a', \
            (datetime.now() + timedelta(seconds=time_second)).timestamp())

def test_sendlater_user_valid():
    '''
    Test 5: user is not a channel owner nor a flockr owner
    user is able to send messages at a later time.
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    time_second = 1
    current_time = datetime.now()
    message_sendlater(token2, channel_id, 'a', \
        (current_time + timedelta(seconds=time_second)).timestamp())

    sleep(time_second*2)
    messages_list = channel_messages(token1, channel_id, 0)['messages']
    message_timestamp_compare(messages_list, 0, current_time, time_second)
    assert len(messages_list) == 1
    assert messages_list[0]['message'] == "a"

def test_sendlater_channel_owner():
    '''
    Test 6: user is a channel owner but not a flockr owner
    user is able to send messages at a later time.
    '''
    clear()
    token1 = register('1')[1]
    u_id2, token2 = register('2')
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    channel_addowner(token1, channel_id, u_id2)
    time_second = 1
    current_time = datetime.now()
    message_sendlater(token2, channel_id, 'a', \
        (current_time + timedelta(seconds=time_second)).timestamp())

    sleep(time_second*2)
    messages_list = channel_messages(token1, channel_id, 0)['messages']
    message_timestamp_compare(messages_list, 0, current_time, time_second)
    assert len(messages_list) == 1
    assert len(messages_list) == 1
    assert messages_list[0]['message'] == "a"

def test_sendlater_flockr_owner():
    '''
    Test 7: user is a flockr owner
    user is able to send messages at a later time.
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    time_second = 1
    current_time = datetime.now()
    message_sendlater(token, channel_id, 'a', \
        (current_time + timedelta(seconds=time_second)).timestamp())

    sleep(time_second*2)
    messages_list = channel_messages(token, channel_id, 0)['messages']
    message_timestamp_compare(messages_list, 0, current_time, time_second)
    assert len(messages_list) == 1
    assert messages_list[0]['message'] == "a"

def test_sendlater_multi_time():
    '''
    Test 8: messages are scheduled to be sent at multiple
    different times
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    time_second1 = 1
    time_second2 = 2
    time_second3 = 3
    current_time = datetime.now()
    message_sendlater(token2, channel_id, 'a', \
        (current_time + timedelta(seconds=time_second1)).timestamp())
    message_sendlater(token2, channel_id, 'b', \
        (current_time + timedelta(seconds=time_second2)).timestamp())
    message_sendlater(token2, channel_id, 'c', \
        (current_time + timedelta(seconds=time_second3)).timestamp())

    sleep(time_second1 + time_second2 + time_second3)
    messages_list = channel_messages(token1, channel_id, 0)['messages']
    message_timestamp_compare(messages_list, 0, current_time, time_second3)
    message_timestamp_compare(messages_list, 1, current_time, time_second2)
    message_timestamp_compare(messages_list, 2, current_time, time_second1)

    assert len(messages_list) == 3
    assert messages_list[0]['message'] == "c"
    assert messages_list[1]['message'] == "b"
    assert messages_list[2]['message'] == "a"

def test_sendlater_multi_channel():
    '''
    Test 9: messages are scheduled to be sent in multiple
    different channels at the same scheduled time
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id1 = create_public_channel(token1, '1')
    channel_id2 = create_public_channel(token1, '1')
    channel_id3 = create_public_channel(token1, '1')
    channel_join(token2, channel_id1)
    channel_join(token2, channel_id2)
    channel_join(token2, channel_id3)

    time_second = 1
    current_time = datetime.now()
    message_sendlater(token2, channel_id1, 'a', \
        (current_time + timedelta(seconds=time_second)).timestamp())
    message_sendlater(token2, channel_id2, 'b', \
        (current_time + timedelta(seconds=time_second)).timestamp())
    message_sendlater(token2, channel_id3, 'c', \
        (current_time + timedelta(seconds=time_second)).timestamp())

    sleep(time_second*3)
    messages_list1 = channel_messages(token1, channel_id1, 0)['messages']
    messages_list2 = channel_messages(token1, channel_id2, 0)['messages']
    messages_list3 = channel_messages(token1, channel_id3, 0)['messages']

    message_timestamp_compare(messages_list1, 0, current_time, time_second)
    message_timestamp_compare(messages_list2, 0, current_time, time_second)
    message_timestamp_compare(messages_list3, 0, current_time, time_second)

    assert len(messages_list1) == 1
    assert len(messages_list2) == 1
    assert len(messages_list3) == 1

    assert messages_list1[0]['message'] == "a"
    assert messages_list2[0]['message'] == "b"
    assert messages_list3[0]['message'] == "c"

def test_sendlater_multi_user1():
    '''
    Test 10: messages are scheduled to be sent by multiple
    different users, all planning to sent at the same time
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    token3 = register('3')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    channel_join(token3, channel_id)
    time_second = 2
    current_time = datetime.now()
    message_sendlater(token1, channel_id, 'a', \
        (current_time + timedelta(seconds=time_second)).timestamp())
    message_sendlater(token2, channel_id, 'b', \
        (current_time + timedelta(seconds=time_second)).timestamp())
    message_sendlater(token3, channel_id, 'c', \
        (current_time + timedelta(seconds=time_second)).timestamp())

    messages_list = channel_messages(token1, channel_id, 0)['messages']
    assert len(messages_list) == 0

    sleep(time_second*4)
    messages_list = channel_messages(token1, channel_id, 0)['messages']
    assert len(messages_list) == 3

    message_timestamp_compare(messages_list, 0, current_time, time_second)
    message_timestamp_compare(messages_list, 1, current_time, time_second)
    message_timestamp_compare(messages_list, 2, current_time, time_second)

    all_msg = [x['message'] for x in messages_list]
    assert ['a', 'b', 'c'] == sorted(all_msg)

def test_sendlater_multi_user2():
    '''
    Test 11: messages are scheduled to be sent by multiple
    different users, planned at different times
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    token3 = register('3')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    channel_join(token3, channel_id)
    current_time = datetime.now()
    time_second1 = 5
    time_second2 = 10
    time_second3 = 15
    message_sendlater(token1, channel_id, 'a', \
        (current_time + timedelta(seconds=time_second1)).timestamp())
    message_sendlater(token2, channel_id, 'b', \
        (current_time + timedelta(seconds=time_second2)).timestamp())
    message_sendlater(token3, channel_id, 'c', \
        (current_time + timedelta(seconds=time_second3)).timestamp())
    messages_list = channel_messages(token1, channel_id, 0)['messages']
    assert len(messages_list) == 0

    sleep(time_second1*1.2)
    messages_list = channel_messages(token1, channel_id, 0)['messages']
    assert len(messages_list) == 1
    assert messages_list[0]['message'] == "a"

    sleep(time_second1*1.2)
    messages_list = channel_messages(token1, channel_id, 0)['messages']
    assert len(messages_list) == 2
    assert messages_list[0]['message'] == "b"
    assert messages_list[1]['message'] == "a"

    sleep(time_second1*1.2)
    messages_list = channel_messages(token1, channel_id, 0)['messages']
    assert len(messages_list) == 3
    assert messages_list[0]['message'] == "c"
    assert messages_list[1]['message'] == "b"
    assert messages_list[2]['message'] == "a"

    message_timestamp_compare(messages_list, 0, current_time, time_second3)
    message_timestamp_compare(messages_list, 1, current_time, time_second2)
    message_timestamp_compare(messages_list, 2, current_time, time_second1)
