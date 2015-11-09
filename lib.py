import time


def get_formated_time():
    struct_time = time.localtime()
    year = struct_time.tm_year
    month = struct_time.tm_mon
    day = struct_time.tm_mday
    hour = struct_time.tm_hour
    min = struct_time.tm_min
    sec = struct_time.tm_sec
    formated_time = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(min) + ":" + str(sec)
    return formated_time
