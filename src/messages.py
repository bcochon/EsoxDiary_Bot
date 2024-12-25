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
    help_rec =              "For recording an entry use the /rec command. The recorded entry must contain text, which is took from the message you are answering to when sending /rec. If the /rec message is not answering to any other message, the rest of the /rec message text is used. For example, sending "+'"/rec hello</i>"'+", without answering to any other message, will record an entry with the text <i>hello</i>, but will record the text from the message its answering to if there is one"
    help_rec_disclaimer =   "At the moment, the bot can't detect if you're answering to messages sent by you, only messages sent by other participants. If you want to record a message you sent, you'll have to edit it and add the /rec command at the beggining and then forward it to the bot chat or ask another chat participant to answer to it with the /rec command."
    start =                 "Welcome to my bot!"
    muted =                 "Muted. I will no longer answer to messages I don't understand"
    unmuted =               "Unmuted. I will tell you if I don't understand a message"
    quit =                  "Send /y to confirm closing"
    quitted =               "Terminating program..."
    quit_cancel =           "Bot closing cancelled"
    default =               "I didn't understand that. Use /help to know what I can do"
    entry_text_info =       lambda self, date, username, text: f'Date: {date}\n<b>{username}</b> said : "{text}"'
    entry_textreply_info =  lambda self, username, text: f'After <b>{username}</b> said : "{text}"'
    entry_ending =          lambda self, requestor: f'<i>Entry requested by {requestor}</i>'
    diary_already_created = "This chat already has a diary created"
    diary_created =         "Diary created successfully. Use /rec to add an entry to the diary"
    diary_create_error =    "Ups... couldn't create a diary from this chat. Make sure this is a private or group chat"
    no_diary =              "There is no diary created for this chat yet. Use /create to create a diary"
    already_joined =        "You are already part of this diary"
    invalid_join =          "You can only join groupchat diaries"
    joined =                "Succesfully added user to this diary"
    entry_added =           "Succesfully added entry to diary"
    rec_error =             "Ups... can't turn that message into an entry. Make sure you are correctly using /rec. "+'For more info, use "/help rec"'
    check =                 "Sending entries..."
    no_entries =            "No entries yet for this diary"
    del_diary_confirm =     "Are you sure you want to delete this diary?"
    del_diary =             "Diary deleted"
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
es_msgs.help_rec =              'Para grabar una entrada usa el comando /rec. La entrada debe contener texto, el cual se obtiene del mensaje al que respondes al enviar /rec. Si el mensaje con /rec no está respondiendo a otro, se graba el texto que acompaña al mensaje con /rec. Por ejemplo, al enviar "/rec hola", sin responder a otro mensaje, se grabará una entrada con el texto <i>hola</i>, pero si se responde a otro mensaje, se grabará en la entrada el texto del mensaje respondido'
es_msgs.help_rec_disclaimer =   "Por el momento, el bot no puede detectar respuestas a mensajes del mismo usuario que responde, solo respuestas a otros usuarios del chat. Si quieres grabar una entrada con un mensaje propio, Tendrás que editarlo para añadir el comando /rec al comienzo del mensaje y luego reenviar el mensaje al chat del bot, o pedirle a otro participante del chat que responda al mensaje con el comando /rec."
es_msgs.start =                 "Bienvenido a mi bot!"
es_msgs.muted =                 "Muteado. Ya no voy a responderte si no entiendo un mensaje"
es_msgs.unmuted =               "Desmuteado. Voy a avisarte si no entiendo un mensaje"
es_msgs.quit =                  "Usa /y para confirmar apagar el bot"
es_msgs.quitted =               "Terminando programa..."
es_msgs.quit_cancel =           "Apagado de bot cancelado"
es_msgs.default =               "No entendí lo que dijiste. Usa /help para saber qué puedo hacer"
es_msgs.entry_text_info =       lambda date, username, text: f'Fecha: {date}\n<b>{username}</b> dijo : "{text}"'
es_msgs.entry_textreply_info =  lambda username, text: f'Luego de que <b>{username}</b> dijera : "{text}"'
es_msgs.entry_ending =          lambda requestor: f'<i>Entrada grabada por {requestor}</i>'
es_msgs.diary_already_created = "Este chat ya tiene un diario creado"
es_msgs.diary_created =         "Diario creado correctamente. Usa /rec para añadir una entrada a este diario"
es_msgs.diary_create_error =    "Ups... no se pudo crear un diario para este chat. Asegúrate de estar en un chat privado o de grupo"
es_msgs.no_diary =              "No hay un diario creado para este chat aún. Usa /create para crear un diario"
es_msgs.already_joined =        "Ya eres integrante de este diario"
es_msgs.invalid_join =          "Solo puedes unirte a diarios de chats grupales"
es_msgs.joined =                "Usuario añadido al diario con éxito"
es_msgs.entry_added =           "Entrada añadida al diario con éxito"
es_msgs.rec_error =             "Ups... ese mensaje no puede convertirse en entrada. Asegúrate de estar usando correctamente el comando /rec. "+'Para más información, usa "/help rec"'
es_msgs.check =                 "Enviando entradas..."
es_msgs.no_entries =            "Aún no hay entradas para este diario"
es_msgs.del_diary_confirm =     "¿Seguro que quieres eliminar este diario?"
es_msgs.del_diary =             "Diario eliminado"