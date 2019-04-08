#腾讯地图工具类

import requests
from urllib.parse import quote
from utils import AjaxJson

QQ_MAP_KEY = "PZYBZ-YWC6U-SJZVT-24DZQ-JDHLK-BEFK5"

#通过地址获取经纬度
def getLatAndLng(address):
    address = quote(address)
    url = "https://apis.map.qq.com/ws/geocoder/v1/?key=" + QQ_MAP_KEY + "&address="+address
    response = requests.get(url,timeout=3)
    data = {}
    text = response.text
    #装换成json格式数据
    response = AjaxJson.loadsJsonByStrData(text)
    #如果请求失败
    if response["status"] != 0:
        data['lat'] = None
        data['lng'] = None
        return data
    data['lat'] = response['result']['location']['lat']
    data['lng'] = response['result']['location']['lng']
    print(data)
    return data


#按照行读取文件
def readtxt(file):
    with open(file,encoding="utf-8") as f:
        Line = []
        line = f.readline()
        while line:
            Line.append(line.strip())
            line = f.readline()
    return Line


if __name__ == '__main__':
    getLatAndLng("北京市海淀区彩和坊路海淀西大街74号")