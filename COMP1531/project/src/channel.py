##########################################################################################
###                           Implementation for channel.py                            ###
##########################################################################################
from data import *
from error import *
from helper import *

global users
global channels
global messages

############################################################################################
###                                  CHANNEL_INVITE                                      ###
############################################################################################

def channel_invite(token, channel_id, u_id):
    '''
    Invites a user (with user id u_id) to join a channel with ID channel_id.
    Once invited the user is added to the channel immediately.
    Parameters:
        token, channel_id, u_id
    Returns:
        {}
    Exception:
        AccessError
            - Invalid token
            - User performing action not in channel
        InputError
            - Invalid channel id
            - Invalid u_id
    '''
    c_index = check_channel_valid(channel_id)
    auth_id = get_user_id(token)
    check_user_in_channel(auth_id, channel_id)
    invite_index = get_user_index(u_id)


    if not u_id in channels[c_index]['all_members']:
        if user_flockr_owner(u_id):
            channels[c_index]['owner_members'].append(u_id)
        channels[c_index]['all_members'].append(u_id)
        users[invite_index]['channels'].append(channel_id)

    return {}

##########################################################################################
###                                   CHANNEL_DETAILS                                  ###
##########################################################################################

def channel_details(token, channel_id):
    '''
    Given a channel_id that the authorised user is part of,
    provide basic details about the channel
    Parameters:
        token, channel_id
    Returns:
        {name, [owner_members], [all_members]}
    Exception:
        AccessError
            - Invalid token
            - User performing action not in channel
        InputError
            - Invalid channel id
    '''
    c_index = check_channel_valid(channel_id)
    auth_id = get_user_id(token)
    check_user_in_channel(auth_id, channel_id)

    owner_members_list = []
    for owner_id in channels[c_index]['owner_members']:
        for user in users:
            if owner_id == user['u_id']:
                owner_dict = {
                    "u_id": user["u_id"],
                    "name_first": user["name_first"],
                    "name_last": user["name_last"],
                    "profile_img_url": user["profile_img_url"]
                }
                owner_members_list.append(owner_dict)

    members_list = []
    for member_id in channels[c_index]['all_members']:
        for user in users:
            if member_id == user['u_id']:
                member_dict = {
                    "u_id": user["u_id"],
                    "name_first": user["name_first"],
                    "name_last": user["name_last"],
                    "profile_img_url": user["profile_img_url"]
                }
                members_list.append(member_dict)

    return {
        'name': channels[c_index]['name'],
        'owner_members': owner_members_list,
        'all_members': members_list,
    }

##########################################################################################
###                                   CHANNEL_MESSAGES                                 ###
##########################################################################################

def channel_messages(token, channel_id, start):
    '''
    Find all messages in the channel and store them in a list
    List is reversed to return the most recent messages
    End is always start + 50 unless least recent messages in channel have been returned
    Parameter:
        token, channel_id, start
    Returns:
        {[messages], start, end}
    Exception:
        AccessError
            - Invalid token
            - User performing action is not in channel
        InputError
            - Invalid channel id
            - Start value greater than total messages in channel
    '''
    check_channel_valid(channel_id)
    auth_id = get_user_id(token)
    check_user_in_channel(auth_id, channel_id)

    end = start + 50

    channel_messages_list = []
    for m in messages:
        if m['channel_id'] == channel_id:
            if start > len(m['messages']):
                raise InputError(description="Start greater than number of messages")
            channel_messages_list = list(m['messages'])
            channel_messages_list.reverse()

    if len(channel_messages_list) <= 50:
        end = -1

    output = channel_messages_list[start:end] if end > 0 else \
        channel_messages_list[start:]

    return {
        'messages': change_user_reacted(output, auth_id),
        'start': start,
        'end': end,
    }

##########################################################################################
###                                   CHANNEL_LEAVE                                    ###
##########################################################################################

def channel_leave(token, channel_id):
    '''
    Given a channel_id, the user (given by token) is removed as a member of the channel
    Parameters:
        token, channel_id
    Returns:
        {}
    Exception:
        AccessError
            - Invalid token
            - User performing action not in channel
        InputError
            - Invalid channel id
    '''
    auth_id = get_user_id(token)
    c_index = check_channel_valid(channel_id)
    check_user_in_channel(auth_id, channel_id)

    u_index = get_user_index(auth_id)

    channels[c_index]['all_members'].remove(auth_id)
    users[u_index]['channels'].remove(channel_id)
    if check_user_owner(auth_id, channel_id):
        channels[c_index]['owner_members'].remove(auth_id)

    # if channel has 0 members, remove channel from database
    if len(channels[c_index]['all_members']) == 0:
        channels.remove(channels[c_index])

    # if channel has 1 member, make that member an owner
    elif len(channels[c_index]['all_members']) == 1:
        channels[c_index]['owner_members'] = channels[c_index]['all_members']

    # if the only channel owner leaves, make the oldest member an owner
    elif len(channels[c_index]['owner_members']) == 0:
        channels[c_index]['owner_members'].append(channels[c_index]['all_members'][0])

    return {}

##########################################################################################
###                                     CHANNEL_JOIN                                   ###
##########################################################################################

def channel_join(token, channel_id):
    '''
    Given a channel_id that user can join, add them to the channel
    Parameters:
        token, channel_id
    Returns:
        {}
    Exception:
        AccessError
            - Invalid token
            - Channel is private and user performing action is not a global owner
        InputError
            - Invalid channel id
    '''

    auth_id = get_user_id(token)
    c_index = check_channel_valid(channel_id)
    u_index = get_user_index(auth_id)

    if not auth_id in channels[c_index]['all_members']:
        if (channels[c_index]['is_public'] == 0 and not user_flockr_owner(auth_id)):
            raise AccessError(description="Invalid permission. Channel is not \
                                         public and user is not a flockr owner")
        else:
            if user_flockr_owner(auth_id):
                channels[c_index]['owner_members'].append(auth_id)

            channels[c_index]['all_members'].append(auth_id)
            users[u_index]['channels'].append(channel_id)

    return {}

##########################################################################################
###                                   CHANNEL_ADDOWNER                                 ###
##########################################################################################

def channel_addowner(token, channel_id, u_id):
    '''
    Authorised user (from token) makes user with u_id an owner of the channel
    Parameters:
        token, channel_id, u_id
    Returns:
        {}
    Exception:
        AccessError
            - Invalid token
            - User performing action is not a channel owner or flockr owner
        InputError
            - Invalid channel id
            - Invalid u_id
            - User being invited is already a channel owner
    '''

    auth_id = get_user_id(token)
    c_index = check_channel_valid(channel_id)
    get_user_index(u_id)

    if check_user_owner(u_id, channel_id):
        raise InputError(description="User to add as owner is already an owner")

    if not (check_user_owner(auth_id, channel_id) or user_flockr_owner(auth_id)):
        raise AccessError(description="Invalid permission. User is not a \
                                       channel owner or a flockr owner")
    else:
        channels[c_index]['owner_members'].append(u_id)

    return {}

##########################################################################################
###                                   CHANNEL_REMOVEOWNER                              ###
##########################################################################################

def channel_removeowner(token, channel_id, u_id):
    '''
    Authorised user (from token) removes owner permissions from user with u_id
    Parameters:
        token, channel_id, u_id
    Returns:
        {}
    Exception:
        AccessError
            - Invalid token
            - Action is performed by a user that is not a channel owner or flockr owner
        InputError
            - Invalid channel id
            - Invalid u_id
            - User being removed as owner is not an owner
    '''

    auth_id = get_user_id(token)
    c_index = check_channel_valid(channel_id)
    get_user_index(u_id)

    if not check_user_owner(u_id, channel_id):
        raise InputError(description="User to remove is not an owner")
    elif not (check_user_owner(auth_id, channel_id) or user_flockr_owner(auth_id)):
        raise AccessError(description="Insufficient permission. User is not a \
                                       channel owner or a flockr owner")
    else:
        channels[c_index]['owner_members'].remove(u_id)

    return {}
