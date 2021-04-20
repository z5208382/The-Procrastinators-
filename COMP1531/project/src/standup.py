from datetime import datetime, timedelta
from threading import Timer
from helper import *
from data import *
global channels
global users
global messages
global trivias

##########################################################################################
###                                   STANDUP_START                                    ###
##########################################################################################
def standup_start(token, channel_id, length):
    '''
    Start the standup period which runs for 'length' seconds
    Parameters: token, channel_id, length
    Return: {time_finish}
    Exceptions:
        - InputError: channel_id is not a valid channel
        - InputError: an active standup is currently running
    '''
    auth_id = get_user_id(token)
    c_index = check_channel_valid(channel_id)
    check_user_in_channel(auth_id, channel_id)
    if standup_active(token, channel_id)['is_active']:
        raise InputError(description='standup is currently active')

    for trivia in trivias:
        if trivia['channel_id'] == channel_id:
            if trivia['trivia_active']:
                raise InputError(description='trivia is currently active')

    time_finish = (datetime.now() + timedelta(seconds=length)).timestamp()
    Timer(length, send_standup_messages, [auth_id, channel_id, time_finish]).start()
    channels[c_index]['standup'] = time_finish

    return {
        'time_finish': time_finish
    }

def send_standup_messages(u_id, channel_id, time_created):
    '''
    Sends the packaged message to the channel from the user who
    started the standup.
    Parameters: token, channel_id
    '''
    for channel in messages:
        if channel_id == channel['channel_id']:
            if channel['standup_messages'] != "":
                global message_ids_counter
                message_ids_counter += 1
                message_data = {
                    'message_id': message_ids_counter,
                    'u_id': u_id,
                    'message': channel['standup_messages'],
                    'time_created': time_created,
                    'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}],
                    'is_pinned': False
                }
                channel['messages'].append(message_data)
            channel['standup_messages'] = ""

##########################################################################################
###                                  STANDUP_ACTIVE                                    ###
##########################################################################################
def standup_active(token, channel_id):
    '''
    For a given channel, return whether the standup is active and
    what time it finishes. If it is not active, time_finish returns None
    Parameters: token, channel_id
    Return: {is_active, time_finish}
    Exceptions:
        - InputError: channel_id is not a valid channel
    '''
    auth_id = get_user_id(token)
    c_index = check_channel_valid(channel_id)
    check_user_in_channel(auth_id, channel_id)
    time_now = datetime.now().timestamp()
    time_finish = channels[c_index]['standup']
    if time_now < time_finish:
        return {
            'is_active': True,
            'time_finish': time_finish
        }
    else:
        return {
            'is_active': False,
            'time_finish': None
        }

##########################################################################################
###                                   STANDUP_SEND                                     ###
##########################################################################################

def standup_send(token, channel_id, message):
    '''
    Assuming a standup is active, sends a message to be buffered in a queue. At
    the end of the standup, the messages are collated and sent as one
    message by the user who started the standup.
    Return: {}
    Errors:
        Input: - Channel id is not valid
               - Messages is more than 1k characters long
               - No standup currently active in channel
       Access: - Authorised user is not part of channel that message is in
               - Token is invalid

    '''
    auth_id = get_user_id(token)
    check_channel_valid(channel_id)
    check_user_in_channel(auth_id, channel_id)
    if not standup_active(token, channel_id)['is_active']:
        raise InputError(description='No standups currently active')

    if len(message) > 1000:
        raise InputError(description='Message exceeded 1000 characters')

    if message == "":
        raise InputError(description='Message being sent is empty')

    if message.startswith("/trivia"):
        raise InputError(description="Standup is currently active. Cannot do trivia")

    for user in users:
        if user['u_id'] == auth_id:
            message = user['handle'] + ": " + message

    for channel in messages:
        if channel['channel_id'] == channel_id:
            if channel['standup_messages'] == "":
                channel['standup_messages'] = message
            else:
                channel['standup_messages'] += "\n" + message

    return {}
