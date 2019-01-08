import datetime

def yesterdate():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    return str(yesterday)

def todaydate():
    today = backtodate(1)
    return str(today)

def backtodate(day=1):
    today = datetime.date.today()
    beforeday = today - datetime.timedelta(day)
    return str(beforeday)


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

if __name__ == '__main__':
    print(todaydate())
    print(yesterdate())
    print(koreaMMDDdate(2016,1,9))
