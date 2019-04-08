from database.poHelper import EtomPoHelper
from utils import timeUtils
import logging
from utils import QichachaEnum

logger = logging.getLogger('django')

poHelper = EtomPoHelper
#三小时内只能爬取30次完整企业信息
maxThreeHoursTimes = 75
#天只能爬取270次完整企业信息
maxOneDayTimes = 600
#两天的秒数
twoDaySeconds = 172800
oneDaySeconds = 86400
threeHoursSenonds = 10800
#分四段爬取
BIN_SYSTEM = 14

#解说:首先判断已登录账号的登录时间不超过两天(两天过期),且爬取的三小时内次数不超过30条,一天不超过270条


#获取账号,规则,三小时内只能爬取30次完整企业信息,一天只能爬取270次完整企业信息
def getLoginAccount():
    #判断是否需要重新获取登录账号
    flag = getAleradyLoginAccount()
    #需要登录账号
    login_accounts = []
    if flag:
        #改变所有可以使用的账号
        changeUserFlag()
        #获取上次登录时间小于三小时的账号,而且符合所有条件
        last_three_hours = timeUtils.get_time(hours=-3)
        query_sql = "SELECT PHONE_ID,PHONE_NUM,PHONE_PWD FROM crm_phone WHERE USER_FLAG = %s AND TODAY_CRAWLING_TIMES < %s  AND THREE_HOURS_CRAWLING_TIMES < %s AND LAST_LOGIN_TIME <= %s ORDER BY LAST_LOGIN_TIME ASC"
        params = [QichachaEnum.USER_FLAG_TRUE, maxOneDayTimes, maxThreeHoursTimes, last_three_hours]
        data_list = poHelper.fetchall(sql=query_sql,params=params)
        print(data_list)
        if len(data_list) > 0:
            data = data_list[0]
            phone_id = data[0]
            account = {
                "phone":data[1],
                "pwd":data[2]
            }
            now_time = timeUtils.get_time()
            update_sql = "UPDATE crm_phone SET IS_LOGIN_NOW = %s,LAST_LOGIN_TIME = %s WHERE  PHONE_ID = %s"
            params = [QichachaEnum.IS_LOGIN_NOW_TRUE, now_time, phone_id]
            row = poHelper.update(update_sql,params)
            logger.info("获得登录账号%s个" % str(row))
            print("获得登录账号%s个" % str(row))
            print("登录时间:%s" % now_time)
            login_accounts.append(account)
            return login_accounts
        else:
            print("没有可登陆账号")
            logger.info("没有可登陆账号")
            return False
    else:
        #不需要登录账号
        print("不需要登录账号")
        return login_accounts



#改变所有一天没有登录过的账号的状态
def changeUserFlag():
    #修改一天以前的登录状态,今天可以登录
    one_day_ago = timeUtils.get_time(days=-1)
    update_sql = "UPDATE crm_phone SET TODAY_USER_FLAG = %s,THREE_HOURS_CRAWLING_TIMES = 0,TODAY_CRAWLING_TIMES = 0,IS_LOGIN_NOW = %s WHERE USER_FLAG = %s AND LAST_LOGIN_TIME <= %s"
    param = [QichachaEnum.TODAY_USER_FLAG_TRUE, QichachaEnum.IS_LOGIN_NOW_FALSE, QichachaEnum.USER_FLAG_TRUE, one_day_ago]
    row = poHelper.update(update_sql, params=param)
    logger.info("重置一天的账号登录状态为%s%s" % (str(row),"个"))
    #把已登录的账号修改为未登录
    update_sql = "UPDATE crm_phone SET IS_LOGIN_NOW = %s WHERE IS_LOGIN_NOW = %s"
    param = [QichachaEnum.IS_LOGIN_NOW_FALSE, QichachaEnum.IS_LOGIN_NOW_TRUE]
    row = poHelper.update(update_sql, params=param)
    logger.info("修改当天可以使用账号的登录状态为可登录,清空登录状态%s%s" % (str(row),"个"))

#增加一次修改一次个数
def addOneTimes():
    print("爬取成功,增加一次")
    query_sql = "SELECT TODAY_CRAWLING_TIMES,THREE_HOURS_CRAWLING_TIMES,HAVE_ACQUIRED_ALL,PHONE_NUM FROM crm_phone WHERE USER_FLAG = %s AND IS_LOGIN_NOW = %s"
    params = [QichachaEnum.USER_FLAG_TRUE, QichachaEnum.IS_LOGIN_NOW_TRUE]
    data_list = poHelper.fetchall(sql=query_sql, params=params)
    print(data_list)
    if data_list is None or len(data_list) < 1:
        print("没有登录账号,返回")
        return
    data = data_list[0]
    TODAY_CRAWLING_TIMES = data[0]
    THREE_HOURS_CRAWLING_TIMES = data[1]
    HAVE_ACQUIRED_ALL = data[2]
    PHONE_NUM = data[3]
    TODAY_CRAWLING_TIMES += 1
    THREE_HOURS_CRAWLING_TIMES += 1
    HAVE_ACQUIRED_ALL += 1
    update_sql = "UPDATE crm_phone SET TODAY_CRAWLING_TIMES = %s,THREE_HOURS_CRAWLING_TIMES = %s,HAVE_ACQUIRED_ALL = %s WHERE USER_FLAG = %s AND IS_LOGIN_NOW = %s"
    param = [TODAY_CRAWLING_TIMES, THREE_HOURS_CRAWLING_TIMES, HAVE_ACQUIRED_ALL, QichachaEnum.USER_FLAG_TRUE,
             QichachaEnum.IS_LOGIN_NOW_TRUE]
    row = poHelper.update(update_sql, params=param)
    logger.info("修改了%s条账号" % str(row))
    logger.info("账号:%s增加了一条" % (PHONE_NUM))

#重置
def reductionAccount(lastLoginTime,todayTimes,threeHoursTimes):
    three_hour_time = 0
    now_time = timeUtils.get_time()  # 现在
    # now_time_day = now_time[0:10]
    # lastLoginTime_day = lastLoginTime[0:10]
    diff_time = timeUtils.get_date_diff_second(lastLoginTime,now_time)
    #如果今天大于一天时间(昨天),全部置位可使用账号
    if diff_time > oneDaySeconds:
        print("如果今天大于一天时间(昨天),全部置为可使用账号")
        update_sql = "UPDATE crm_phone SET THREE_HOURS_CRAWLING_TIMES = %s,TODAY_USER_FLAG = %s,TODAY_CRAWLING_TIMES = 0 WHERE IS_LOGIN_NOW = %s"
        param = [three_hour_time, QichachaEnum.TODAY_USER_FLAG_TRUE, QichachaEnum.IS_LOGIN_NOW_TRUE]
        row = poHelper.update(update_sql,params=param)
        logger.info("修改了%s条账号" % str(row))
        return
    #普通修改,如果今天总次数大于一天最大次数,置为不可用状态
    if todayTimes >= maxOneDayTimes:
        update_sql = "UPDATE crm_phone SET THREE_HOURS_CRAWLING_TIMES = %s,TODAY_USER_FLAG = %s,TODAY_CRAWLING_TIMES = 0 WHERE IS_LOGIN_NOW = %s"
        param = [three_hour_time, QichachaEnum.TODAY_USER_FLAG_FALSE, QichachaEnum.IS_LOGIN_NOW_TRUE]
        row = poHelper.update(update_sql, params=param)
        logger.info("修改了%s条账号" % str(row))
        return
    #如果三小时内次数大于30次,three置空
    if threeHoursTimes >= maxThreeHoursTimes:
        update_sql = "UPDATE crm_phone SET THREE_HOURS_CRAWLING_TIMES = %s WHERE IS_LOGIN_NOW = %s"
        param = [three_hour_time, QichachaEnum.IS_LOGIN_NOW_TRUE]
        row = poHelper.update(update_sql, params=param)
        logger.info("修改了%s条账号" % str(row))
        return
    print("还原登录账号")

#获取当前登录账号
def getAleradyLoginAccount():
    query_sql = "SELECT PHONE_ID,LAST_LOGIN_TIME,TODAY_CRAWLING_TIMES,THREE_HOURS_CRAWLING_TIMES  FROM crm_phone WHERE USER_FLAG = %s AND IS_LOGIN_NOW = %s"
    params = [QichachaEnum.USER_FLAG_TRUE, QichachaEnum.IS_LOGIN_NOW_TRUE]
    data_list = poHelper.fetchall(sql=query_sql,params=params)
    print(data_list)
    if data_list is None or len(data_list) < 1:
        # print("修改数据库,把每天的次数加上,还有把(三小时)次数置空,然后返回查询新账号的标识")
        print("没有登录账号,返回")
        return True
    data = data_list[0]
    LAST_LOGIN_TIME = data[1]
    TODAY_CRAWLING_TIMES = data[2]
    THREE_HOURS_CRAWLING_TIMES = data[3]
    #判断三小时内次数
    if THREE_HOURS_CRAWLING_TIMES >= maxThreeHoursTimes:
        logger.info("还原账号状态")
        print("还原账号状态")
        reductionAccount(lastLoginTime=LAST_LOGIN_TIME,todayTimes=TODAY_CRAWLING_TIMES,threeHoursTimes=THREE_HOURS_CRAWLING_TIMES)
        return True
    #判断一天次数
    if TODAY_CRAWLING_TIMES >= maxOneDayTimes:
        logger.info("还原账号状态")
        print("还原账号状态")
        reductionAccount(lastLoginTime=LAST_LOGIN_TIME, todayTimes=TODAY_CRAWLING_TIMES,threeHoursTimes=THREE_HOURS_CRAWLING_TIMES)
        return True
    now_time = timeUtils.get_time() #现在
    diff_time = timeUtils.get_date_diff_second(start_str=LAST_LOGIN_TIME,end_str=now_time)
    #判断登录时间超时两天
    if diff_time >= oneDaySeconds:
        logger.info("还原账号状态")
        print("还原账号状态")
        reductionAccount(lastLoginTime=LAST_LOGIN_TIME, todayTimes=TODAY_CRAWLING_TIMES,threeHoursTimes=THREE_HOURS_CRAWLING_TIMES)
        return True
    logger.info("返回不需要重新登录的标识")
    print("返回不需要重新登录的标识")
    return False

#获取公司名称
def getCompanyName(data_list,bin_system):
    if not data_list:
        return None
    for data in data_list:
        data_bin_system = data[1]
        if int(data_bin_system) & bin_system != bin_system:
            name = data[0]
            unique= data[2]
            relaName = data[3]
            print("爬取企业名称为:%s" % name)
            return name,unique,relaName

def setNewCompanyCrawling(name,bin_system,is_can_crawling = QichachaEnum.IS_CAN_CRAWLING_YES):
    data = getCompanyByName(name)
    if not data:
        return
    #是否可以爬
    IS_CAN_CRAWLING = QichachaEnum.IS_CAN_CRAWLING_YES
    if QichachaEnum.IS_CAN_CRAWLING_YES != data[2] or QichachaEnum.IS_CAN_CRAWLING_YES != is_can_crawling:
        IS_CAN_CRAWLING = QichachaEnum.IS_CAN_CRAWLING_NO
    new_system = str(int(data[1]) | bin_system)
    #是否爬完
    IS_CRAWLING = QichachaEnum.IS_CRAWLING_NO
    if int(new_system) >= BIN_SYSTEM:
        IS_CRAWLING =  QichachaEnum.IS_CRAWLING_YES
    item = (IS_CRAWLING, new_system,IS_CAN_CRAWLING,name)
    param = list(item)
    update_sql = "UPDATE crm_crawling_company SET IS_CRAWLING = %s,BIN_SYSTEM = %s, IS_CAN_CRAWLING = %s WHERE NAME = %s"
    row = poHelper.update(update_sql,param)
    print("已完成爬取：%s条" % str(row))


def updateUnique(name,UNIQUE_ID,relaCompanyName):
    update_sql = "UPDATE crm_crawling_company SET UNIQUE_ID = %s,RELA_NAME = %s WHERE NAME = %s"
    param = [UNIQUE_ID,relaCompanyName,name]
    row = poHelper.update(update_sql, param)
    print("增加UNIQUE_ID字段：%s条" % str(row))

def getCompanyByName(name):
    query_sql = "SELECT NAME,BIN_SYSTEM,IS_CAN_CRAWLING FROM crm_crawling_company WHERE NAME = %s"
    params = [name]
    data = poHelper.fetchone(query_sql, params)
    return data

def getAllCompany():
    query_sql = "SELECT NAME,BIN_SYSTEM,UNIQUE_ID,RELA_NAME FROM crm_crawling_company WHERE IS_CAN_CRAWLING = 'Y' AND BIN_SYSTEM < %s AND IS_CRAWLING = 'N'"
    params = [BIN_SYSTEM]
    data_list = poHelper.fetchall(query_sql, params)
    return data_list


#修改状态
def updateCompanyStatus(name,isCanCrawling,isCrawling):
    update_sql = "UPDATE crm_crawling_company SET IS_CAN_CRAWLING = %s , IS_CRAWLING = %s WHERE NAME = %s"
    params = [isCanCrawling,isCrawling,name]
    row = poHelper.update(update_sql,params)
    print("修改数据%s行" % str(row))
    return row

#修改状态为已爬取,爬取成功
def updateCompanyCrawlingSuccess(name):
    updateCompanyStatus(name=name, isCanCrawling=QichachaEnum.IS_CAN_CRAWLING_YES, isCrawling=QichachaEnum.IS_CRAWLING_YES)

#修改为不可爬取状态
def updateCompanyCanCrawlingFail(name):
    updateCompanyStatus(name=name, isCanCrawling=QichachaEnum.IS_CAN_CRAWLING_NO, isCrawling=QichachaEnum.IS_CRAWLING_YES)


if __name__ == '__main__':
    # data_result = getLoginAccount()
    # print(data_result)
    # addOneTimes()
    # getCompanyName()
    # updateCompanyCrawlingSuccess("华为")
    data_list = getAllCompany()
    data = getCompanyName(data_list,QichachaEnum.BASE_BIN_SYSTEM)
    print(data)