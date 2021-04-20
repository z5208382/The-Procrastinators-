import pytest
from channel import *
from helper_tests import *
from other import *

# Flockr permissions
FLOCKR_OWNER = 1
FLOCKR_MEMBER = 2

##########################################################################################
###                                   USERS_ALL TESTS                                  ###
##########################################################################################
def test_invalid_token_users():
    '''
    Test 1: Invalid token
    '''
    clear()
    with pytest.raises(AccessError):
        users_all('invalidToken')


def test_users_one():
    '''
    Test 2: only one user
    '''
    clear()
    user1_uid, user1_token = register('1')

    user1 = user_profile(user1_token, user1_uid)['user']
    assert users_all(user1_token)['users'] == [user1]


def test_users_all_valid():
    '''
    Test 3: multiple users
    '''
    clear()
    user1_uid, user1_token = register('1')
    user2_uid, user2_token = register('2')

    user1 = user_profile(user1_token, user1_uid)['user']
    user2 = user_profile(user2_token, user2_uid)['user']

    assert users_all(user1_token)['users'] == [user1, user2]

    # give same list when token of user2 given

    assert users_all(user2_token)['users'] == [user1, user2]


def test_to_add_users_all():
    '''
    Test 4: added user then checked profiles
    '''
    clear()
    user1_uid, user1_token = register('1')
    user1 = user_profile(user1_token, user1_uid)['user']

    assert users_all(user1_token)['users'] == [user1]

    user2_uid, user2_token = register('2')
    user2 = user_profile(user2_token, user2_uid)['user']

    assert users_all(user1_token)['users'] == [user1, user2]



##########################################################################################
###                       ADMIN/USERPERMISSION/CHANGE TESTS                            ###
##########################################################################################
def test_admin_userpermission_change_invalid_user_id():
    '''
    Test 1 - Input error when invalid uid
    '''
    clear()
    user1_token = register('1')[1]
    with pytest.raises(InputError):
        admin_userpermission_change(user1_token, "invalid_uid", FLOCKR_OWNER)


def test_admin_userpermission_change_invalid_permission_id():
    '''
    Test 2 - Input error when invalid permission id
    '''
    clear()
    user1_token = register('1')[1]
    user2_uid = register('2')[0]

    with pytest.raises(InputError):
        admin_userpermission_change(user1_token, user2_uid, "invalid_permissionId")


def test_admin_userpermission_change_invalid_token():
    '''
    Test 3 - Access error when invalid token
    '''
    clear()
    user2_uid = register('2')[0]

    with pytest.raises(AccessError):
        admin_userpermission_change("invalid_token", user2_uid, FLOCKR_OWNER)


def test_admin_userpermission_is_owner():
    '''
    Test 4 - change permission id of user to member
    '''
    clear()
    _, owner_token, owner_info = register('1', 1)
    owner_info['profile_img_url'] = ''
    member_uid, member_token, member_info = register('2', 1)
    member_info['profile_img_url'] = ''

    # change member permission to owner
    admin_userpermission_change(owner_token, member_uid, FLOCKR_OWNER)

    # make sure member now has owner permissions in channel despite not being channel owner
    new_member_uid, new_member_token, new_member_info = register('3', 1)
    new_member_info['profile_img_url'] = ''

    channel_one = create_public_channel(owner_token, '1')
    channel_join(member_token, channel_one)
    channel_join(new_member_token, channel_one)
    channel_addowner(member_token, channel_one, new_member_uid)

    # use channel details to ensure 2 owners (flockr owner not an owner)
    details = channel_details(member_token, channel_one)
    assert details['owner_members'] == [owner_info, member_info, new_member_info]


def test_admin_userpermission_not_owner():
    '''
    Test 5: user tries to change member permission id to owner but they are not an owner
    '''
    clear()
    _, owner_token, owner_info = register('1', 1)
    owner_info['profile_img_url'] = ''
    member1_uid, member1_token, member1_info = register('2', 1)
    member1_info['profile_img_url'] = ''
    member2_uid, member2_token, member2_info = register('3', 1)
    member2_info['profile_img_url'] = ''

    # Access error when user who is not an owner tries to change permission id
    with pytest.raises(AccessError):
        admin_userpermission_change(member1_token, member2_uid, FLOCKR_OWNER)
    with pytest.raises(AccessError):
        admin_userpermission_change(member2_token, member1_uid, FLOCKR_OWNER)

    admin_userpermission_change(owner_token, member1_uid, FLOCKR_OWNER)

    # make sure new flockr owener now has owner permissions
    # in channel despite not being channel owner

    channel_one = create_public_channel(owner_token, '1')
    channel_join(member2_token, channel_one)
    channel_join(member1_token, channel_one)
    channel_addowner(member1_token, channel_one, member2_uid)

    details = channel_details(member1_token, channel_one)
    assert details['owner_members'] == [owner_info, member1_info, member2_info]


def test_admin_userpermission_owner_to_member():
    '''
    Test 6: owner first make member owner, then 2nd owner make first owner into member
    '''
    clear()
    owner_uid, owner_token = register('1')
    member_uid, member_token = register('2')

    # change member permission to owner
    admin_userpermission_change(owner_token, member_uid, FLOCKR_OWNER)

    # member who is now owner change owner permission id to member
    admin_userpermission_change(member_token, owner_uid, FLOCKR_MEMBER)

    # test to ensure original owner (who now has only member permission)
    # cannot remove an owner to a channel

    channel_one = create_public_channel(member_token, '1')
    channel_join(owner_token, channel_one)

    with pytest.raises(AccessError):
        channel_removeowner(owner_token, channel_one, member_uid)



##########################################################################################
###                                    SEARCH TESTS                                    ###
##########################################################################################
def test_search_invalid_token_owner():
    '''
    Test 1: Search with an invalid token belonging to channel owner
    '''
    clear()
    load_messages = load_message()
    token = load_messages['user']['token']
    with pytest.raises(AccessError):
        search(token + 'a', 'a')


def test_search_invalid_token_member():
    '''
    Test 2: Search with an invalid token belonging to channel member
    '''
    clear()
    load_messages = load_message()
    owner_token = load_messages['user']['token']
    u_id, token = register('b')
    channel_invite(owner_token, load_messages['private'], u_id)
    channel_invite(owner_token, load_messages['public'], u_id)
    with pytest.raises(AccessError):
        search(token + 'a', 'a')


def test_search_empty_query_str_owner():
    '''
    Test 3: Search with an empty query string,
    using token belonging to channel owner
    '''
    clear()
    load_messages = load_message()
    token = load_messages['user']['token']
    assert search(token, '') == {'messages':[]}


def test_search_empty_query_str_member():
    '''
    Test 4: Search with an empty query string,
    using token belonging to channel member
    '''
    clear()
    load_messages = load_message()
    owner_token = load_messages['user']['token']
    u_id, token = register('b')
    channel_invite(owner_token, load_messages['private'], u_id)
    channel_invite(owner_token, load_messages['public'], u_id)
    assert search(token, '') == {'messages':[]}


def test_search_no_channels():
    '''
    Test 5: User search when no channels exists, therefore no messages
    Expect an empty `messages` list
    '''
    clear()
    _, token = register('a')
    result = search(token, 'nothing exists')['messages']
    assert result == []


def test_search_valid_owner_public():
    '''
    Test 6: A valid search test with owner's token,
    using public channel
    Create another user, make user owner, search using token
    '''
    clear()
    load_messages = load_message()
    u_id, token = register('b')
    owner_token = load_messages['user']['token']
    channel_id = load_messages['public']
    channel_invite(owner_token, channel_id, u_id)
    channel_addowner(owner_token, channel_id, u_id)
    result = search(token, 'a')['messages']
    assert len(result) == 2
    assert result[0]['message'] == 'a'
    assert result[1]['message'] == 'a'


def test_search_valid_owner_private():
    '''
    Test 7: A valid search test with owner's token,
    using private channel
    Create another user, make user owner, search using token
    '''
    clear()
    load_messages = load_message()
    u_id, token = register('b')
    owner_token = load_messages['user']['token']
    channel_id = load_messages['private']
    channel_invite(owner_token, channel_id, u_id)
    channel_addowner(owner_token, channel_id, u_id)
    result = search(token, 'a')['messages']
    assert len(result) == 2
    assert result[0]['message'] == 'a'
    assert result[1]['message'] == 'a'


def test_search_valid_member_public():
    '''
    Test 8: A valid search test with member's token,
    using public channel
    Create another user, add user, search using token
    '''
    clear()
    load_messages = load_message()
    u_id, token = register('b')
    owner_token = load_messages['user']['token']
    channel_id = load_messages['public']
    channel_invite(owner_token, channel_id, u_id)
    result = search(token, 'a')['messages']
    assert len(result) == 2
    assert result[0]['message'] == 'a'
    assert result[1]['message'] == 'a'


def test_search_valid_member_private():
    '''
    Test 9: A valid search test with member's token,
    using private channel
    Create another user, add user, search using token
    '''
    clear()
    load_messages = load_message()
    u_id, token = register('b')
    owner_token = load_messages['user']['token']
    channel_id = load_messages['private']
    channel_invite(owner_token, channel_id, u_id)
    result = search(token, 'a')['messages']
    assert len(result) == 2
    assert result[0]['message'] == 'a'
    assert result[1]['message'] == 'a'
