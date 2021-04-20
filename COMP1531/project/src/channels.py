'''
Implementation for channels.py
'''
from datetime import datetime
from error import InputError
from helper import get_user_id
from data import users, channels, messages, trivias, default_UNSW

##########################################################################################
###                                     CHANNELS_LIST                                  ###
##########################################################################################

def channels_list(token):
    '''
    Provides a list of all channels (and associated details) that the authorised user is part of
    Method:
        - Gets user_id from token
        - loop through channels database to find channels that match with user_id
        - append dictionary conatining channel details to list
    '''

    user_id = get_user_id(token)
    channel_list = []
    for channel in channels:
        if user_id in channel['all_members']:
            channel_dict = {
                'channel_id' : channel['channel_id'],
                'name' : channel['name'],
            }
            channel_list.append(channel_dict)
    return {
        'channels': channel_list
    }


##########################################################################################
###                                   CHANNELS_LISTALL                                 ###
##########################################################################################

def channels_listall(token):
    '''
    Provides a list of all channels (and their associated details)
    Method:
        - Check if token is valid
        - loop through all channels and append dictionary containing channel
            details to list of all channels
    '''
    get_user_id(token)
    channel_list = []
    for channel in channels:
        channel_dict = {
            "channel_id": channel["channel_id"], "name": channel["name"]
        }
        channel_list.append(channel_dict)
    return {
        'channels': channel_list
    }

##########################################################################################
###                                   CHANNELS_CREATE                                  ###
##########################################################################################

def channels_create(token, name, is_public):
    '''
    Creates a new channel with that name that is either a public or private channel
    Method:
        - Gets user_id from token
        - check to make sure length of name is not > 20 characters
        - channel id is the index number in the channels list in database
        - Appends all channel info to channels database
        - Appends empty messages list to messages database
        - Add channel_id to users database
    '''

    user_id = get_user_id(token)
    if len(name) > 20:
        raise InputError(description=f"Channel Name: {name} is invalid (length greated than 20))")

    channel_id = len(channels)
    new_channel = {
        "channel_id": channel_id,
        "name": name,
        "is_public": is_public,
        "owner_members": [user_id],
        "all_members": [user_id],
        "standup": datetime.now().timestamp()
    }
    channels.append(new_channel)

    message_dict = {
        'channel_id': channel_id,
        'messages': [],
        'standup_messages': ""}
    messages.append(message_dict)

    global trivias
    global default_UNSW
    trivias.append({
        'channel_id': channel_id,
        'trivia_active': False,
        'categories': [default_UNSW],
        'current_category': None,
        'time_limit': 10,
        'msg_ids': [],
        'trivia_thread': None,
        'points': {}
    })

    for user in users:
        if user['u_id'] == user_id:
            user['channels'].append(channel_id)

    return {
        'channel_id': channel_id
    }
