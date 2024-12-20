from params import DEFAULT_LANG

def messages_get(lang) :
    msgs = langs_dict[lang]
    if not msgs :
        msgs = langs_dict[DEFAULT_LANG]
    return msgs

def commands_text_generator(commands) :
    result = "Commands: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        result += "/" + key + " — "
        result += commands[key] + "\n"
    return result

# ===================================== LANGUAGES =====================================
# -------------------------------------- ENGLISH --------------------------------------
class Messages :
    language = DEFAULT_LANG
    def __init__(self, language):
        self.language = language
    def __str__(self):
        return f"messagesIn{self.language.capitalize()}"
    warn_ban1 =             "You've sent too many messages in a short time\\! You're now banned for 60 seconds"
    warn_ban2 =             "For more info, use /help"
    warn_debug =            "Bot is under maintenance right now. Try again later"
    debug_on =              "Debug mode on"
    debug_off =             "Debug mode off"
    permaban =              lambda username: f'User {username} is permabanned'
    help_intro_text =       "Bot description"
    help_commands_text =    lambda commands: commands_text_generator(commands)
    ban_info =              "Keep in mind that misuse of the bot such as spam can lead to a temporal ban"
    start =                 "Welcome to my bot!"
    muted =                 "Muted. I will no longer answer to messages I don't understand"
    unmuted =               "Unmuted. I will tell you if I don't understand a message"
    quit =                  "Type y to close the bot"
    quitted =               "Terminating program..."
    quit_cancel =           "Bot closing cancelled"
    default =               "I didn't understand that. Use /help to know what I can do"
en_msgs = Messages('en')

# -------------------------------------- SPANISH --------------------------------------
es_msgs = Messages(language = 'es')
es_msgs.warn_ban1 =             "Enviaste muchos mensajes en poco tiempo\\! Estás baneado por 60 segundos"
es_msgs.warn_ban2 =             "Para más información, usa /help"
es_msgs.warn_debug =            "El bot se encuentra en mantenimiento ahora mismo. Intenta de nuevo más tarde"
es_msgs.permaban =              lambda username: f'El usuario {username} se encuentra baneado de forma permanente'
es_msgs.help_intro_text =       "Descripción del bot"
es_msgs.help_commands_text =    lambda commands: commands_text_generator(commands)
es_msgs.ban_info =              "Ten en cuenta que abusar del bot, como mediante spam, puede resultar en un ban temporal"
es_msgs.start =                 "Bienvenido a mi bot!"
es_msgs.muted =                 "Muteado. Ya no voy a responderte si no entiendo un mensaje"
es_msgs.unmuted =               "Desmuteado. Voy a avisarte si no entiendo un mensaje"
es_msgs.quit =                  "Escribe y para apagar el bot"
es_msgs.quitted =               "Terminando programa..."
es_msgs.quit_cancel =           "Apagado de bot cancelado"
es_msgs.default =               "No entendí lo que dijiste. Usa /help para saber qué puedo hacer"


# ==================================== DICTIONARY =====================================

langs_dict = {
    'en' : en_msgs,
    'es' : es_msgs
}