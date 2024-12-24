from telebot import types as teletypes
import logging
import logging.config
from params import BOT_OWNER
from params import LOGGER_CONFIG_PATH
from datetime import datetime
from time import time


logging.config.fileConfig(LOGGER_CONFIG_PATH)
logger = logging.getLogger('DiaryBot')
loggerIgnore = logging.getLogger('Ignore')
loggerErrors = logging.getLogger('Errors')

ALLSCP = ['audio', 'document', 'video', 'videonote', 'voice', 'location', 'contact', 'sticker', 'photo']

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

def message_date_string(message : teletypes.Message) :
    return datetime.fromtimestamp(message.date).strftime('%d/%m/%Y %H:%M:%S')

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

def from_bot_owner(message : teletypes.Message) :
    return message.from_user.id == BOT_OWNER