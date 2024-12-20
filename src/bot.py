import os

from dotenv import load_dotenv

import telebot

from messages import messages_get
import commands
from params import *
from utils import *
from user_handler import check_banned
from user_handler import check_spam

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

commands.set_commands(bot)

print("Bot Online")

# ============================================ Message handlers ============================================
# --------- Test ---------------------------------------------
@bot.message_handler(commands=['test'])
def test(message):
    print_message(message)

# --------- Spam control -------------------------------------
@bot.message_handler(func=lambda msg: check_banned(msg.from_user.id))
def warn_ban(message):
    cid = message.from_user.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    bot.send_message(cid, text=msg.warn_ban1)
    bot.send_message(cid, text=msg.warn_ban2)

# --------- Debug warning ------------------------------------
@bot.message_handler(func=lambda msg: debugginMode and not from_bot_owner(msg))
def warn_debug(message):
    lang = message.from_user.language_code
    msg = messages_get(lang)
    bot.reply_to(message, msg.warn_debug)
    check_spam(message.from_user.id)

# --------- Banned warning -----------------------------------
@bot.message_handler(func=lambda msg: msg.from_user.id in bannedUsers)
def reject_user(message):
    cid = message.chat.id
    lang = message.from_user.language_code
    msg = messages_get(lang)
    username = message.from_user.username
    bot.send_message(cid, msg.permaban(username))

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
    bot.send_message(
        cid, 
        telebot.formatting.format_text(
            msg.help_intro_text,
            msg.help_commands_text(commands.commands_get(lang)),
            msg.ban_info,
            separator="\n" # separator separates all strings
        ),
        parse_mode='MarkdownV2'
    )  # send the generated help page
    check_spam(message.from_user.id)

# --------- Mute command -------------------------------------
@bot.message_handler(commands=['togglemute'])
def command_mute(message):
    lang = message.from_user.language_code
    msg = messages_get(lang)
    muteStatus = not muteStatus
    if muteStatus :
        bot.reply_to(message, msg.muted)
    else :
        bot.reply_to(message, msg.unmuted)

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
    if message.text.lower() == 'y':
        try:
            bot.send_message(cid, msg.quitted)
            bot.stop_bot()
            print("Program terminated")
        except:
            print("Unexpected exception. Program could not be terminated")
    else:
        bot.reply_to(message, msg.quit_cancel)


# --------- Toggle Debug command -----------------------------
@bot.message_handler(commands=['toggledebug'], func=lambda msg: from_bot_owner(msg))
def command_debug(message):
    lang = message.from_user.language_code
    msg = messages_get(lang)
    debugginMode = not debugginMode
    if debugginMode :
        bot.reply_to(message, "Debug mode on")
    else :
        bot.reply_to(message, "Debug mode off")

# --------- Default ------------------------------------------
@bot.message_handler(func=lambda msg: not muteStatus)
def default(message):
    lang = message.from_user.language_code
    msg = messages_get(lang)
    bot.reply_to(message, msg.default)
    check_spam(message.from_user.id)

# ========================================== Message handlers end ==========================================


bot.infinity_polling()