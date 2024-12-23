import os

from dotenv import load_dotenv

import telebot
from telebot import types as teletypes

from messages import messages_get
import commands
from params import *
from utils import *
from user_handler import check_banned
from user_handler import check_spam
from user_handler import get_user_step
from user_handler import set_user_step

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
def ignore(message):
    user = user_from_message(message)
    date = message_date_string(message)
    logger.debug(f"Ignored message from {user} at {date}")
    loggerIgnore.debug('\n'+message_info_string(message))

# --------- Test ---------------------------------------------
@bot.message_handler(commands=['test'])
def test(message):
    info = message_info_string(message)
    print(info)

# --------- Debug warning ------------------------------------
@bot.message_handler(func=lambda msg: debugginMode and not from_bot_owner(msg))
def warn_debug(message):
    lang = message.from_user.language_code
    msg = messages_get(lang).warn_debug
    bot.reply_to(message, msg)
    check_spam(message.from_user.id)

# --------- Spam control -------------------------------------
@bot.message_handler(func=lambda msg: check_banned(msg.from_user.id))
def warn_ban(message):
    cid = message.from_user.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    bot.send_message(cid, text=msg.warn_ban1)
    bot.send_message(cid, text=msg.warn_ban2)

# --------- Banned warning -----------------------------------
@bot.message_handler(func=lambda msg: msg.from_user.id in bannedUsers)
def reject_user(message):
    cid = message.chat.id
    lang = message.from_user.language_code
    username = message.from_user.username
    msg = messages_get(lang).permaban(username)
    bot.send_message(cid, msg)

# ============================================== Commands ==================================================
# --------- Start command ------------------------------------
@bot.message_handler(commands=['start'])
def command_start(message):
    lang = message.from_user.language_code
    msg = messages_get(lang)
    bot.reply_to(message, msg.start)
    command_help(message)

# --------- Help command -------------------------------------
@bot.message_handler(commands=['help'])
def command_help(message):
    cid = message.chat.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    txt = msg.help_intro_text + '\n\n'
    txt += msg.help_commands_text + '\n'
    txt += msg.ban_info + '\n\n'
    txt += msg.help_ending
    print(txt)
    bot.send_message(cid, txt, parse_mode='HTML', link_preview_options=teletypes.LinkPreviewOptions(is_disabled=True))  # send the generated help page
    check_spam(message.from_user.id)

# --------- Mute command -------------------------------------
@bot.message_handler(commands=['togglemute'])
def command_mute(message):
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
def command_create(message):
    default(message) #NO IMPLEMENTADO

# --------- Check command -------------------------------------
@bot.message_handler(commands=['check'])
def command_check(message):
    default(message) #NO IMPLEMENTADO

# --------- Record command -------------------------------------
@bot.message_handler(commands=['rec'])
def command_record(message):
    default(message) #NO IMPLEMENTADO

# --------- Modify command -------------------------------------
@bot.message_handler(commands=['mod'])
def command_modify(message):
    default(message) #NO IMPLEMENTADO

# --------- Delete diary command -------------------------------------
@bot.message_handler(commands=['deldiary'])
def command_deldiary(message):
    default(message) #NO IMPLEMENTADO

# --------- Delete entry command -------------------------------------
@bot.message_handler(commands=['delentry'])
def command_delentry(message):
    default(message) #NO IMPLEMENTADO

# ======================================== Privileged Commands =============================================
# --------- Close bot command --------------------------------
@bot.message_handler(commands=['q'], func=lambda msg: from_bot_owner(msg))
def command_quit(message):
    cid = message.chat.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    uid = message.from_user.id
    bot.send_message(cid, msg.quit)
    set_user_step(uid, 2)

@bot.message_handler(func=lambda msg:  get_user_step(msg.from_user.id) == 2)
def command_quitted(message):
    cid = message.chat.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    uid = message.from_user.id
    set_user_step(uid, 0)
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
def command_debug(message):
    lang = message.from_user.language_code
    msg = messages_get(lang)
    debugginMode = not debugginMode
    if debugginMode :
        bot.reply_to(message, msg.debug_on)
    else :
        bot.reply_to(message, msg.debug_off)

# --------- Default ------------------------------------------
@bot.message_handler(func=lambda msg: not muteStatus)
def default(message):
    lang = message.from_user.language_code
    msg = messages_get(lang)
    bot.reply_to(message, msg.default)
    check_spam(message.from_user.id)

# ========================================== Message handlers end ==========================================


bot.infinity_polling()
logger.info("Bot closed")
commands.set_offline(bot)