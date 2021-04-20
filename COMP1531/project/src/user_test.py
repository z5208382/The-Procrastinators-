import pytest
from auth import auth_logout
from error import InputError
from other import clear
from helper_tests import *
from user import *

##########################################################################################
###                                 USER_PROFILE TESTS                                 ###
##########################################################################################

def test_profile_invalid_token():
    '''
    Test 1: When an invalid token is input,
    raise an AccessError
    '''
    clear()

    token1 = register('1')[1]
    u_id2 = register('2')[0]
    auth_logout(token1)
    with pytest.raises(AccessError):
        user_profile(token1, u_id2)

def test_profile_invalid_uid():
    '''
    Test 2: When an invalid u_id is input,
    raise an InputError
    '''
    clear()

    token1 = register('1')[1]
    u_id2 = register('2')[0]
    with pytest.raises(InputError):
        user_profile(token1, -(u_id2))

def test_profile_correct():
    '''
    Test 3: Checks that the correct profile details are returned
    '''
    clear()

    token1 = register('1')[1]
    u_id2, _, member2 = register('2', 2)
    profile = user_profile(token1, u_id2)['user']

    assert profile['u_id'] == u_id2
    assert profile['email'] == "cemail@email.com"
    assert profile['name_first'] == member2['name_first']
    assert profile['name_last'] == member2['name_last']


##########################################################################################
###                             USER_PROFILE_SETNAME TESTS                             ###
##########################################################################################

def test_setname_invalid_token():
    '''
    Test 1: When an invalid token is input,
    raise an AccessError
    '''
    clear()

    token1 = register('1')[1]
    auth_logout(token1)
    with pytest.raises(AccessError):
        user_profile_setname(token1, 'John', 'Smith')

def test_setname_correct():
    '''
    Test 2: Ensure the user's first and last name have been correctly input
    '''
    clear()

    register('2')
    u_id1, token1 = register('1')
    user_profile_setname(token1, 'John', 'Smith')
    profile = user_profile(token1, u_id1)['user']

    full_name = [profile['name_first'], profile['name_last']]

    assert full_name == ['John', 'Smith']

def test_setname_name_first_short():
    '''
    Test 3: When the first name being input is less than 1, raise InputError
    '''
    clear()

    token1 = register('1')[1]
    with pytest.raises(InputError):
        user_profile_setname(token1, '', 'Smith')

def test_setname_name_first_long():
    '''
    Test 4: When the first name being input is greater than 50 in length,
    raise InputError
    '''
    clear()

    token1 = register('1')[1]
    with pytest.raises(InputError):
        user_profile_setname(token1, 'x'*51, 'Smith')

def test_setname_name_last_short():
    '''
    Test 5: When the first name being input is less than 1 in length,
    raise InputError
    '''
    clear()

    token1 = register('1')[1]
    with pytest.raises(InputError):
        user_profile_setname(token1, 'John', '')

def test_setname_name_last_long():
    '''
    Test 6: When the first name being input is greater than 50 in length,
    raise InputError
    '''
    clear()

    token1 = register('1')[1]
    with pytest.raises(InputError):
        user_profile_setname(token1, 'John', 'x'*51)

def test_setname_name_first_not_alphabet():
    '''
    Test 7: If first name being input has non-alphabetic characters and
    is not a hyphen or space,
    return InputError
    '''
    clear()

    token1 = register('1')[1]
    with pytest.raises(InputError):
        user_profile_setname(token1, '�', 'Smith')

def test_setname_name_last_not_alphabet():
    '''
    Test 8: If last name being input has non-alphabetic characters and
    is not a hyphen or space,
    return InputError
    '''
    clear()

    token1 = register('1')[1]
    with pytest.raises(InputError):
        user_profile_setname(token1, 'John', '�')

def test_setname_name_first_space():
    '''
    Test 9: If first name being input only has spaces,
    raise input error
    '''

    clear()

    token1 = register('1')[1]
    with pytest.raises(InputError):
        user_profile_setname(token1, '   ', 'Smith')

def test_setname_name_first_hyphen():
    '''
    Test 10: If first name being input only has hyphens,
    raise input error
    '''
    clear()

    token1 = register('1')[1]
    with pytest.raises(InputError):
        user_profile_setname(token1, '---', 'Smith')

def test_setname_name_first_space_hyphen():
    '''
    Test 11: If first name being input only has hyphens,
    raise input error
    '''
    clear()

    token1 = register('1')[1]
    with pytest.raises(InputError):
        user_profile_setname(token1, '-  -', 'Smith')

def test_setname_name_last_space():
    '''
    Test 12: If first name being input only has spaces,
    raise input error
    '''
    clear()

    token1 = register('1')[1]
    with pytest.raises(InputError):
        user_profile_setname(token1, 'John', '   ')

def test_setname_name_last_hyphen():
    '''
    Test 13: If first name being input only has hyphens,
    raise input error
    '''
    clear()

    token1 = register('1')[1]
    with pytest.raises(InputError):
        user_profile_setname(token1, 'John', '---')

def test_setname_name_last_space_hyphen():
    '''
    Test 14: If first name being input only has hyphen and spaces,
    raise input error
    '''
    clear()

    token1 = register('1')[1]
    with pytest.raises(InputError):
        user_profile_setname(token1, 'John', '-  -')



##########################################################################################
###                             USER_PROFILE_SETEMAIL TESTS                            ###
##########################################################################################
def test_setemeail_invalid_token():
    '''
    Test 1: Use an invalid token to set a valid email
    Expect, InputError
    '''
    clear()
    _, token = register('ian')
    with pytest.raises(AccessError):
        user_profile_setemail(token + 'a', 'test@example.com')


def test_setemail_empty_email():
    '''
    Test 2: With a valid token, set empty email
    Expect, InputError
    '''
    clear()
    _, token = register('ian')
    with pytest.raises(InputError):
        user_profile_setemail(token, '')


def test_setemail_invalid_email_format():
    '''
    Test 3: With a valid token, set email with wrong format
    Expect, InputError
    '''
    clear()
    _, token = register('ian')
    with pytest.raises(InputError):
        user_profile_setemail(token, 'test@.com_test')


def test_setemail_email_already_in_use():
    '''
    Test 4: With a valid token, set email same email twice
    Expect, InputError
    '''
    clear()
    _, token = register('ian')
    user_profile_setemail(token, 'test@gmail.com')
    _, token1 = register('a')
    with pytest.raises(InputError):
        user_profile_setemail(token1, 'test@gmail.com')


def test_setemail_invalid_utf_email():
    '''
    Test 5: With a valid token, set email to a non utf string
    Expect, InputError
    '''
    email = '�������@���.com'
    clear()
    _, token = register('ian')
    with pytest.raises(InputError):
        user_profile_setemail(token, email)


def test_setemail_non_standard_utf_chars():
    '''
    Test 6: With a valid token, set email to a non standard utf character
    Expect, InputError
    '''
    email = '𝕥𝕖𝕤𝕥@𝕖𝕩𝕒𝕞𝕡𝕝𝕖.𝕔𝕠𝕞'
    clear()
    _, token = register('ian')
    with pytest.raises(InputError):
        user_profile_setemail(token, email)


def test_setemail_emoji_email():
    '''
    Test 7: With a valid token, set email to email with emoji
    Expect, InputError
    '''
    email = 'the_🐐@aol.com'
    clear()
    _, token = register('ian')
    with pytest.raises(InputError):
        user_profile_setemail(token, email)


def test_setemail_valid():
    '''
    Test 8: With a valid token, set email to a valid email
    Expect, InputError
    '''
    email = 'valid_email@yahoo.com'
    clear()
    register('bro')
    u_id, token = register('ian')
    user_profile_setemail(token, email)
    new_email = user_profile(token, u_id)['user']['email']
    assert email == new_email



##########################################################################################
###                           USER_PROFILE_SETHANDLE TESTS                             ###
##########################################################################################
def test_sethandle_invalid_token():
    '''
    Test 1: Use an invalid token to set a valid handle
    Expect, InputError
    '''
    clear()
    _, token = register('ian')
    with pytest.raises(AccessError):
        user_profile_sethandle(token + 'a', 'IanJ')


def test_sethandle_empty_handle():
    '''
    Test 2: With a valid token, try set an empty handle
    Expect, InputError
    '''
    clear()
    _, token = register('ian')
    with pytest.raises(InputError):
        user_profile_sethandle(token, '')


def test_sethandle_invalid_handle_length():
    '''
    Test 3: With a valid token, try set a handle that exceeds 20 chars
    Expect, InputError
    '''
    clear()
    _, token = register('ian')
    with pytest.raises(InputError):
        user_profile_sethandle(token, 'handle' * 30)


def test_sethandle_handle_already_in_use():
    '''
    Test 4: Set handle of first registered user as 'ianj'
    Try setting handle of 2nd user as 'ianj' as well
    Expect, InputError
    '''
    handle = 'ianj'
    clear()
    _, token1 = register('ian')
    user_profile_sethandle(token1, handle)
    _, token2 = register('iann')
    with pytest.raises(InputError):
        user_profile_sethandle(token2, handle)


def test_sethandle_invalid_utf_handle():
    '''
    Test 5: Try set handle as utf string, this will work
    '''
    handle = '��������'
    clear()
    u_id, token = register('ian')
    user_profile_sethandle(token, handle)
    new_handle = user_profile(token, u_id)['user']['handle_str']
    assert new_handle == handle


def test_sethandle_emoji_handle():
    '''
    Test 6: Try set handle as emojis
    '''
    handle = '😀😀😀😀😀'
    clear()
    u_id, token = register('ian')
    user_profile_sethandle(token, handle)
    new_handle = user_profile(token, u_id)['user']['handle_str']
    assert new_handle == handle


def test_sethandle_valid_min_length():
    '''
    Test 7: Set handle with minimum length (3)
    '''
    handle = 'abc'
    clear()
    u_id, token = register('ian')
    user_profile_sethandle(token, handle)
    new_handle = user_profile(token, u_id)['user']['handle_str']
    assert new_handle == handle


def test_sethandle_valid_max_length():
    '''
    Test 8: Set handle with maximum length (20)
    '''
    handle = 'a' * 20
    clear()
    u_id, token = register('ian')
    user_profile_sethandle(token, handle)
    new_handle = user_profile(token, u_id)['user']['handle_str']
    assert new_handle == handle


def test_sethandle_valid():
    '''
    Test 9: Set handle with length somewhere in between min and max
    '''
    handle = 'aRandomPerson'
    clear()
    register('bro')
    u_id, token = register('ian')
    user_profile_sethandle(token, handle)
    new_handle = user_profile(token, u_id)['user']['handle_str']
    assert new_handle == handle

##########################################################################################
###                               USER_UPLOADPHOTO TESTS                               ###
##########################################################################################

def test_uploadphoto_invalid_token():
    '''
    Test 1 : tests for invalid user token
    Raises an InputError
    '''
    clear()
    token = register('1')[1]
    img_url = "https://i.imgur.com/QLMuFYp.jpeg"
    with pytest.raises(AccessError):
        user_profile_uploadphoto(token + 'a', img_url, 0, 0, 75, 40)

def test_uploadphoto_http_not_200():
    '''
    Test 2: test for img_url that generates a HTTP status code that's
    not status code 200
    Raises an InputError
    '''
    clear()
    img_url = "https://imgur.com/QLMuFYp.jpe"
    token = register('1')[1]
    with pytest.raises(InputError):
        user_profile_uploadphoto(token, img_url, 0, 0, 75, 40)

def test_uploadphoto_xstart_invalid():
    '''
    Test 3: test for x_start is invalid/out of bounds
    Raises an InputError
    '''
    clear()
    img_url = "https://i.imgur.com/QLMuFYp.jpeg"
    token = register('1')[1]
    with pytest.raises(InputError):
        user_profile_uploadphoto(token, img_url, -1, 0, 75, 40)

def test_uploadphoto_ystart_invalid():
    '''
    Test 4: test for y_start is invalid/out of bounds
    Raises an InputError
    '''
    clear()
    img_url = "https://i.imgur.com/QLMuFYp.jpeg"
    token = register('1')[1]
    with pytest.raises(InputError):
        user_profile_uploadphoto(token, img_url, 0, -1, 75, 40)

def test_uploadphoto_xend_invalid():
    '''
    Test 5: test for x_send is invalid/out of bounds
    Raises an InputError
    '''
    clear()
    img_url = "https://i.imgur.com/QLMuFYp.jpeg"
    token = register('1')[1]
    with pytest.raises(InputError):
        user_profile_uploadphoto(token, img_url, 0, 0, 71000, 40)

def test_uploadphoto_yend_invalid():
    '''
    Test 6: test for y_end is invalid/out of bounds
    Raises an InputError
    '''
    clear()
    img_url = "https://i.imgur.com/QLMuFYp.jpeg"
    token = register('1')[1]
    with pytest.raises(InputError):
        user_profile_uploadphoto(token, img_url, 0, 0, 75, 40000)

def test_uploadphoto_not_jpg():
    '''
    Test 7: test for img_url that is not a jpg file
    Raises an InputError
    '''
    clear()
    img_url = \
        "https://freepngimg.com/thumb/the_legend_of_zelda/21540-1-zelda-link-transparent.png"
    token = register('1')[1]
    with pytest.raises(InputError):
        user_profile_uploadphoto(token, img_url, 0, 0, 75, 40)


def test_uploadphoto_valid():
    '''
    Test 8: valid case, picture of tank diving in to
    destory submarines
    Asserts that url is what we expected
    '''
    clear()
    img_url = 'https://i.imgur.com/mKjOjUY.jpg'
    os.environ['URL'] = 'url/'
    user_data = []
    for i in range(3):
        i = str(i)
        u_id, token = register(i)
        user_profile_uploadphoto(token, img_url, 0, 0, 300, 300)
        user_data.append((u_id, token))

    for u_id, token in reversed(user_data):
        db_url = user_profile(token, u_id)['user']['profile_img_url']
        assert db_url == f'url/static/profile_{u_id}.jpg'
