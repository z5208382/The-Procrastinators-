# Flockr Project Assumptions

## General
* Test file naming convention: `<file name>_test.py`
* Variables that are passed in from the front end (token, channel_id, u_id, start, is_public) are not empty and are formatted correctly (i.e. character specifications and length)
* Owner of flockr is user with `u_id : 0` 

## Database
* Iteration 1: Assume multiple dictionaries are used for 'database'
    **REFER 6.1**

## Auth
* Parameters that are input by the user (email, password, name_first, name_last) may be empty
* name_first can only contain letters (uppercase and lowercase), spaces and dashes, otherwise an input error is returned
* name_last can only contain letters (uppercase and lowercase), dashes and spaces, otherwise an input error is returned
    ### Tokens
    * If `token` is an empty string, assume user is not logged in
    * Registering a person automatically logs them in (a valid token is given)
    * Token generated with payload dictionary with 'u_id' and 'email' as keys
    ### Valid email
    * Other than passing regex test, email domain must also be resolvable
    ### Reset password
    * Assume `reset_code` is in user dictionary

## Channel
* for channel_messages, start must be greater than or equal to zero
* an authorised user cannot invite themselves or invite other members who are already in the channel (for channel_join/invite)
* if there is only one person left in a channel, they become the owner of that channel
* if there is no one left in a channel, the channel is removed
* if there is only one channel owner and they leave, the oldest member becomes owner 
* To add an owner to a channel (using channel_addowner), they first need to be a member of that channel
* a flockr owner can add/remove owners without being in the channel
* if the user u_id (as passed through the parameters) is not valid, return an InputError

## Channels
* Channels_list will return both public and private channels that the user is a member of
* Channels_create will make the user who's creating the channel also an owner of the channel
* Channels_listall will return all channels - both public and private (even if the user is not a member of that channel)
* Assume no messages in messages database for channel when calling channels_create
* Assume more than one channel can have the same name

## Messages
* `message_pin` or `message_unpin`: can be performed by a channel owner or a flockr owner, but they MUST be in channel

## Standup
* Length is greater or equal to 0
* Length cannot be empty
* The authorised user must be a member of the channel with the given channel_id

## Handle string
* Can be any character, includes emojis

## Trivia
* Default category is loaded into `trivias` when channel is created
* Correct option is always the first option (when creating a trivia)
