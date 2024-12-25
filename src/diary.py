from telebot import types as teletypes
import os
from params import DEFAULT_LANG, DIARIES_PATH
from utils import name_from_user, log_exception, unix_date_string, get_from_file, save_to_file, get_dictionary_from_files, logger, loggerErrors
from messages import messages_get
from user_handler import add_diary_to_user, remove_diary_from_user

__all__ = ['diary_exists', 'create_diary', 'delete_diary', 'get_diary']

# =============================================== ENTRIES ===============================================

class Entry :
    def __init__(self, requested_by: teletypes.User, message: teletypes.Message, is_personal: bool = True):
        self.requested_by = requested_by
        self.mid = message.id
        self.text = message.text.replace('/rec','').replace('@EsoxDiary_bot','').strip()
        self.cid = message.chat.id
        if message.forward_origin.type == 'user' :
            self.date = message.forward_origin.date
            self.from_user = message.forward_origin.sender_user
        else:
            self.date = message.date
            self.from_user = message.from_user
        if message.reply_to_message:
            self.reply_to_user = message.reply_to_message.from_user
            self.reply_to_text = message.reply_to_message.text
        else:
            self.reply_to_user = None
            self.reply_to_text = None
        self.type = self.define_type(message)
        if self.type != 'text' : raise Exception('Non text entries not supported yet')

    def __str__(self) :
        return self.format(DEFAULT_LANG)
    
    def define_type(self, message) :
        if message.text : return 'text'
        if message.photo : return 'photo'
        if message.video : return 'video'
        if message.voice : return 'voice'
        return None
    
    def format(self, language : str) :
        try:
            functions = {
                'text' : self.format_text
            }
            return functions[self.type](language)
        except Exception as e:
            log_exception(e)
            return None
    
    def format_text(self, language : str) :
        date = unix_date_string(self.date)
        author = name_from_user(self.from_user)
        text = self.text
        requestor = name_from_user(self.requested_by)
        msgs = messages_get(language)
        if self.reply_to_user :
            reply_to_user = name_from_user(self.reply_to_user)
            reply_to_text = self.reply_to_text
            return f'{msgs.entry_text_info(date, author, text)}\n\n{msgs.entry_ending(requestor)}\n{msgs.entry_textreply_info(reply_to_user, reply_to_text)}'
        return f'{msgs.entry_text_info(date, author, text)}\n\n{msgs.entry_ending(requestor)}'


# =============================================== DIARIES ===============================================


class Diary :
    def __init__(self, chat : teletypes.Chat) :
        self.cid = chat.id
        self.entries = []
        self.entries_by_date = {}
        self.type = chat.type
        self.title = chat.title
        self.participants = []
        diaries_dict.update({self.cid : self})
        self.save_diary_to_file()
    
    def create_entry(self, requested_by: teletypes.User, message: teletypes.Message, is_personal: bool) :
        try:
            entry = Entry(requested_by, message, is_personal)
        except Exception as e:
            raise e
        else :
            self.add_entry(entry)

    def add_entry(self, entry : Entry) :
        self.entries.append(entry)
        self.date_add(entry)
        self.save_diary_to_file()

    def remove_entry(self, entry : Entry) :
        self.entries.remove(entry)
        self.date_remove(entry)
        self.save_diary_to_file()

    def date_add(self, entry: Entry) :
        date = entry.date
        if date in self.entries_by_date : 
            self.entries_by_date[date].append(entry)
        else : 
            self.entries_by_date.update({date : [entry]})

    def date_remove(self, entry: Entry) :
        date = entry.date
        self.entries_by_date[date].remove(entry)
        if self.entries_by_date[date] == [] :
            self.entries_by_date.pop(date)

    def remove_whole_date(self, date: int) :
        if date in self.entries_by_date :
            self.entries_by_date.pop(date)
        self.save_diary_to_file()

    def retrieve_entries(self, date: int) :
        if date not in self.entries_by_date: return []
        return self.entries_by_date[date]
    
    def retrieve_all_entries(self) :
        entries = []
        for date in self.entries_by_date:
            for entry in self.entries_by_date[date] :
                entries.append(entry)
        return entries
    
    def save_diary_to_file(self) :
        cid = self.cid
        path = f'{DIARIES_PATH}/{cid}'
        save_to_file(path, self)

    def remove_participant(self, uid:int) :
        if uid in self.participants :
            self.participants.remove(uid)
            remove_diary_from_user(uid, self.cid)
        logger.debug(f'Removed participant {uid} from private diary {self.cid}')

    def remove_all_participant(self) :
        for uid in self.participants :
            self.remove_participant(uid)

    def delete_diary(self) :
        cid = self.cid
        path = f'{DIARIES_PATH}/{cid}'
        diaries_dict.pop(cid)
        os.remove(path)


class PrivateDiary(Diary) :
    def __init__(self, chat : teletypes.Chat) :
        super().__init__(chat)
        uid = chat.id
        self.participants = [uid]
        add_diary_to_user(uid, self.cid)

    def add_participant(self, uid:int) :
        logger.debug(f'Cant add participant to private diary {self.cid}')

class GroupDiary(Diary) :
    def __init__(self, chat : teletypes.Chat) :
        super().__init__(chat)

    def add_participant(self, uid:int) :
        if uid not in self.participants :
            self.participants.append(uid)
            add_diary_to_user(uid, self.cid)
        logger.debug(f'Added participant {uid} to group diary {self.cid}')


# ============================================== FUNCTIONS ==============================================

def diary_exists(chat_id : int) -> bool :
    return chat_id in diaries_dict

def get_diary(chat_id : int) -> PrivateDiary | GroupDiary :
    try:
        diary = diaries_dict[chat_id]
    except Exception as e:
        log_exception(e)
        diary = None
    return diary

def create_diary(chat : teletypes.Chat) :
    if chat.type == "private" : return PrivateDiary(chat)
    if chat.type == "group" : return GroupDiary(chat)
    raise Exception('Chat type not supported yet (only private and group chats supported)')

def delete_diary(chat_id : int) :
    diaries_dict[chat_id].remove_diary()

def get_diary_from_file(cid : int) -> PrivateDiary | GroupDiary | None :
    path = f'{DIARIES_PATH}/{cid}'
    return get_from_file(path)

def get_diaries_from_files() -> dict :
    return get_dictionary_from_files(DIARIES_PATH)


# ============================================== START FUNCTIONS ==============================================

diaries_dict = get_diaries_from_files()