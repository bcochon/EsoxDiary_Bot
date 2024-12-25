from telebot import types as teletypes
import logging
import logging.config
import pickle
import os
from params import BOT_OWNER, LOGGER_CONFIG_PATH
from datetime import datetime
from time import time
from threading import Lock

logging.config.fileConfig(LOGGER_CONFIG_PATH)
logger = logging.getLogger('DiaryBot')
loggerIgnore = logging.getLogger('Ignore')
loggerErrors = logging.getLogger('Errors')

ALLSCP = ['audio', 'document', 'video', 'videonote', 'voice', 'location', 'contact', 'sticker', 'photo']

message_mutex = Lock()

def log_exception(exception : Exception) :
    loggerErrors.error('Error {0}'.format(str(exception)))

def is_answering_pic(message : teletypes.Message) :
    if message.reply_to_message:
        ansTo = message.reply_to_message
        if ansTo.photo:
            return True
        return False

def sent_secs_ago(message : teletypes.Message, secs : int) :
    time_since_mesage = int(time()) - message.date
    return time_since_mesage > secs

def message_date_string(message : teletypes.Message, format : str = '%d/%m/%Y %H:%M:%S') :
    return unix_date_string(message.date, format)

def unix_date_string(date : int, format : str = '%d/%m/%Y %H:%M:%S') :
    return datetime.fromtimestamp(date).strftime(format)

def user_from_message(message : teletypes.Message) :
    user = message.from_user.username
    if not user: user = message.chat.id
    uid = message.from_user.id
    return f'{user}({uid})' 

def name_from_user(user : teletypes.User) :
    name = user.first_name
    if name: return name
    name = user.username
    if name: return name
    return ''

def message_info(message : teletypes.Message) :
    user = message.from_user
    date = message_date_string(message)
    info = {
        'UserID':    user.id,
        'User':      user.first_name+user.last_name,
        'Username':  user.username,
        'Language':  user.language_code,
        'Message':   message.text,
        'Date':      date
    }
    return info

def message_info_string(message : teletypes.Message):
    info = message_info(message)
    info_string = ''
    for key in info:
        info_string += f'{key}: {info[key]}\n'
    return info_string

def save_message_to_file(message : teletypes.Message):
    path = 'test'
    with message_mutex :
        save_to_file(path, message)

def from_bot_owner(message : teletypes.Message) :
    return message.from_user.id == BOT_OWNER

def save_to_file(path : str, data) :
    try:
        with open(path, 'wb') as f:
            pickle.dump(data, f)
    except Exception as e:
        log_exception(e)

def get_from_file(path : str) :
    try:
        with open(path, 'rb') as f:
            diary = pickle.load(f)
    except Exception as e:
        log_exception(e)
        diary = None
    return diary

def get_dictionary_from_files(path) -> dict :
    dict = {}
    files = os.listdir(path)
    for s_key in files :
        key = int(s_key)
        value = get_from_file(f'{path}/{key}')
        dict.update({key : value})
    return dict