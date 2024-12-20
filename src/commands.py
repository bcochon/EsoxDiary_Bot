from params import DEFAULT_LANG
from params import BOT_OWNER
from telebot import types as tele_types

# =============================== COMMANDS ===============================
privileged_commands = {
    'q'             : 'close bot execution',
    'toggledebug'   : 'toggle debug mode'
}

commands_en = {
    'start'         : 'begin using the bot',
    'help'          : 'learn more about available commands',
    'togglemute'    : 'toggle answer to not understood messages',
    'create'        : 'create new diary for this chat',
    'check'         : 'see diary entries',
    'rec'           : 'record entry in this chat diary',
    'mod'           : 'modify a diary entry',
    'deldiary'      : 'delete this chat diary',
    'delentry'      : 'delete a diary entry'
}

commands_es = {
    'start'         : 'empezar a usar el bot',
    'help'          : 'más info acerca de los comandos disponibles',
    'togglemute'    : 'activar respuesta a mensajes no entendidos',
    'create'        : 'crear nuevo diario para este chat',
    'check'         : 'ver entradas de diario',
    'rec'           : 'grabar una entrada en el diario de este chat',
    'mod'           : 'modificar una entrada de diario',
    'deldiary'      : 'eliminar el diario de este chat',
    'delentry'      : 'eliminar una entrada de diario'
}

commands_langs = {
    'en' : commands_en,
    'es' : commands_es
}

# ============================== FUNCTIONS ===============================

def commands_get(lang) :
    cmds = commands_langs[lang]
    if not cmds :
        cmds = commands_langs[DEFAULT_LANG]
    return cmds

def commands_list(commands) :
    list = []
    for key in commands:
        list.append(tele_types.BotCommand(key, commands[key]))
    return list
commandsList = commands_list(commands_langs[DEFAULT_LANG])

def set_regular_commands(bot) :
    for lang in commands_langs:
        thisLangCommands = commands_get(lang)
        bot.set_my_commands(commands=commands_list(thisLangCommands), language_code=lang)

def set_privileged_commands(bot) :
    privileged_scope = tele_types.BotCommandScopeChat(chat_id=BOT_OWNER)
    privilegedCommandsList = commandsList+commands_list(privileged_commands)
    bot.set_my_commands(commands=privilegedCommandsList, scope=privileged_scope)

def set_commands(bot) :
    set_privileged_commands(bot)
    set_regular_commands(bot)