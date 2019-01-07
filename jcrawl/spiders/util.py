import datetime

def yesterdate():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    return yesterday

def todaydate():
    today = datetime.date.today()
    return today


if __name__ == '__main__':
    print(todaydate())
    print(yesterdate())
