from auth import auth_register
from channels import channels_create
from message import message_send

############################################################################################
###                                  HELPER TEST FUNCTIONS                               ###
############################################################################################

def register(a, *args):
    '''
    registers user, returns their u_id and token
    if extra arguments added, also returns member details (as returned in channel_details)
    '''
    if a in ['0', '1', '2', '3', '4', '5']:
        a = a.translate(str.maketrans('01234', 'abcde'))
        user = auth_register(a + "email@email.com", "1234abcd", "First" + a, "Last" + a)
        u_id = user['u_id']
        token = user['token']
        member = {'u_id': u_id, 'name_first': 'First' + a, 'name_last': 'Last' + a}
    else:
        user = auth_register(f"{a.lower()}@gmail.com", "1234abcd", a, a)
        u_id = user['u_id']
        token = user['token']
        member = {'u_id': u_id, 'name_first': a, 'name_last': a}

    if len(args) > 0:
        return [u_id, token, member]
    else:
        return [u_id, token]


def create_public_channel(token, a):
    '''
    creates a public channel and returns its channel_id
    '''
    return channels_create(token, 'Channel' + a, True)['channel_id']


def create_private_channel(token, a):
    '''
    creates a private channel and returns its channel_id
    '''
    return channels_create(token, 'Channel' + a, False)['channel_id']


def load_message():
    '''
    Create a user, a public and a private channel.
    Send message to both channels
    Returns:
        { user: {u_id, token},
          private: channel_id,
          public: channel_id
        }
    '''
    u_id, token = register('a')
    pub_channel = channels_create(token, 'pub', True)['channel_id']
    priv_channel = channels_create(token, 'priv', False)['channel_id']
    user = {'u_id': u_id, 'token': token}
    for i in "abcdaefghij":
        message_send(token, pub_channel, i)
        message_send(token, priv_channel, i)

    return {
        'user': user,
        'private': priv_channel,
        'public': pub_channel
    }
