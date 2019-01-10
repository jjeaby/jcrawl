import datetime
import os
import random, string
from os import path


def yesterdate():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    return str(yesterday)

def todaydate():
    today = backtodate(0)
    return str(today)

def backtodate(day=1):
    today = datetime.date.today()
    beforeday = today - datetime.timedelta(day)
    return str(beforeday)

def todaydatehour():
    today = datetime.datetime.now()
    today_date = today.strftime("%Y%m%d%H")
    return today_date



def koreaMMDDdate(year, month, day):
    dt = datetime.datetime(year, month, day)
    koreaMMDD = str(dt.month) + "월" + str(dt.day)+ "일("+ korea_weekday_label(dt.weekday()) + ")"
    return str(koreaMMDD)

def korea_weekday_label(day):
    if day == 0 :
        return "월"
    elif day == 1 :
        return "화"
    elif day == 2 :
        return "수"
    elif day == 3 :
        return "목"
    elif day == 4 :
        return "금"
    elif day == 5 :
        return "토"
    elif day == 6 :
        return "일"

def make_random_word():
    UPP = random.SystemRandom().choice(string.ascii_uppercase)
    LOW1 = random.SystemRandom().choice(string.ascii_lowercase)
    LOW2 = random.SystemRandom().choice(string.ascii_lowercase)
    LOW3 = random.SystemRandom().choice(string.ascii_lowercase)
    LOW4 = random.SystemRandom().choice(string.ascii_lowercase)
    DIG1 = random.SystemRandom().choice(string.digits)
    DIG2 = random.SystemRandom().choice(string.digits)
    DIG3 = random.SystemRandom().choice(string.digits)
    DIG4 = random.SystemRandom().choice(string.digits)
    SPEC1 = random.SystemRandom().choice('!@#$%^&*()')
    SPEC2 = random.SystemRandom().choice('!@#$%^&*()')
    random_word = None
    random_word = UPP + LOW1 + LOW2 + LOW3 + LOW4 + DIG1 + DIG2 + DIG3 + DIG4+ SPEC1 + SPEC2
    random_word = ''.join(random.sample(random_word, len(random_word)))
    return str(random_word)



def write_file(finename=None, mode="w", write_text=""):
    fs = open(finename, mode=mode, encoding="utf-8")
    fs.writelines(write_text + "\n")
    fs.close()

if __name__ == '__main__':
    print(todaydate())
    print(yesterdate())
    print(koreaMMDDdate(2016,1,9))
    print(make_random_word())
    print(todaydatehour())


    start_path = '/my/root/directory'

    list_of_vars = [ "a", "b"]
    list_of_vars = ("apple", "banana", "cherry")

