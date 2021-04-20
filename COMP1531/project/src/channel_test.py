##########################################################################################
###                           Tests for channel.py                                     ###
##########################################################################################
import pytest
from auth import *
from channel import *
from channels import *
from error import *
from message import *
from other import *
from helper_tests import *


##########################################################################################
###                                  CHANNEL_INVITE TESTS                              ###
##########################################################################################

# Test 1

def test_invite_invalid_token():
    '''
    Invalid token is inputs
    Raise AccessError
    '''
    clear()
    token1 = register('1')[1]
    u_id2 = register('2')[0]
    channel_id = create_public_channel(token1, '1')
    auth_logout(token1)
    with pytest.raises(AccessError):
        channel_invite(token1, channel_id, u_id2)

# Test 2

def test_invite_invalid_channel_id():
    '''
    Invalid channel_id is input
    Raise InputError
    '''
    clear()
    token1 = register('1')[1]
    u_id2 = register('2')[0]
    with pytest.raises(InputError):
        channel_invite(token1, 1, u_id2)

# Test 3

def test_invite_invalid_uid():
    '''
    Invalid u_id is inputs
    Raise InputError
    '''
    clear()
    token1 = register('1')[1]
    u_id2 = register('2')[0]
    channel_id = create_public_channel(token1, '1')
    with pytest.raises(InputError):
        channel_invite(token1, channel_id, u_id2*2)

# Test 4

def test_invite_access_error():
    '''
    A non-member user tries to invite someone to a channel
    Raise AccessError
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    u_id3 = register('3')[0]
    channel_id = create_public_channel(token1, '1')
    with pytest.raises(AccessError):
        channel_invite(token2, channel_id, u_id3)

# Test 5

def test_invite_valid1():
    '''
    Ensure channel owner is able to invite someone to a channel
    '''
    clear()
    token1 = register('1')[1]
    u_id2 = register('2')[0]
    channel_id = create_public_channel(token1, '1')
    channel_invite(token1, channel_id, u_id2)
    members = channel_details(token1, channel_id)['all_members']
    assert len(members) == 2

# Test 6

def test_invite_valid2():
    '''
    Ensure both a channel owner and channel member are able to invite other
    users to the channel
    '''
    clear()
    token1 = register('1')[1]
    u_id2, token2 = register('2')
    u_id3 = register('3')[0]
    channel_id = create_public_channel(token1, '1')
    channel_invite(token1, channel_id, u_id2)
    channel_invite(token2, channel_id, u_id3)
    members = channel_details(token1, channel_id)['all_members']
    assert len(members) == 3


def test_invite_flockr_owner():
    '''
    Channel owner invites a flockr owner
    '''
    clear()
    owner_id = register('0')[0]
    user_token = register('1')[1]
    pub = create_public_channel(user_token, 'hello')
    priv = create_private_channel(user_token, 'hello')
    channel_invite(user_token, pub, owner_id)
    channel_invite(user_token, priv, owner_id)
    for channel in [pub, priv]:
        details = channel_details(user_token, channel)
        assert len(details['all_members']) == 2
        assert len(details['owner_members']) == 2

# Test 7

def test_invite_already_member():
    '''
    Authorised user invites someone who is already in the channel
    Test user isn't added again
    '''
    clear()
    token1 = register('1')[1]
    u_id2, token2 = register('2')
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    channel_invite(token1, channel_id, u_id2)
    members = channel_details(token1, channel_id)['all_members']
    assert len(members) == 2

##########################################################################################
###                                 CHANNEL_DETAILS TESTS                              ###
##########################################################################################

# Test 1

def test_details_invalid_token():
    '''
    Invalid token is input
    Raise AccessError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    auth_logout(token)
    with pytest.raises(AccessError):
        channel_details(token, channel_id)

# Test 2

def test_details_invalid_channel_id():
    '''
    Invalid channel_id is input
    Raise InputError
    '''
    clear()
    token = register('1')[1]
    with pytest.raises(InputError):
        channel_details(token, 1)

# Test 3

def test_details_access_error():
    '''
    A non-member user tries to get channel details
    Raise AccessError
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    with pytest.raises(AccessError):
        channel_details(token2, channel_id)

# Test 4

def test_details_valid_one_user():
    '''
    Channel only has one member
    Ensure correct channel details are returned
    '''
    clear()
    _, token, member = register('1', 1)
    member['profile_img_url'] = ''
    channel_id = create_public_channel(token, '1')
    details = channel_details(token, channel_id)
    assert details['name'] == "Channel1"
    assert details['owner_members'] == [member]
    assert details['all_members'] == [member]

# Test 5

def test_details_valid_multiple_users():
    '''
    Channel has multiple users
    Ensure correct channel details are returned
    '''
    clear()
    register('0')
    _, token1, member1 = register('1', 1)
    member1['profile_img_url'] = ''
    u_id2, token2, member2 = register('2', 1)
    member2['profile_img_url'] = ''
    u_id3, _, member3 = register('3', 1)
    member3['profile_img_url'] = ''
    u_id4, _, member4 = register('4', 1)
    member4['profile_img_url'] = ''
    channel_id = create_public_channel(token1, '1')
    channel_invite(token1, channel_id, u_id2)
    channel_invite(token1, channel_id, u_id3)
    channel_invite(token1, channel_id, u_id4)
    details = channel_details(token2, channel_id)
    assert details['name'] == "Channel1"
    assert details['owner_members'] == [member1]
    assert details['all_members'] == [member1, member2, member3, member4]

# Test 6

def test_details_valid_multiple_channels():
    '''
    Two different channels both have two users, with one user in both channels
    Ensure both channel's details are returned
    '''
    clear()
    register('0')
    u_id1, token1, member1 = register('1', 1)
    member1['profile_img_url'] = ''
    _, token2, member2 = register('2', 1)
    member2['profile_img_url'] = ''
    u_id3, _, member3 = register('3', 1)
    member3['profile_img_url'] = ''

    channel_id1 = create_public_channel(token1, '1')
    channel_id2 = create_public_channel(token2, '2')

    channel_invite(token1, channel_id1, u_id3)

    channel_invite(token2, channel_id2, u_id1)
    details1 = channel_details(token1, channel_id1)

    assert details1['name'] == "Channel1"
    assert details1['owner_members'] == [member1]
    assert details1['all_members'] == [member1, member3]
    details2 = channel_details(token1, channel_id2)

    assert details2['name'] == "Channel2"
    assert details2['owner_members'] == [member2]
    assert details2['all_members'] == [member2, member1]


##########################################################################################
###                                 CHANNEL_MESSAGE TESTS                              ###
##########################################################################################

# Test 1

def test_messages_invalid_token():
    '''
    Invalid token is input
    Raise AccessError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_send(token, channel_id, "Hello")
    auth_logout(token)
    with pytest.raises(AccessError):
        channel_messages(token, channel_id, 0)

# Test 2

def test_messages_invalid_channel_id():
    '''
    Invalid channel_id is input
    Raise InputError
    '''
    clear()
    token = register('1')[1]
    with pytest.raises(InputError):
        channel_messages(token, 1, 0)

# Test 3

def test_messages_invalid_start():
    '''
    Start is greater than the number of messages
    Raise InputError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_send(token, channel_id, "Hello")
    with pytest.raises(InputError):
        channel_messages(token, channel_id, 2)

# Test 4

def test_messages_access_error():
    '''
    Authorised user is not a member of the channel
    Raise AccessError
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    with pytest.raises(AccessError):
        channel_messages(token2, channel_id, 0)

# Test 5

def test_messages_start0_more_than_50():
    '''
    If start is 0 and there are more than 50 messages
    Ensure correct return
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    for _ in range(0, 70):
        message_send(token, channel_id, "Hi")
    data = channel_messages(token, channel_id, 0)
    assert len(data['messages']) == 50
    assert data['start'] == 0
    assert data['end'] == 50

# Test 6

def test_messages_start_positive_more_than_50():
    '''
    If start is greater than 0 and there are more than 50 messages
    Ensure correct return
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    for _ in range(0, 70):
        message_send(token, channel_id, "Hi")
    data = channel_messages(token, channel_id, 10)
    assert len(data['messages']) == 50
    assert data['start'] == 10
    assert data['end'] == 60

# Test 7

def test_messages_start_0_less_than_50():
    '''
    If start is 0 and there are less than 50 messages
    Ensure correct return
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    for _ in range(0, 49):
        message_send(token, channel_id, "Hi")
    data = channel_messages(token, channel_id, 0)
    assert len(data['messages']) == 49
    assert data['start'] == 0
    assert data['end'] == -1

# Test 8

def test_messages_start_positive_less_than_50():
    '''
    If start is greater than 0 and there are less than 50 messages
    Ensure correct return
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    for _ in range(0, 20):
        message_send(token, channel_id, "Hi")
    data = channel_messages(token, channel_id, 10)
    assert len(data['messages']) == 10
    assert data['start'] == 10
    assert data['end'] == -1

# Test 9

def test_messages_small():
    '''
    Test with three different messages
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    message_send(token, channel_id, "Hello")
    message_send(token, channel_id, "Hi")
    message_send(token, channel_id, "Bye")
    data = channel_messages(token, channel_id, 2)
    message = data['messages']
    assert message[0]['message'] == "Hello"
    assert data['start'] == 2
    assert data['end'] == -1

##########################################################################################
###                                 CHANNEL_LEAVE TESTS                                ###
##########################################################################################

# Test 1

def test_leave_invalid_token():
    '''
    Invalid token is input
    Raise AccessError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    auth_logout(token)
    with pytest.raises(AccessError):
        channel_leave(token, channel_id)

# Test 2

def test_leave_invalid_channel_id():
    '''
    Invalid channel_id is input
    Raise InputError
    '''
    clear()
    token = register('1')[1]
    with pytest.raises(InputError):
        channel_leave(token, 1)

# Test 3

def test_leave_access_error():
    '''
    If a non-member user tries to leave a channel
    Raise AccessError
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    with pytest.raises(AccessError):
        channel_leave(token2, channel_id)

# Test 4

def test_leave_members():
    '''
    Test members are removed from the channel when they leave
    '''
    clear()
    _, token1, member1 = register('1', 1)
    member1['profile_img_url'] = ''
    u_id2, token2, _ = register('2', 1)
    u_id3, _, member3 = register('3', 1)
    member3['profile_img_url'] = ''
    channel_id = create_public_channel(token1, '1')
    channel_invite(token1, channel_id, u_id2)
    channel_invite(token1, channel_id, u_id3)
    channel_leave(token2, channel_id)
    details = channel_details(token1, channel_id)
    assert details['all_members'] == [member1, member3]

# Test 5

def test_leave_new_owner():
    '''
    If there is only one member left in a channel, they become the owner
    '''
    clear()
    _, token1, _ = register('1', 1)
    u_id2, token2, member2 = register('2', 1)
    member2['profile_img_url'] = ''
    channel_id = create_public_channel(token1, '1')
    channel_invite(token1, channel_id, u_id2)
    channel_leave(token1, channel_id)
    details = channel_details(token2, channel_id)
    assert details['owner_members'] == [member2]

# Test 6

def test_leave_all_members():
    '''
    All members of a channel leave
    Check that the channel is removed and no other users can join it
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    channel_leave(token, channel_id)
    with pytest.raises(InputError):
        channel_join(token, channel_id)

# Test 6

def test_leave_owner():
    '''
    The only owner of a channel leaves it
    Oldest member becomes the new owner
    '''
    clear()
    register('0')
    token1 = register('1', 1)[1]
    u_id2, token2, member2 = register('2', 1)
    member2['profile_img_url'] = ''
    u_id3 = register('3', 1)[0]
    channel_id = create_public_channel(token1, '1')
    channel_invite(token1, channel_id, u_id2)
    channel_invite(token1, channel_id, u_id3)
    channel_leave(token1, channel_id)
    details = channel_details(token2, channel_id)
    assert details['owner_members'] == [member2]
    assert len(details['all_members']) == 2


##########################################################################################
###                                 CHANNEL_JOIN TESTS                                 ###
##########################################################################################

# Test 1

def test_join_invalid_token():
    '''
    Invalid token is input
    Raise AccessError
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    auth_logout(token)
    with pytest.raises(AccessError):
        channel_join(token, channel_id)

# Test 2

def test_join_invalid_channel_id():
    '''
    Invalid channel_id is input
    Raise InputError
    '''
    clear()
    token = register('1')[1]
    with pytest.raises(InputError):
        channel_join(token, 1)

# Test 3

def test_join_access_error():
    '''
    A user tries to join a private channel
    Raise AccessError
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_private_channel(token1, '1')
    with pytest.raises(AccessError):
        channel_join(token2, channel_id)

# Test 4

def test_join_valid_one_channel():
    '''
    Test a user is able to join a channel
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_public_channel(token1, '1')
    channel_join(token2, channel_id)
    details = channel_details(token2, channel_id)
    assert len(details['all_members']) == 2

# Test 5

def test_join_valid_multiple_channels():
    '''
    Test multiple users are able to join multiple channels
    '''
    clear()
    _, token1, member1 = register('1', 1)
    member1['profile_img_url'] = ''
    _, token2, member2 = register('2', 1)
    member2['profile_img_url'] = ''
    _, token3, member3 = register('3', 1)
    member3['profile_img_url'] = ''
    channel_id1 = create_public_channel(token1, '1')
    channel_id2 = create_public_channel(token2, '2')
    channel_join(token3, channel_id1)
    channel_join(token1, channel_id2)
    channel1 = channel_details(token1, channel_id1)
    assert channel1['all_members'] == [member1, member3]
    channel2 = channel_details(token2, channel_id2)
    assert channel2['all_members'] == [member2, member1]

# Test 6

def test_join_private_channel_global_owner():
    '''
    Ensure global owner successfully joins private channel
    '''
    clear()
    token1 = register('1')[1]
    token2 = register('2')[1]
    channel_id = create_private_channel(token2, '1')
    channel_join(token1, channel_id)
    assert len(channel_details(token1, channel_id)['all_members']) == 2

# Test 7

def test_join_user_in_channel():
    '''
    User joins a channel they are already in
    Test that user is not added twice
    '''
    clear()
    token = register('1')[1]
    channel_id = create_public_channel(token, '1')
    channel_join(token, channel_id)
    assert len(channel_details(token, channel_id)['all_members']) == 1

##########################################################################################
###                                 CHANNEL_ADDOWNER TESTS                             ###
##########################################################################################

# Test 1

def addowner_invalid_token(is_public):
    '''
    Test addowner function with invalid token.
    Will raise AccessError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''
    token1 = register('1')[1]
    u_id2 = register('2')[0]
    if is_public:
        channel_id = create_public_channel(token1, '1')
    else:
        channel_id = create_private_channel(token1, '1')

    with pytest.raises(AccessError):
        channel_addowner(token1 * 2, channel_id, u_id2)

# Test 2

def test_addowner_invalid_token_pub():
    '''
    Test addowner function,
    with invalid token for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_invalid_token(True)

# Test 3

def test_addowner_invalid_token_priv():
    '''
    Test addowner function,
    with invalid token for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_invalid_token(False)

# Test 4

def addowner_invalid_channel_id(is_public):
    '''
    Test addowner function with invalid channel id.
    Will raise InputError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''
    token = register('1')[1]
    u_id1 = register('2')[0]

    if is_public:
        channel_id = create_public_channel(token, '1')
    else:
        channel_id = create_private_channel(token, '1')

    channel_invite(token, channel_id, u_id1)

    with pytest.raises(InputError):
        channel_addowner(token, channel_id + 100, u_id1)

# Test 5

def test_addowner_invalid_channel_id_pub():
    '''
    Test addowner function,
    with invalid channel id for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_invalid_channel_id(True)

# Test 6

def test_addowner_invalid_channel_id_priv():
    '''
    Test addowner function,
    with invalid channel id for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_invalid_channel_id(False)

# Test 7

def addowner_invalid_uid(is_public):
    '''
    Test addowner function with invalid user id.
    Will raise InputError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''
    token1 = register('1')[1]
    u_id2 = register('2')[0]
    if is_public:
        channel_id = create_public_channel(token1, '1')
    else:
        channel_id = create_private_channel(token1, '1')

    u_id2 *= 2
    with pytest.raises(InputError):
        channel_addowner(token1, channel_id, u_id2)

# Test 8

def test_addowner_invalid_uid_pub():
    '''
    Test addowner function,
    with invalid user id for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_invalid_uid(True)

# Test 9

def test_addowner_invalid_uid_priv():
    '''
    Test addowner function,
    with invalid user id for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_invalid_uid(False)

# Test 10

def addowner_uid_is_owner(is_public):
    '''
    Test addowner function when user is already an owner.
    Will raise InputError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''
    u_id, token = register('1')
    if is_public:
        channel_id = create_public_channel(token, '1')
    else:
        channel_id = create_private_channel(token, '1')

    with pytest.raises(InputError):
        channel_addowner(token, channel_id, u_id)

# Test 11

def test_addowner_uid_is_owner_pub():
    '''
    Test addowner function,
    user is already owner for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_uid_is_owner(True)

# Test 12

def test_addowner_uid_is_owner_priv():
    '''
    Test addowner function,
    user is already owner for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_uid_is_owner(False)

# Test 13

def addowner_access_error(is_public):
    '''
    Test addowner function when user not an owner of channel and flockr.
    Will raise AccessError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''
    register('0') # claim u_id : 0
    token1 = register('1')[1]
    u_id2, token2 = register('2')
    if is_public:
        channel_id = create_public_channel(token1, '1')
    else:
        channel_id = create_private_channel(token1, '1')

    with pytest.raises(AccessError):
        channel_addowner(token2, channel_id, u_id2)

# Test 14

def test_addowner_access_error_pub():
    '''
    Test addowner function,
    user not channel and flockr owner public channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_access_error(True)

# Test 15

def test_addowner_access_error_priv():
    '''
    Test addowner function,
    user not channel and flockr owner private channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_access_error(False)

# Test 16

def addowner_valid(is_public):
    '''
    Test addowner function with valid inputs is added correctly
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''
    register('0')
    token1 = register('1')[1]
    u_id2, token2 = register('2')

    if is_public:
        channel_id = create_public_channel(token1, '1')
    else:
        channel_id = create_private_channel(token1, '1')

    channel_invite(token1, channel_id, u_id2)
    channel_addowner(token1, channel_id, u_id2)
    owners = channel_details(token2, channel_id)['owner_members']
    for owner in owners:
        if owner['u_id'] == u_id2:
            break
    else:
        assert False, f"u_id({u_id2}) not in channel({channel_id})"

# Test 17

def test_addowner_valid_pub():
    '''
    Test addowner function,
    with valid input for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_valid(True)

# Test 18

def test_addowner_valid_priv():
    '''
    Test addowner function,
    with valid input for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_valid(False)

# Test 19
# owner is added if the authorised user is a flockr owner
# authorised user is not part of the channel
# tests both public and private channels
def addowner_owns_flockr(is_public):
    '''
    Test addowner function with owner user id is correctly added.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''
    token0 = register('0')[1]
    token1 = register('1')[1]
    u_id2 = register('2')[0]

    if is_public:
        c_id = create_public_channel(token1, '1')
    else:
        c_id = create_private_channel(token1, '1')

    channel_invite(token1, c_id, u_id2)
    channel_addowner(token0, c_id, u_id2)

    owners = channel_details(token1, c_id)['owner_members']
    for owner in owners:
        if owner['u_id'] == u_id2:
            break
    else:
        assert False, f"u_id({u_id2} not added"

# Test 20

def test_addowner_owns_flockr_pub():
    '''
    Test addowner function,
    flockr owner adds an owner for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_owns_flockr(True)

# Test 21

def test_addowner_owns_flockr_priv():
    '''
    Test addowner function,
    flockr owner adds an owner for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    addowner_owns_flockr(False)


##########################################################################################
###                                 CHANNEL_REMOVEOWNER TESTS                          ###
##########################################################################################

# Test 1
def removeowner_invalid_token(is_public):
    '''
    Test removeowner function with invalid token.
    Will raise AccessError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''
    u_id1, token1 = register('1')
    token2 = register('2')[1]
    if is_public:
        channel = create_public_channel(token1, '1')
    else:
        channel = create_private_channel(token1, '1')

    with pytest.raises(AccessError):
        channel_removeowner(token2 * 2, channel, u_id1)

# Test 2

def test_removeowner_invalid_token_pub():
    '''
    Test removeowner function,
    with invalid token for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_invalid_token(True)

# Test 3

def test_removeowner_invalid_token_priv():
    '''
    Test removeowner function,
    with invalid token for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_invalid_token(False)


# Test 4

def removeowner_invalid_channel_id(is_public):
    '''
    Test removeowner function with invalid channel id.
    Will raise InputError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''
    register('0')
    u_id, token = register('1')
    u_id1, token1 = register('2')

    if is_public:
        channel = create_public_channel(token, '1')
    else:
        channel = create_private_channel(token, '1')

    channel_invite(token, channel, u_id1)
    channel_addowner(token, channel, u_id1)

    with pytest.raises(InputError):
        channel_removeowner(token1, channel + 999, u_id)

# Test 5

def test_removeowner_invalid_channel_id_pub():
    '''
    Test removeowner function,
    with invalid channel id for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_invalid_channel_id(True)

# Test 6

def test_removeowner_invalid_channel_id_priv():
    '''
    Test removeowner function,
    with invalid channel id for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_invalid_channel_id(False)

# Test 7

def removeowner_invalid_uid(is_public):
    '''
    Test removeowner function with invalid user id.
    Will raise InputError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''
    token1 = register('1')[1]
    u_id2 = register('2')[0]
    if is_public:
        channel = create_public_channel(token1, '1')
    else:
        channel = create_private_channel(token1, '1')

    u_id2 *= 2
    with pytest.raises(InputError):
        channel_removeowner(token1, channel, u_id2)

# Test 8

def test_removeowner_invalid_uid_pub():
    '''
    Test removeowner function,
    with invalid user id for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_invalid_uid(True)

# Test 9

def test_removeowner_invalid_uid_priv():
    '''
    Test removeowner function,
    with invalid user id for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_invalid_uid(False)

# Test 10

def removeowner_uid_is_not_owner(is_public):
    '''
    Test removeowner function when user id not an owner.
    Will raise InputError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''
    register('0')
    token1 = register('1')[1]
    u_id2 = register('2')[0]
    if is_public:
        channel = create_public_channel(token1, '1')
    else:
        channel = create_private_channel(token1, '1')

    channel_invite(token1, channel, u_id2)
    with pytest.raises(InputError):
        channel_removeowner(token1, channel, u_id2)

# Test 11

def test_removeowner_uid_is_not_owner_pub():
    '''
    Test removeowner function,
    user id not an owner for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_uid_is_not_owner(True)

# Test 12

def test_removeowner_uid_is_not_owner_priv():
    '''
    Test removeowner function,
    user id not an owner for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_uid_is_not_owner(False)

# Test 13

def removeowner_access_error(is_public):
    '''
    Test removeowner function when user not owner of channel and flockr.
    Will raise AccessError.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''
    register('0') # claim u_id : 0
    u_id1, token1 = register('1')
    token2 = register('2')[1]
    if is_public:
        channel = create_public_channel(token1, '1')
    else:
        channel = create_private_channel(token1, '1')

    with pytest.raises(AccessError):
        channel_removeowner(token2, channel, u_id1)

# Test 14

def test_removeowner_access_error_pub():
    '''
    Test removeowner function,
    user does not own channel and flockr for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_access_error(True)

# Test 15

def test_removeowner_access_error_priv():
    '''
    Test removeowner function,
    user does not own channel and flockr for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_access_error(False)

# Test 16
# owner is removed for both public and private channels
def removeowner_valid(is_public):
    '''
    Test removeowner function with valid inputs is added correctly.
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''
    register('0')
    u_id1, token1 = register('1')
    u_id2, token2 = register('2')

    if is_public:
        channel_id = create_public_channel(token1, '1')
    else:
        channel_id = create_private_channel(token1, '1')

    channel_invite(token1, channel_id, u_id2)
    channel_addowner(token1, channel_id, u_id2)

    owners = channel_details(token2, channel_id)['owner_members']
    initial_count = len(owners)

    channel_removeowner(token2, channel_id, u_id1)

    owners = channel_details(token2, channel_id)['owner_members']
    final_count = len(owners)
    assert final_count + 1 == initial_count

# Test 17

def test_removeowner_pub():
    '''
    Test removeowner function,
    with valid inputs for public channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_valid(True)

# Test 18

def test_removeowner_priv():
    '''
    Test removeowner function,
    with valid inputs for private channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_valid(False)

# Test 19

def removeowner_owns_flockr(is_public):
    '''
    Test removeowner function when user owns flockr but not in channel
    Checks if a channel owner is removed by the flockr owner correctly
    Can test public and private channels
    Parameter: is_public(Boolean)
    Returns: None
    '''
    token0 = register('0')[1]
    u_id1, token1 = register('1')
    u_id2, token2 = register('2')

    if is_public:
        c_id = create_public_channel(token1, '1')
    else:
        c_id = create_private_channel(token1, '1')

    channel_invite(token1, c_id, u_id2)
    channel_addowner(token1, c_id, u_id2)

    owners = channel_details(token2, c_id)['owner_members']
    initial_count = len(owners)

    channel_removeowner(token0, c_id, u_id1)

    owners = channel_details(token2, c_id)['owner_members']
    final_count = len(owners)

    assert final_count + 1 == initial_count

# Test 20

def test_removeowner_owns_flockr_pub():
    '''
    Test removeowner function,
    when user owns flockr but not in channel removes another channel owner in a public channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_owns_flockr(True)

# Test 21

def test_removeowner_owns_flockr_priv():
    '''
    Test removeowner function,
    when user owns flockr but not in channel removes another channel owner in a private channel
    Parameter: None
    Returns: None
    '''
    clear()
    removeowner_owns_flockr(False)
