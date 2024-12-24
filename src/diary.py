from telebot import types as teletypes
from telebot import TeleBot
from params import DEFAULT_LANG
from utils import name_from_user
from utils import log_exception
from utils import message_date_string
from messages import messages_get

__all__ = ['diary_exists', 'create_diary', 'delete_diary', 'get_diary']

# =============================================== ENTRIES ===============================================

class Entry :
    def __init__(self, requested_by: teletypes.User, message: teletypes.Message, is_personal: bool = True):
        self.requested_by = requested_by
        self.message = message
        self.date = message.date
        self.type = self.define_type()
        if self.type != 'text' : raise Exception('Non text entries not supported yet')

    def __str__(self) :
        return self.format(DEFAULT_LANG)
    
    def define_type(self) :
        if self.message.text : return 'text'
        if self.message.photo : return 'photo'
        if self.message.video : return 'video'
        if self.message.voice : return 'voice'
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
        date = message_date_string(self.message)
        author = name_from_user(self.message.from_user)
        text = self.message.text
        requestor = name_from_user(self.requested_by)
        msgs = messages_get(language)
        return f'{msgs.entry_text_info(date, author, text)}\n\n{msgs.entry_ending(requestor)}'


# =============================================== DIARIES ===============================================

diaries_dict = {}

class Diary :
    def __init__(self, chat) :
        self.cid = chat.id
        diaries_dict.update({self.cid : self})

    entries_by_date = {}

    def add_entry(self, requested_by: teletypes.User, message: teletypes.Message, is_personal: bool) :
        new_entry = Entry(requested_by, message, is_personal)
        self.date_add(new_entry)

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

    def retrieve_entries(self, date: int) :
        if date not in self.entries_by_date: return []
        return self.entries_by_date[date]
    
    def retrieve_all_entries(self) :
        entries = []
        for date in self.entries_by_date:
            for entry in self.entries_by_date[date] :
                entries.append(entry)
        return entries

    def remove_diary(self) :
        diaries_dict.pop(self.cid)


class PrivateDiary(Diary) :
    type = 'private'
    participants = []

class GroupDiary(Diary) :
    type = 'group'
    participants = []


# ============================================== FUNCTIONS ==============================================

def diary_exists(chat_id : int) -> bool :
    return chat_id in diaries_dict

def get_diary(chat_id : int) -> PrivateDiary | GroupDiary :
    return diaries_dict[chat_id]

def create_diary(chat : teletypes.Chat) :
    if chat.type == "private" : return PrivateDiary(chat)
    if chat.type == "group" : return GroupDiary(chat)
    raise Exception('Chat type diary not supported yet')

def delete_diary(chat_id : int) :
    diaries_dict[chat_id].remove_diary()