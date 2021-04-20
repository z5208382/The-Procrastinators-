import pytest

from auth import *
from channel import *
from channels import *
from error import *
from helper_tests import *
from other import *

##########################################################################################
###                                 CHANNELS_LIST TESTS                                ###
##########################################################################################

def test_empty_channels_list():
    '''
    Test 1: Channels List is Empty; User in No channels
    '''
    clear()
    user1_token = register('1')[1]
    assert channels_list(user1_token) == {"channels": []}


def test_some_channels_list():
    '''
    Test 2: User only apart of some channels
    '''
    clear()
    user1_token = register('1')[1]
    user2_token = register('2')[1]
    channel_one = create_public_channel(user1_token, '1')
    channel_two = create_public_channel(user2_token, '2')

    channel1 = channel_details(user1_token, channel_one)
    channel2 = channel_details(user2_token, channel_two)
    # channel_list will only display the channel they are a member of
    assert channels_list(user1_token) == {
        "channels": [{"channel_id": channel_one, "name": channel1['name']}]
    }

    assert channels_list(user2_token) == {
        "channels": [{"channel_id": channel_two, "name": channel2['name']}]
    }

    # Add user 2 to channel 1 and check if User 2 now has 2 channels
    channel_join(user2_token, channel_one)
    assert channels_list(user2_token) == {
        "channels": [
            {"name": channel1['name'], "channel_id": channel_one},
            {"name": channel2['name'], "channel_id": channel_two}
            ]
    }


def test_display_public_private():
    '''
    Test 3: Ensure channels_list displays both public and private channels the user is in
    '''
    clear()
    user1_token = register('1')[1]

    channel_one = create_public_channel(user1_token, '1')
    channel_two = create_private_channel(user1_token, '2')

    channel1 = channel_details(user1_token, channel_one)
    channel2 = channel_details(user1_token, channel_two)

    # Display both public and private channels for user
    assert channels_list(user1_token) == {
        "channels": [
            {"name": channel1['name'], "channel_id": channel_one},
            {"name": channel2['name'], "channel_id": channel_two}
            ]
    }

    # User 2 creates a new channel
    user2_token = register('2')[1]
    channel_three = create_private_channel(user2_token, '3')
    channel3 = channel_details(user2_token, channel_three)

    # Display Private Channel for user2
    # shouldn't display channelOne and channelTwo
    assert channels_list(user2_token) == {
        "channels": [
            {"name": channel3['name'], "channel_id": channel_three}
            ]
    }


def test_all_channels_list():
    '''
    Test 4: Create new channel to check if channels list for
    user is updated (user also part of all channels)
    '''
    clear()
    user1_token = register('1')[1]

    channel_one = create_public_channel(user1_token, '1')
    channel_two = create_private_channel(user1_token, '2')

    channel1 = channel_details(user1_token, channel_one)
    channel2 = channel_details(user1_token, channel_two)

    # Display both public and private channels for user
    assert channels_list(user1_token) == {
        "channels": [
            {"name": channel1['name'], "channel_id": channel_one},
            {"name": channel2['name'], "channel_id": channel_two}
            ]
    }

    # Create a new channel and check if it is displayed in the user's channel list
    channel_three = create_public_channel(user1_token, '3')
    channel3 = channel_details(user1_token, channel_three)

    assert channels_list(user1_token) == {
        "channels": [
            {"name": channel1['name'], "channel_id": channel_one},
            {"name": channel2['name'], "channel_id": channel_two},
            {"name": channel3['name'], "channel_id": channel_three}
            ]
    }


##########################################################################################
###                             CHANNELS_LISTALL TESTS                                 ###
##########################################################################################

def test_empty_channels_list_all():
    '''
    Test 1: Channels List is Empty; No channels exist
    '''
    clear()
    user1_token = register('1')[1]
    assert channels_listall(user1_token) == {"channels": []}


def test_channels_list_all():
    '''
    Test 2: Display all channels despite user token entered as parameter
    '''
    clear()
    user1_token = register('1')[1]
    user2_token = register('2')[1]

    channel_one = create_public_channel(user1_token, '1')
    channel_two = create_public_channel(user1_token, '2')
    channel_three = create_public_channel(user1_token, '3')

    channel1 = channel_details(user1_token, channel_one)
    channel2 = channel_details(user1_token, channel_two)
    channel3 = channel_details(user1_token, channel_three)

    # Return all channels when giving token of user1
    assert channels_listall(user1_token) == {
        "channels": [
            {"name": channel1['name'], "channel_id": channel_one},
            {"name": channel2['name'], "channel_id": channel_two},
            {"name": channel3['name'], "channel_id": channel_three}
            ]
    }

    # Also return all channels when giving token of user2, despite user2 not being in the channels
    assert channels_listall(user2_token) == {
        "channels": [
            {"name": channel1['name'], "channel_id": channel_one},
            {"name": channel2['name'], "channel_id": channel_two},
            {"name": channel3['name'], "channel_id": channel_three}
            ]
    }


def test_channels_list_all_PublicPrivate():
    '''
    Test 3: Display both public and private channels
    '''
    clear()
    user1_token = register('1')[1]
    user2_token = register('2')[1]

    channel_public = create_public_channel(user1_token, '1')
    channel_private = create_private_channel(user1_token, '2')

    channel1 = channel_details(user1_token, channel_public)
    channel2 = channel_details(user1_token, channel_private)

    # Return all channels when giving token of user1, even if channel_private is not public
    assert channels_listall(user1_token) == {
        "channels": [
            {"name": channel1['name'], "channel_id": channel_public},
            {"name": channel2['name'], "channel_id": channel_private}
            ]
    }

    # Add user 2 to channel_public
    channel_join(user2_token, channel_public)

    # Return all channels given token of user2 (includung private channel),
    # even if user 2 is not a member of channel_private
    assert channels_listall(user2_token) == {
        "channels": [
            {"name": channel1['name'], "channel_id": channel_public},
            {"name": channel2['name'], "channel_id": channel_private}
            ]
    }


##########################################################################################
###                                 CHANNELS_CREATE TESTS                              ###
##########################################################################################

def test_invalid_channel_name_public():
    '''
    Test 1: Input Error when name of public channel is > 20 characters
    '''
    clear()
    user1_token = register('1')[1]
    channel_name = "Invalidname_inputerror"
    with pytest.raises(InputError):
        channels_create(user1_token, channel_name, is_public=True).get("channel_id")


def test_invalid_channel_name_private():
    '''
    Test 2: Input Error when name of private channel is > 20 characters
    '''
    clear()
    user1_token = register('1')[1]
    channel_name = "Invalidnameinputerror"
    with pytest.raises(InputError):
        channels_create(user1_token, channel_name, is_public=False).get("channel_id")


def test_valid_channel_public():
    '''
    Test 3: Valid Channel name given and Public Channel created successfully
    '''
    clear()
    user1_token = register('1')[1]
    channel_name = "validname"

    channel_valid = channels_create(user1_token, channel_name, is_public=True).get("channel_id")

    # Display channels of user to check if created successfully
    assert channels_list(user1_token) == {
        "channels": [{"channel_id": channel_valid, "name": channel_name, }]
    }

def test_valid_channel_private():
    '''
    Test 4: Valid Channel name given and Private Channel created successfully
    '''
    clear()
    user1_token = register('1')[1]
    channel_name = "validname"

    channel_valid = (channels_create(user1_token, channel_name, is_public=False)).get("channel_id")

    # Display channels of user to check if created successfully
    assert channels_list(user1_token) == {
        "channels": [{"name": channel_name, "channel_id": channel_valid}]
    }
