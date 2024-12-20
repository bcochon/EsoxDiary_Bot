import os

from dotenv import load_dotenv

import telebot

from messages import messages_get
import params as ps
import utils
from user_handler import check_banned
from user_handler import check_spam

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

print("Bot Online")

# ============================================= Define commands ============================================
commands = {
    'start'         : 'start description',
    'help'          : 'help description',
    'togglemute'    : 'togglemute description'
}
commandsList = utils.commands_list(commands)
bot.delete_my_commands(scope=None, language_code=None)
bot.set_my_commands(commands=commandsList)

# ============================================ Message handlers ============================================
# --------- Test ---------------------------------------------
@bot.message_handler(commands=['test'])
def test(message):
    utils.print_message(message)

# --------- Spam control -------------------------------------
@bot.message_handler(func=lambda msg: check_banned(msg.from_user.id))
def warn_ban(message):
    cid = message.from_user.id
    msg = messages_get(message.from_user)
    bot.send_message(cid, text=msg.warn_ban1)
    bot.send_message(cid, text=msg.warn_ban2)

# --------- Debug warning ------------------------------------
@bot.message_handler(func=lambda msg: ps.debugginMode and msg.from_user.username != ps.botOwner)
def warn_debug(message):
    msg = messages_get(message.from_user)
    bot.reply_to(message, msg.warn_debug)
    check_spam(message.from_user.id)

# --------- Toggle Debug command -----------------------------
@bot.message_handler(commands=['toggledebug'], func=lambda msg: msg.from_user.username == ps.botOwner)
def command_debug(message):
    msg = messages_get(message.from_user)
    ps.debugginMode = not ps.debugginMode
    if ps.debugginMode :
        bot.reply_to(message, "Debug mode on")
    else :
        bot.reply_to(message, "Debug mode off")

# --------- Banned warning -----------------------------------
@bot.message_handler(func=lambda msg: msg.from_user.id in ps.bannedUsers)
def reject_user(message):
    cid = message.chat.id
    msg = messages_get(message.from_user)
    username = message.from_user.username
    bot.send_message(cid, msg.permaban(username))

# --------- Help command -------------------------------------
@bot.message_handler(commands=['help'])
def command_help(message):
    cid = message.chat.id
    msg = messages_get(message.from_user)
    bot.send_message(
        cid, 
        telebot.formatting.format_text(
            msg.help_intro_text,
            msg.help_commands_text(commands),
            msg.ban_info,
            separator="\n" # separator separates all strings
        ),
        parse_mode='MarkdownV2'
    )  # send the generated help page
    check_spam(message.from_user.id)

# --------- Start command ------------------------------------
@bot.message_handler(commands=['start'])
def command_start(message):
    msg = messages_get(message.from_user)
    bot.reply_to(message, msg.start)
    command_help(message)

# --------- Mute command -------------------------------------
@bot.message_handler(commands=['togglemute'])
def command_mute(message):
    msg = messages_get(message.from_user)
    ps.muteStatus = not ps.muteStatus
    if ps.muteStatus :
        bot.reply_to(message, msg.muted)
    else :
        bot.reply_to(message, msg.unmuted)

# --------- Close bot command --------------------------------
@bot.message_handler(commands=['q'], func=lambda msg: msg.from_user.username == ps.botOwner)
def command_quit(message):
    cid = message.chat.id
    msg = messages_get(message.from_user)
    uid = message.from_user.id
    bot.send_message(cid, msg.quit)
    utils.set_user_step(uid, 2)

@bot.message_handler(func=lambda msg:  utils.get_user_step(msg.from_user.id) == 2)
def command_quitted(message):
    cid = message.chat.id
    msg = messages_get(message.from_user)
    uid = message.from_user.id
    utils.set_user_step(uid, 0)
    if message.text.lower() == 'y':
        try:
            bot.send_message(cid, msg.quitted)
            bot.stop_bot()
            print("Program terminated")
        except:
            print("Unexpected exception. Program could not be terminated")
    else:
        bot.reply_to(message, msg.quit_cancel)

# --------- Default ------------------------------------------
@bot.message_handler(func=lambda msg: not ps.muteStatus)
def command_default(message):
    msg = messages_get(message.from_user)
    bot.reply_to(message, msg.default)
    check_spam(message.from_user.id)

# ========================================== Message handlers end ==========================================


bot.infinity_polling()