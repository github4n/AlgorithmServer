from datetime import datetime
import json
import numpy as np

#继承转化json错误字典的的类
class DateEncoder(json.JSONEncoder ):
    def default(self, obj):
        #时间错误
        if isinstance(obj, datetime):
            return obj.__str__()
        #数字错误   数字不可转化为json字符串,只有再转化一次才可以变成json字符串
        elif isinstance(obj, np.integer):
            return int(obj)
        #浮点数错误  浮点数不可转化为json字符串,只有再转化一次才可以变成json字符串
        elif isinstance(obj, np.floating):
            return float(obj)
        #数组错误  数组不可转化为json字符串,只有再转化一次才可以变成json字符串
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
            #如果是byte  转换成str
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)

class AjaxJson():
    def __init__(self):
        self.data = {
            "success" : True,
            "msg" : "成功"
        }
    def getData(self):
        return self.data
#单例
_ajaxJson = AjaxJson().getData()
#获得原始json对象
def getAjaxJson():
    return AjaxJson().getData()

#装换成json字符串格式,再传输
def toJsonStrData(data):
    #ensure_ascii属性 可以转换中文
    data = json.dumps(data,ensure_ascii=False,cls=DateEncoder)
    return data

#装换成json格式数据
def loadsJsonByStrData(data):
    if data.startswith(u'\ufeff'):
        data = data.encode('utf8')[3:].decode('utf8')
    data = json.loads(data,encoding="utf-8")
    return data

#获得json字符串
def getDumpsAjaxJsonByData(data):
    jsonData = getAjaxJson()
    try:
        jsonData["data"] = data
    except Exception as e:
        print(e)
        jsonData["success"] = False
        jsonData["msg"] = "转换数据失败!"
    return toJsonStrData(jsonData)

#获得不成功的数据
def getUnSuccessData(msg):
    jsonData = getAjaxJson()
    jsonData["success"] = False
    jsonData["msg"] = msg
    return toJsonStrData(jsonData)