from error import InputError

def echo(value):
    '''
    Provided from starter code,
    Raises InputError when value is 'echo'
    '''
    if value == 'echo':
        raise InputError('Input cannot be echo')
    return value
