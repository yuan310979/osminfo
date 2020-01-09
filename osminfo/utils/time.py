from datetime import datetime

def cur_time():
    return datetime.now().strftime("%Y%m%d-%H%M%S")