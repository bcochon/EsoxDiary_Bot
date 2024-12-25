from params import DEFAULT_LANG, BOT_OWNER
from telebot import types as teletypes
from utils import logger

# =============================== COMMANDS ===============================
commands_langs = {}

class CommandsByLanguage :
    def __init__(self, language, privileged, offline, menu, diary) :
        self.language = language
        self.privileged = privileged
        self.offline = offline
        self.menu = menu
        self.diary = diary
        commands_langs.update({language : self})

    def get_regular(self) :
        return self.menu|self.diary
    
    def get_privileged(self) :
        return self.get_regular()|self.privileged

commands_en = CommandsByLanguage(
    language = 'en',
    privileged = {
        'q'             : 'close bot execution',
        'toggledebug'   : 'toggle debug mode'
    },
    offline = {
        'offline'       : 'bot currently offline 😴'
    },
    menu = {
        'help'          : 'how to use',
        'togglemute'    : "toggle answer to messages I don't understand"
    },
    diary = {
        'create'        : 'create diary for this chat',
        'check'         : 'see diary entries',
        'rec'           : 'record entry in this chat diary',
        'deldiary'      : 'delete this chat diary',
        'delentry'      : 'delete a diary entry'
    }
)

commands_es = CommandsByLanguage(
    language = 'es',
    privileged = {
        'q'             : 'close bot execution',
        'toggledebug'   : 'toggle debug mode'
    },
    offline = {
        'offline'       : 'bot apagado ahora mismo 😴'
    },
    menu = {
        'help'          : 'guía de uso',
        'togglemute'    : 'activar respuesta a mensajes no entendidos'
    },
    diary = {
        'create'        : 'crear diario para este chat',
        'check'         : 'ver entradas de diario',
        'rec'           : 'grabar una entrada en el diario de este chat',
        'deldiary'      : 'eliminar el diario de este chat',
        'delentry'      : 'eliminar una entrada de diario'
    }
)

privileged_scope = teletypes.BotCommandScopeChat(chat_id=BOT_OWNER)

# ============================== FUNCTIONS ===============================

def commands_get(lang: str) :
    if lang in commands_langs :
        return commands_langs[lang]
    return commands_langs[DEFAULT_LANG]

def commands_list(commands: dict) :
    list = []
    for key in commands:
        list.append(teletypes.BotCommand(key, commands[key]))
    return list

regularCommandsList = commands_list(commands_langs[DEFAULT_LANG].get_regular())
privilegedCommandsList = commands_list(commands_langs[DEFAULT_LANG].get_privileged())
offlineCommandsList = commands_list(commands_langs[DEFAULT_LANG].offline)

def set_regular_commands(bot) :
    for lang in commands_langs:
        thisLangCommands = commands_get(lang).get_regular()
        bot.set_my_commands(commands=commands_list(thisLangCommands), language_code=lang)
    logger.debug('Regulars commands set')

def delete_regular_commands(bot) :
    for lang in commands_langs:
        bot.delete_my_commands(language_code=lang)
    logger.debug('Regulars commands deleted')

def set_privileged_commands(bot) :
    bot.set_my_commands(commands=privilegedCommandsList, scope=privileged_scope)
    logger.debug('Privileged commands set')

def delete_privileged_commands(bot) :
    bot.delete_my_commands(scope=privileged_scope)
    logger.debug('Privileged commands deleted')

def set_commands(bot) :
    bot.set_my_commands(commands=regularCommandsList)
    set_privileged_commands(bot)
    set_regular_commands(bot)

def delete_commands(bot) :
    bot.delete_my_commands()
    delete_privileged_commands(bot)
    delete_regular_commands(bot)

def set_offline(bot) :
    delete_commands(bot)
    bot.set_my_commands(commands=offlineCommandsList)
    logger.debug('Commands set to offline')

def cms_menu(lang : str) :
    cms_menu = commands_get(lang).menu
    cms_diary = commands_get(lang).diary
    menu = cms_string(cms_menu)
    menu += "\n<b>Diary</b>\n"
    menu += cms_string(cms_diary)
    return menu

def cms_string(cms : dict) :
    result = ''
    for key in cms:
        result += f'/{key} — {cms[key]}\n'
    return result