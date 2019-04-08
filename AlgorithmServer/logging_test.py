
from . import settings

#这里开始是日志
import os
BASE_LOG_DIR = os.path.join(settings.BASE_DIR , "log")   # logging日志文件配置的位置

LOGGING = {
    'version': 1,  # 保留字段
    'disable_existing_loggers': False,      # 不要禁用已经存在的logger实例

    'formatters': {     # 定义三种日志显示的格式
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        'collect': {
            'format': '%(message)s'
        }
    },

    'filters': {    # 定义一个过滤规则
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',  # ():括弧代表在任意时刻都执行
        },
    },

    'handlers': {  # 日志流的处理方式
        'console': {    # 把日志打印到终端时设置的参数
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "info.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 500,  # 日志大小 500M
            'backupCount': 3,  #
            'formatter': 'standard',
            'encoding': 'utf-8',    # 设置编码是为了防止中文编码混乱
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_LOG_DIR, "err.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 500,  # 日志大小 500M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'collect': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切换文件保存
            'filename': os.path.join(BASE_LOG_DIR, "collect.log"),
            'maxBytes': 1024 * 1024 * 500,  # 日志大小 500M
            'backupCount': 5,
            'formatter': 'collect',
            'encoding': "utf-8"
        }
    },
    'loggers': {

       # 默认的logger应用如下配置
        '': {
            'handlers': ['default', 'console', 'error'],  # 上线之后可以把'console'移除
            'level': 'DEBUG',
            'propagate': True,      # propagate：是否向父级logger实例传递日志信息
        },

        # 名为 'collect'的logger还单独处理
        'collect': {
            'handlers': ['console', 'collect'],
            'level': 'INFO',
        }
    },
}