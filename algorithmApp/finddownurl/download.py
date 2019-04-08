from urllib.request import urlopen#用于获取网页
from bs4 import BeautifulSoup
import re
from utils import file_path

def geturllist(contents,url_in,suffix_path):
    baesObj = BeautifulSoup(contents, 'html.parser')
    # print(bsObj)
    t1 = baesObj.find_all('a')
    # span_list = baesObj.find_all("span")
    # botton_list = baesObj.find_all("botton")
    res = []
    file = open(suffix_path, encoding="utf-8")
    re_list = file.readlines()
    file.close()
    for t2 in t1:
        res_u = []
        res_t = []
        # print(t2)
        re_1='[a-zA-z]+://[^"]*'
        re_url=re.findall(re_1, str(t2))
        if len(re_url)==0:
            url_f = t2.get('href')
        else:
            url_f=re_url[0]
        # print(url_f)
        url = ""
        try:
            if len(url_f) != 0:
                if url_f[0] == '.':
                    url = url_in + url_f[1:]
                elif url_f[0] == '/':
                    if url_in[0] == 'h':
                        list = url_in.split('/')
                        url = list[0] + '//' + list[2] + url_f
                    elif url_in[0] == 'f':
                        list = url_in.split('/')
                        url = list[0] + '//' + list[2] + url_f
                    else:
                        list = url_in.split('/')
                        url = list[0] + url_f
                else:
                    url = url_f
        except:
            pass

        text = t2.get_text()
        # print(url, text)
        for pat in re_list:
            pat=pat.strip().replace('\n','').replace('\r','').replace('\t','')
            # print(pat)
            file_name_t = re.findall(pat, text)
            if len(file_name_t) !=0:
                res_t.append(True)
            file_name_u = re.findall(pat, url)
            if len(file_name_u) !=0:
                res_u.append(True)

        if res_t.count(True)>0:
            res.append(str(t2))
            # print(url,text)
        else:
            if res_u.count(True)>0:
                res.append(str(t2))
                # print(url,text)
            else:
                pass
    # print(res)
    return res

if __name__ == '__main__':
    url='http://www.mot.gov.cn/xiazaizhongxin/ziliaoxiazai/'
    content= urlopen('http://www.mot.gov.cn/xiazaizhongxin/ziliaoxiazai/')
    list_str= geturllist(content,url,file_path.down_load_file)
    print(len(list_str))



