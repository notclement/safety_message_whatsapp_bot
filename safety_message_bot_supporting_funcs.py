from config import *


def get_groups():
    """Returns a list of groups in the safety_message_groups.txt file"""
    with open(PATH_TO_GROUP_NAMES, 'rb') as f:
        groups_lst = [msg.rstrip('\r\n') for msg in f]
    return groups_lst


def get_safety_quotes():
    """Returns a list of safety quotes in the safety_quotes.txt file"""
    with open(PATH_TO_SAFETY_QUOTES, 'rb') as f:
        safety_quotes_lst = [msg.rstrip('\r\n') for msg in f]
    return safety_quotes_lst


def get_safety_messages():
    """Returns a list of safety messages in the safety_messages.txt file"""
    with open(PATH_TO_SAFETY_MESSSAGES, 'rb') as f:
        safety_messages_lst = [msg.rstrip('\r\n') for msg in f]
    return safety_messages_lst
