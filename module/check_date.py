import datetime

def check_date(params):
    now = datetime.datetime.now()
    if "TODAY" == params:
        return now, "오늘"
    elif "TOMORROW" == params:
        return now + datetime.timedelta(days=1), "내일"
    elif "A_TOMORROW" == params:
        return now + datetime.timedelta(days=2), "내일모레"
    elif "AA_TOMORROW" == params:
        return now + datetime.timedelta(days=3), "글피"
    elif "AAA_TOMORROW" == params:
        return now + datetime.timedelta(days=4), "그글피"
    elif "YESTERDAY" == params:
        return now - datetime.timedelta(days=1), "어제"
    elif "B_YESTERDAY" == params:
        return now - datetime.timedelta(days=2), "그저께"
    elif "BB_YESTERDAY" == params:
        return now - datetime.timedelta(days=3), "그그저께"
    else:
        return None, None