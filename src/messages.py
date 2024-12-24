from params import DEFAULT_LANG
from commands import cms_menu

def messages_get(lang) :
    msgs : Messages = langs_dict[lang]
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
langs_dict = {}
# -------------------------------------- ENGLISH --------------------------------------
class Messages :
    language = DEFAULT_LANG
    def __init__(self, language):
        self.language = language
        langs_dict.update({language : self})
    def __str__(self):
        return f"messagesIn{self.language.capitalize()}"
    warn_ban1 =             "You've sent too many messages in a short time! You're now banned for 60 seconds"
    warn_ban2 =             "For more info, use /help"
    warn_debug =            "Bot is under maintenance right now. Try again later"
    debug_on =              "Debug mode on"
    debug_off =             "Debug mode off"
    permaban =              lambda self, username: f'User {username} is permabanned'
    help_intro_text =       "Welcome to <b>EsoxDiaryBot</b>. This bot offers you a diary for personal use or any groupchat this bot is added to."
    help_commands_text =    "You can use me through this commands: \n\n" + cms_menu(language)
    ban_info =              "Keep in mind that misuse of the bot such as spam can lead to a temporal ban"
    help_ending =           'You can check the code running behind this bot <a href="https://github.com/bcochon/telegramEeveeBot">here</a>'
    start =                 "Welcome to my bot!"
    muted =                 "Muted. I will no longer answer to messages I don't understand"
    unmuted =               "Unmuted. I will tell you if I don't understand a message"
    quit =                  "Send /y to confirm closing"
    quitted =               "Terminating program..."
    quit_cancel =           "Bot closing cancelled"
    default =               "I didn't understand that. Use /help to know what I can do"
    entry_text_info =       lambda self, date, username, text: f'Date: {date}\n<b>{username}</b> said : "{text}"'
    entry_ending =          lambda self, requestor: f'<i>Entry requested by {requestor}</i>'
    diary_already_created = "This chat already has a diary created"
    diary_created =         "Diary created successfully. Use /rec to add an entry to the diary"
    no_diary =              "There is no diary created for this chat yet. Use /create to create a diary"
    entry_added =           "Succesfully added entry to diary"
    check =                 "Sending entries..."
    no_entries =            "No entries yet for this diary"
en_msgs = Messages('en')

# -------------------------------------- SPANISH --------------------------------------
es_msgs = Messages(language = 'es')
es_msgs.warn_ban1 =             "Enviaste muchos mensajes en poco tiempo\\! Estás baneado por 60 segundos"
es_msgs.warn_ban2 =             "Para más información, usa /help"
es_msgs.warn_debug =            "El bot se encuentra en mantenimiento ahora mismo. Intenta de nuevo más tarde"
es_msgs.permaban =              lambda username: f'El usuario {username} se encuentra baneado de forma permanente'
es_msgs.help_intro_text =       "Bienvenido a <b>EsoxDiaryBot</b>. Este bot te permite tener un diario personal o para cualquier grupo al que añadas este bot."
es_msgs.help_commands_text =    "Estos son los comandos que puedes usar: \n\n" + cms_menu('es')
es_msgs.ban_info =              "Ten en cuenta que abusar del bot, como mediante spam, puede resultar en un ban temporal"
es_msgs.help_ending =           'Puedes encontrar el código detrás de este bot <a href="https://github.com/bcochon/telegramEeveeBot">aquí</a>'
es_msgs.start =                 "Bienvenido a mi bot!"
es_msgs.muted =                 "Muteado. Ya no voy a responderte si no entiendo un mensaje"
es_msgs.unmuted =               "Desmuteado. Voy a avisarte si no entiendo un mensaje"
es_msgs.quit =                  "Usa /y para confirmar apagar el bot"
es_msgs.quitted =               "Terminando programa..."
es_msgs.quit_cancel =           "Apagado de bot cancelado"
es_msgs.default =               "No entendí lo que dijiste. Usa /help para saber qué puedo hacer"
es_msgs.entry_text_info =       lambda date, username, text: f'Fecha: {date}\n<b>{username}</b> dijo : "{text}"'
es_msgs.entry_ending =          lambda requestor: f'<i>Entrada grabada por {requestor}</i>'
es_msgs.diary_already_created = "Este chat ya tiene un diario creado"
es_msgs.diary_created =         "Diario creado correctamente. Usa /rec para añadir una entrada a este diario"
es_msgs.no_diary =              "No hay un diario creado para este chat aún. Usa /create para crear un diario"
es_msgs.entry_added =           "Entrada añadida al diario con éxito"
es_msgs.check =                 "Enviando entradas..."
es_msgs.no_entries =            "Aún no hay entradas para este diario"