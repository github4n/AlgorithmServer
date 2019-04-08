import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pyquery import PyQuery as pq
from utils import AjaxJson,file_path

def get_result(doc):
    length = []
    EleClass = []
    EleId = []
    for i in doc("div").items():
        length.append(len(i.text()))
        EleClass.append(i.attr('class'))
        EleId.append(i.attr('id'))

    # print(length)
    # print(EleClass)
    # print(EleId)

    n=2
    try:
        while n > 1:
            index = length.index(max(length))
            # print(EleClass[index], EleId[index])
            n = EleClass.count(EleClass[index])
            if n > 1:
                length.remove(length[index])
                EleClass.remove(EleClass[index])
                EleId.remove(EleId[index])
            # print('循环中……')
        return EleClass[index], EleId[index]
    except:
        return None,None

def Auto_select(html):
    # url = urlopen('https://new.qq.com/omn/20190121/20190121A1DV9U.html')
    # bsObj = str(BeautifulSoup(url, 'html.parser'))
    length_1 = []

    doc = pq(html)
    doc.find('style').remove()
    doc.find('script').remove()
    doc.find('img').remove()
    Class,Id=get_result(doc)
    # print(Class,Id)

    name='div'+'.'+Class.split()[0]
    it = doc(name).children()
    length=len(it.text())
    for s in it("div").items():
        length_1.append(len(s.text()))
    pre=max(length_1)/length
    # print(pre)
    while pre>0.6:
        length_2=[]
        Class, Id=get_result(it)
        name = 'div' + '.' + Class.split()[0]
        it = doc(name).children()
        length = len(it.text())
        for s in it("div").items():
            length_2.append(len(s.text()))
        pre = max(length_2) / length
        # print(pre)
        # print(Class, Id)
    # print(Class, Id)
    return {'eleClassName':Class,'eleId':Id}


if __name__ == "__main__":
    # url = urlopen('https://mil.news.sina.com.cn/')
    # url = urlopen('https://mil.news.sina.com.cn/dgby/2019-01-22/doc-ihqfskcn9269078.shtml')
    url ='https://new.qq.com/omn/20190121/20190121A1DV9U.html'
    response = requests.get(url)
    # print(response.text)
    res=Auto_select(response.text)
    print(res)
    # print(AjaxJson.getDumpsAjaxJsonByData(res))