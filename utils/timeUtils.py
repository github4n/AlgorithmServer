


#计算时间差
import datetime
import logging
logger = logging.getLogger('django')
oneDaySeconds = 86400
#获取时间差
def get_date_diff_second(start_str, end_str):
    start = datetime.datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
    diff = end - start
    # 相差天数
    days = diff.days
    print('相差天数：', diff.days)
    # 相差秒数
    seconds = diff.seconds
    count_seconds = seconds
    if days > 0:
        count_seconds = days * oneDaySeconds + seconds
    print('相差秒数：', count_seconds)
    # 相差微秒数
    # print('相差微秒数：', diff.microseconds)
    return count_seconds


def get_time(days=0,seconds=0,hours=0,weeks=0):
    now_time = datetime.datetime.now()
    result_time = (now_time + datetime.timedelta(days=days,hours=hours,weeks=weeks,seconds=seconds)).strftime('%Y-%m-%d %H:%M:%S')
    logger.info("得到时间:%s" % result_time)
    print("得到时间:%s" % result_time)
    return result_time


if __name__ == '__main__':
    result = get_date_diff_second('2018-11-21 00:00:00','2018-11-21 23:59:59')
    print(result)
    # get_time(days=-1)