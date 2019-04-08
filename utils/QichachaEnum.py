
from enum import Enum

#企查查枚举
class QichachaEnum(Enum):
    #可以使用
    USER_FLAG_TRUE = 'T'
    #不可以使用
    USER_FLAG_FALSE = 'F'
    #现在登陆中
    IS_LOGIN_NOW_TRUE = 'T'
    #现在没有登陆
    IS_LOGIN_NOW_FALSE = 'F'
    #今天还可以使用
    TODAY_USER_FLAG_TRUE = '1'
    #今天不可以使用
    TODAY_USER_FLAG_FALSE = '2'

USER_FLAG_TRUE = 'T'
USER_FLAG_FALSE = 'F'
IS_LOGIN_NOW_TRUE = 'T'
IS_LOGIN_NOW_FALSE = 'F'
TODAY_USER_FLAG_TRUE = '1'
TODAY_USER_FLAG_FALSE = '2'
#是否可以爬取
IS_CAN_CRAWLING_YES = 'Y'
IS_CAN_CRAWLING_NO = 'N'
#是否已爬取
IS_CRAWLING_YES = 'Y'
IS_CRAWLING_NO = 'N'
#基本信息
BASE_BIN_SYSTEM = 1
#电话等
FIRM_BIN_SYSTEM = 2
#susong
SUSONG_BIN_SYSTEM = 4
#RUN
RUN_BIN_SYSTEM = 8



if __name__ == '__main__':
    print(QichachaEnum.IS_LOGIN_NOW_FALSE.value)