# -*- coding: utf-8 -*-

# #JAVA 数据库地址
# JAVA_DBHOST = '119.23.229.158'
# JAVA_DBUSER = "root"#账号
# JAVA_DBPWD = "666666"#测试库密码
# JAVA_DBNAME = 'mydb'

JAVA_DBHOST = "192.168.150.20"#JAVA测试库地址
# JAVA_DBHOST = "39.107.53.99"#正式JAVA测试库地址
JAVA_DBUSER = "poadmin"#账号
JAVA_DBPWD = "ETOMDB6666"#测试库密码
JAVA_DBNAME = 'po_service_data'#Java数据库名称
# JAVA_DBNAME = 'po_produce_service'#Java数据库名称  正式
# JAVA_DBNAME = 'po_algorithm'

DBPORT = 3306#端口
DBCHAR = "utf8"



#MQ配置
rabbitMQ_USER='admin'  # 账号
# rabbitMQ_PASSWORD='admin' #测试密码
rabbitMQ_PASSWORD='Rabbit,2018' #正式密码
# rabbitMQ_PORT=5672 #测试端口
rabbitMQ_PORT=5670 #正式端口
# rabbitMQ_HOST='192.168.150.104' #地址
rabbitMQ_HOST='192.168.150.14' #正式地址
# rabbitMQ_QUEUE='testQueue' #队列名
# rabbitMq_EXCHANGE='testExchange'#交换机
rabbitMQ_QUEUE='pythonQueue' #队列名
# rabbitMq_EXCHANGE='pythonExchange'#交换机
# rabbitMQ_QUEUE = "pythonQueue-new"#队列名 测试队列
rabbitMq_EXCHANGE='pythonExchange'#交换机

#测试交换机
test_testExchange = "testExchange"
#测试队列
test_testQueue = "testQueue"


#pythonHbaseid   获得队列里的id
rabbitMq_HBASEID='hbaseKeyQueue'#从这个队列里读取数据
rabbitMQ_INDUSTRYQUEUE='industryQueue' #队列名
rabbitMq_INDUSTRYEXCHANGE='industryExchange'#交换机


rabbitMq_TEXTSIMILARQUEUE='textsimilarQueue'

#重新加工队列
rabbitMQ_REWORK_QUEUE='reworkQueue' #队列名
rabbitMQ_REWORK_EXCHANGE='reworkExchange'#交换机