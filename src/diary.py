from telebot import types as teletypes
import pickle
import os
from params import DEFAULT_LANG
from params import DIARIES_PATH
from utils import name_from_user
from utils import log_exception
from utils import unix_date_string
from messages import messages_get

__all__ = ['diary_exists', 'create_diary', 'delete_diary', 'get_diary']

# =============================================== ENTRIES ===============================================

class Entry :
    def __init__(self, requested_by: teletypes.User, message: teletypes.Message, is_personal: bool = True):
        self.requested_by = requested_by
        self.mid = message.id
        self.cid = message.chat.id
        self.text = message.text
        self.from_user = message.from_user
        self.date = message.date
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
        return f'{msgs.entry_text_info(date, author, text)}\n\n{msgs.entry_ending(requestor)}'


# =============================================== DIARIES ===============================================


class Diary :
    def __init__(self, chat) :
        self.cid = chat.id
        self.entries = []
        self.entries_by_date = {}
        diaries_dict.update({self.cid : self})
        self.save_diary_to_file()

    def q_entries(self) : len(self.entries_by_date)

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
        try:
            with open(path, 'wb') as f:
                pickle.dump(self, f)
        except Exception as e:
            log_exception(e)

    def delete_diary(self) :
        cid = self.cid
        path = f'{DIARIES_PATH}/{cid}'
        diaries_dict.pop(cid)
        os.remove(path)


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

def get_diary_from_file(cid : int) -> PrivateDiary | GroupDiary | None :
    path = f'{DIARIES_PATH}/{cid}'
    try:
        with open(path, 'rb') as f:
            diary = pickle.load(f)
    except Exception as e:
        log_exception(e)
        diary = None
    return diary

def get_diaries_from_files() -> dict :
    diaries = {}
    diary_files = os.listdir(DIARIES_PATH)
    for s_cid in diary_files :
        cid = int(s_cid)
        diary = get_diary_from_file(cid)
        diaries.update({cid : diary})
    return diaries

diaries_dict = get_diaries_from_files()