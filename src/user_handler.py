import time
import threading
import os

from params import USERS_PATH
from utils import logger, save_to_file, get_from_file, get_dictionary_from_files

BAN_TIME = 60 #seconds

class UserSteps :
    DEFAULT = 0
    QUIT = 1

class CustomUserInfo:
    def __init__(self, uid):
        self.uid = uid
        self.spamCount = 0
        self.step = 0
        self.banned = False
        self.diaries = []
        self.save_user_to_file()

    def __str__(self):
        return f"User{self.id} (Banned={self.banned})"

    def count_msg(self):
        self.spamCount += 1
        if self.spamCount > 6:
            self.ban(BAN_TIME)
        thread = threading.Thread(target=self.uncount_msg)
        thread.start()

    def uncount_msg(self):
        time.sleep(30)
        self.spamCount -= 1

    def ban(self, banTime):
        self.banned = True
        logger.info(f"Banned user {self.uid} for {BAN_TIME} seconds")
        thread = threading.Thread(target=self.unban, args=(banTime,))
        thread.start()

    def unban(self, banTime):
        time.sleep(banTime)
        self.banned = False

    def add_diary(self, diary_cid : int) :
        if diary_cid not in self.diaries :
            self.diaries.append(diary_cid)
        logger.debug(f'Added diary {diary_cid} to user {self.uid} diaries')
        self.save_user_to_file()

    def remove_diary(self, diary_cid) :
        if diary_cid in self.diaries :
            self.diaries.remove(diary_cid)
        logger.debug(f'Removed diary {diary_cid} from user {self.uid} diaries')
        self.save_user_to_file()

    def save_user_to_file(self) :
        uid = self.uid
        path = f'{USERS_PATH}/{uid}'
        save_to_file(path, self)


def unban_all_users(users : dict) :
    for user in users :
        users[user].banned = False
        users[user].spamCount = 0

def register_user(uid) -> CustomUserInfo :
    if uid not in users :
        newUser = CustomUserInfo(uid)
        users.update({uid : newUser})
        logger.debug(f"New user {uid} detected")
    return users[uid]

def check_spam(id):
    if not check_banned(id) :
        spammer = register_user(id)
        spammer.count_msg()

def check_banned(id):
    return register_user(id).banned

def get_user_step(uid):
    if uid not in users:
        register_user(uid)
    return users[uid].step

def set_user_step(uid, step):
    user = register_user(uid)
    user.step = step

def add_diary_to_user(uid, diary_cid) :
    user = register_user(uid)
    user.add_diary(diary_cid)

def remove_diary_from_user(uid, diary_cid) :
    user = register_user(uid)
    user.remove_diary(diary_cid)

def get_user_from_file(uid : int) -> CustomUserInfo | None :
    path = f'{USERS_PATH}/{uid}'
    return get_from_file(path)

def get_users_from_files() -> dict :
    return get_dictionary_from_files(USERS_PATH)


# ============================================== START FUNCTIONS ==============================================

users = get_users_from_files()
unban_all_users(users)