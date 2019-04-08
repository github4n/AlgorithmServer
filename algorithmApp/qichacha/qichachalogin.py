import json
import pickle
import re
import time

from selenium import webdriver
#代码中的chrome_options.add_argument()非常关键，一是要以无界面形式运行，二是禁用沙盒，否则程序报错。
#linux上使用,打开方式以无界面打开
from utils import QQMapHelp
from utils import file_path

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # 指定无界面形式运行
chrome_options.add_argument('no-sandbox') # 禁止沙盒


tianyan_cookie_file = file_path.not_user_file
qichacha_cookie_file = file_path.qichacha_drive_cookie_path

#注:这些方法还需要一个插件  下面 chromedriver.exe ,也可以用火狐
# 同目录下(脚本运行目录)放置  chromedriver.exe  这个文件, 下载地址http://npm.taobao.org/mirrors/chromedriver/
# 部署的话最好部署在windows服务器下,安装最新的谷歌浏览器

#天眼查账号登录
def login(url):
    # dirver.maximize_window()
    dirver = webdriver.Chrome(chrome_options=chrome_options)
    dirver.get(url)
    time.sleep(3)
    # page_source = dirver.page_source
    # print(page_source)
    phoneNumber = dirver.find_elements_by_xpath('//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input')
    phone = input("你的电话")
    phoneNumber[0].send_keys(phone)

    password = dirver.find_elements_by_xpath('//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/input')
    # 密码
    passwords = input("你的密码")
    password[0].send_keys(passwords)

    time.sleep(3)

    sublit = dirver.find_elements_by_xpath('//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[5]')
    sublit[0].click()
    time.sleep(3)
    print(dirver.get_cookies())
    print(type(dirver.get_cookies()))

    with open(tianyan_cookie_file, 'wb') as handle:
        pickle.dump(dirver.get_cookies(), handle)
    time.sleep(60)
    # dirver.quit()
#使用微博模拟登陆
def login_qichacha(url,phone,password):
    dirver = webdriver.Chrome(chrome_options=chrome_options)
    dirver.get(url)
    time.sleep(3)

    weibologin = dirver.find_elements_by_xpath('//*[@id="qrcodeLoginPanel"]/div[2]/div/div[3]/a[3]')
    weibologin[0].click()
    time.sleep(5)
    #用户名  或者微博名
    # phone = input("你的电话")
    dirver.find_elements_by_xpath('//*[@id="userId"]')[0].send_keys(phone)
    time.sleep(3)
    #密码
    # password = input("你的微博密码")
    dirver.find_elements_by_xpath('//*[@id="passwd"]')[0].send_keys(password)
    time.sleep(3)
    sublimt = dirver.find_elements_by_xpath('//*[@id="outer"]/div/div[2]/form/div/div[2]/div/p/a[1]')
    sublimt[0].click()
    time.sleep(10)
    print(dirver.get_cookies())
    print(type(dirver.get_cookies()))

    with open(qichacha_cookie_file, 'wb') as handle:
        pickle.dump(dirver.get_cookies(), handle)
    dirver.close()
    # time.sleep(60)
def getCookieStr():
    #打开文件
    with open(qichacha_cookie_file, 'rb') as handle:
        b = pickle.load(handle)
        print(b)
        cookie_str = ''
        for index in b:
            cookie_str += index['name'] + '=' + index['value'] + ';'
        cookie_str = cookie_str[:-1]
        print(cookie_str)
    return cookie_str

#获取登录账号和密码
def get_login_id(login_note_path):
    login_notes = QQMapHelp.readtxt(login_note_path)
    phones = []
    passwords = []
    user_times = []
    for item in  login_notes:
        login_ids = re.split('[()]', item.strip())
        print(login_ids)
        phones.append(login_ids[1])
        passwords.append(login_ids[3])
        user_times.append(int(login_ids[5]))
    #最小的次数
    min_user_times = int(min(user_times))
    #最小次数位置
    path = user_times.index(min_user_times)
    print("第",path,"位置的登录账号")
    phone = phones[path]
    password = passwords[path]
    min_user_times += 1
    user_times[path] = min_user_times
    print(user_times)
    #清空文件内容
    with open(login_note_path,mode='w',encoding='utf-8') as file:
        file.seek(0)
        file.truncate()  #清空文件内容
        file.close()
    #重新写入文件内容
    file = open(login_note_path,mode='a',encoding='utf-8')
    for index in range(len(phones)):
        line_text = "("+phones[index] +")" + "("+passwords[index] +")" + "("+str(user_times[index]) +")" + "\n"
        print(line_text)
        file.writelines(line_text)
    file.close()
    return phone,password


if __name__ == '__main__':
    #天眼查
    # url = 'https://www.tianyancha.com/login'
    # login(url)

    # 企查查
    # url = 'https://www.qichacha.com/user_login'
    # login_notes = QQMapHelp.readtxt("utils/qichacha_cookie.txt")
    #
    # phone = '15394451742'
    # password = '15394451742.'
    # login_qichacha(url=url, phone=phone, password=password)

    #保存cookie
    # with open(cookie_file, 'wb') as handle:
    #     pickle.dump(data, handle)
    # #打开文件
    # with open(qichacha_cookie_file, 'rb') as handle:
    #     b = pickle.load(handle)
    #     print(b)
    #     cookie_str = ''
    #     for index in b:
    #         cookie_str += index['name'] + '=' + index['value'] + ';'
    #     cookie_str = cookie_str[:-1]
    #     print(cookie_str)
    # from tutorial.utils import file_path
    login_note_path = file_path.login_note_path
    get_login_id(login_note_path)

