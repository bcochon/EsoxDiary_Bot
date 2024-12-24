import os

from dotenv import load_dotenv

import telebot
from telebot import types as teletypes
from telebot.handler_backends import ContinueHandling

from messages import messages_get
import commands
from params import *
from utils import *
from user_handler import check_banned
from user_handler import check_spam
from user_handler import get_user_step
from user_handler import set_user_step
from user_handler import UserSteps
from diary import *

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
bannedUsers = []
debugginMode = False
muteStatus = []

commands.set_commands(bot)

logger.info("Bot Online")

# ============================================ Message handlers ============================================
# --------- Ignore previous messages -------------------------
@bot.message_handler(func=lambda msg: sent_secs_ago(msg, 30))
def ignore(message : teletypes.Message):
    user = user_from_message(message)
    date = message_date_string(message)
    logger.debug(f"Ignored message from {user} at {date}")
    loggerIgnore.debug('\n'+message_info_string(message))

# --------- Test ---------------------------------------------
@bot.message_handler(commands=['test'])
def test(message : teletypes.Message):
    info = message_info_string(message)
    print(info)
    save_message_to_file(message)

# --------- Debug warning ------------------------------------
@bot.message_handler(func=lambda msg: debugginMode and not from_bot_owner(msg))
def warn_debug(message : teletypes.Message):
    lang = message.from_user.language_code
    msg = messages_get(lang).warn_debug
    bot.reply_to(message, msg)
    check_spam(message.from_user.id)

# --------- Spam control -------------------------------------
@bot.message_handler(func=lambda msg: check_banned(msg.from_user.id))
def warn_ban(message : teletypes.Message):
    cid = message.from_user.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    bot.send_message(cid, text=msg.warn_ban1)
    bot.send_message(cid, text=msg.warn_ban2)

# --------- Banned warning -----------------------------------
@bot.message_handler(func=lambda msg: msg.from_user.id in bannedUsers)
def reject_user(message : teletypes.Message):
    cid = message.chat.id
    lang = message.from_user.language_code
    username = message.from_user.username
    msg = messages_get(lang).permaban(username)
    bot.send_message(cid, msg)

# ============================================== Commands ==================================================
# --------- Start command ------------------------------------
@bot.message_handler(commands=['start'])
def command_start(message : teletypes.Message):
    lang = message.from_user.language_code
    msg = messages_get(lang)
    bot.reply_to(message, msg.start)
    command_help(message)

# --------- Help command -------------------------------------
@bot.message_handler(commands=['help'], func=lambda msg: len(msg.text.split())>1)
def command_help_rec(message : teletypes.Message):
    args = message.text.split()
    if args[1].lower() != 'rec':
        return ContinueHandling
    cid = message.chat.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    txt = msg.help_rec + '\n'
    txt += msg.help_rec_disclaimer
    bot.send_message(cid, txt, parse_mode='HTML')

@bot.message_handler(commands=['help'])
def command_help(message : teletypes.Message):
    cid = message.chat.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    txt = msg.help_intro_text + '\n\n'
    txt += msg.help_commands_text + '\n'
    txt += msg.ban_info + '\n\n'
    txt += msg.help_ending
    bot.send_message(cid, txt, parse_mode='HTML', link_preview_options=teletypes.LinkPreviewOptions(is_disabled=True))  # send the generated help page
    check_spam(message.from_user.id)

# --------- Mute command -------------------------------------
@bot.message_handler(commands=['togglemute'])
def command_mute(message : teletypes.Message):
    cid = message.chat.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    user = user_from_message(message)
    if cid not in muteStatus :
        muteStatus.append(cid)
        bot.reply_to(message, msg.muted)
        this_status = 'muted'
    else :
        muteStatus.remove(cid)
        bot.reply_to(message, msg.unmuted)
        this_status = 'unmuted'
    logger.debug(f'User {user} toggled muteStatus for chat {cid} (muteStatus={this_status})')

# --------- Create command -------------------------------------
@bot.message_handler(commands=['create'])
def command_create(message : teletypes.Message):
    cid = message.chat.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    if diary_exists(cid) :
        bot.reply_to(message, msg.diary_already_created)
    else :
        create_diary(message.chat)
        bot.reply_to(message, msg.diary_created)

# --------- Check command -------------------------------------
@bot.message_handler(commands=['check'])
def command_check(message : teletypes.Message):
    cid = message.chat.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    if diary_exists(cid) :
        return ContinueHandling()
    bot.reply_to(message, msg.no_diary)

@bot.message_handler(commands=['check'])
def retrieve_entries(message : teletypes.Message):
    cid = message.chat.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    bot.send_message(cid, msg.check)
    diary = get_diary(cid)
    entries = diary.retrieve_all_entries()
    if entries:
        for entry in entries :
            text = entry.format(lang)
            reply = teletypes.ReplyParameters(message_id=entry.mid, chat_id=entry.cid)
            bot.send_message(cid, text, parse_mode='HTML', reply_parameters=reply)
    else :
        bot.send_message(cid, msg.no_entries)

# --------- Record command -------------------------------------
@bot.message_handler(commands=['rec'])
def command_record(message : teletypes.Message):
    cid = message.chat.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    if diary_exists(cid) :
        return ContinueHandling()
    bot.reply_to(message, msg.no_diary)
    
@bot.message_handler(commands=['rec'])
def new_entry(message : teletypes.Message):
    try:
        cid = message.chat.id
        lang = message.from_user.language_code
        msg = messages_get(lang)
        entry_message = message.reply_to_message
        if not entry_message : entry_message = message
        get_diary(cid).create_entry(message.from_user, entry_message, True)
        bot.reply_to(message, msg.entry_added)
    except Exception as e:
        log_exception(e)
        bot.reply_to(message, msg.rec_error)

# --------- Modify command -------------------------------------
@bot.message_handler(commands=['mod'])
def command_modify(message : teletypes.Message):
    default(message) #NO IMPLEMENTADO

# --------- Delete diary command -------------------------------------
@bot.message_handler(commands=['deldiary'])
def command_deldiary(message : teletypes.Message):
    cid = message.chat.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    get_diary(cid).delete_diary()

# --------- Delete entry command -------------------------------------
@bot.message_handler(commands=['delentry'])
def command_delentry(message : teletypes.Message):
    default(message) #NO IMPLEMENTADO

# ======================================== Privileged Commands =============================================
# --------- Close bot command --------------------------------
@bot.message_handler(commands=['q'], func=lambda msg: from_bot_owner(msg))
def command_quit(message : teletypes.Message):
    cid = message.chat.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    uid = message.from_user.id
    bot.send_message(cid, msg.quit)
    set_user_step(uid, UserSteps.QUIT)

@bot.message_handler(func=lambda msg:  get_user_step(msg.from_user.id) == UserSteps.QUIT)
def command_quitted(message : teletypes.Message):
    cid = message.chat.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    uid = message.from_user.id
    set_user_step(uid, UserSteps.DEFAULT)
    if message.text.lower() == '/y':
        try:
            bot.send_message(cid, msg.quitted)
            bot.stop_bot()
            logger.debug("Closing bot...")
        except Exception as e:
            logger.error("Unexpected error. Couldn't close bot")
            log_exception(e)
    else:
        bot.reply_to(message, msg.quit_cancel)


# --------- Toggle Debug command -----------------------------
@bot.message_handler(commands=['toggledebug'], func=lambda msg: from_bot_owner(msg))
def command_debug(message : teletypes.Message):
    lang = message.from_user.language_code
    msg = messages_get(lang)
    debugginMode = not debugginMode
    if debugginMode :
        bot.reply_to(message, msg.debug_on)
    else :
        bot.reply_to(message, msg.debug_off)

# --------- Default ------------------------------------------
@bot.message_handler(func=lambda msg: not muteStatus)
def default(message : teletypes.Message):
    lang = message.from_user.language_code
    msg = messages_get(lang)
    bot.reply_to(message, msg.default)
    check_spam(message.from_user.id)

# ========================================== Message handlers end ==========================================


bot.infinity_polling()
logger.info("Bot closed")
commands.set_offline(bot)