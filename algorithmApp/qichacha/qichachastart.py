import os
import random
import re
import time as sys_time

from urllib.parse import quote
from urllib import request
from bs4 import BeautifulSoup

from utils import AjaxJson
from utils import QQMapHelp
from utils import proxymiddlewares
from algorithmApp.qichacha import qichachalogin
from utils import file_path
from database.service import qichachaLoginServcie

count = 0
un_cookei = []
time_list = [5,6,7]
#使用过期cookie骗过企查查,不要使用已登录的cookie
cookie = "hasShow=1;Hm_lvt_3456bee468c83cc63fb5147f119f1075=1542667824;_uab_collina=154266782384676131679019;Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1542667841;zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201542667823750%2C%22updated%22%3A%201542667840885%2C%22info%22%3A%201542667823753%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%228c791baf2686230abb4959a38bd90a9b%22%7D;zg_did=%7B%22did%22%3A%20%221672e2aea83945-0ee86fc6826a39-16380b2f-75300-1672e2aea84531%22%7D;QCCSESSID=6p5afjj8v1vsf806mkaaejmla7;UM_distinctid=1672e2aeb315f7-0cf489e58c63ad-16380b2f-75300-1672e2aeb32e6f;CNZZDATA1254842228=452614545-1542663594-%7C1542663594;acw_tc=73df0f9715426678213708583ef4a5b87e6ec119d1c50357cb6cdea10b"
qichachaloginfile = file_path.qichachaloginfile

error_url_file = file_path.error_url_file

def get_usable_cookie():
    Cookie = proxymiddlewares.get_that_random_cookie()
    if Cookie in un_cookei:
        Cookie = get_usable_cookie()
    return Cookie

def get_random_time():
    return random.choice(time_list)

"""
 法律诉讼
	   csusong
	   经营状况	
	   crun
	   经营风险
	   cfengxian
	   企业年报
	   creport
	   知识产权
	   cassets
"""


def company_infoget(url,cookie):
    global count
    global article_num
    print("已爬取数据:",count)

    headers={
        'User-Agent': proxymiddlewares.get_random_user_agent(),
        'cookie' : cookie,
        'referer': 'http://www.qichacha.com/',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'accept-encoding': 'json, br',
        'accept': '*/*',
        'Connection': 'keep-alive',
        'x-requested-with': 'XMLHttpRequest',
        'Cache-Control': 'max-age=0',
        'Host': 'www.qichacha.com'
    }
    dataJson = {}
    try:
        count = count + 1
        url_company = url
        url_company.encode("utf-8")
        sys_time.sleep(get_random_time())
        headers['referer'] = url_company
        reponse = request.Request(url=url_company,headers=headers,origin_req_host=proxymiddlewares.get_that_random_ip())
        htmls = request.urlopen(reponse,timeout=30)
        soup= BeautifulSoup(htmls.read(), 'html.parser')
        unique = url.split('_')[1].replace('.html', '')


        gongsimingcheng = soup.select(".content .row  h1")
        if len(gongsimingcheng)==0:
            print('企业名称:无')
            # write_str = '"enterpriseName"' + ':' + '"无",' + '\n'
            # file.write(write_str)
            dataJson["enterpriseName"] = "无"
        else:
            print('企业名称:',gongsimingcheng[0].get_text())
            # write_str = '"enterpriseName"' + ':"' + gongsimingcheng[0].get_text() + '",\n'
            # file.write(write_str)
            qiye_name=gongsimingcheng[0].get_text()
            dataJson["enterpriseName"] = qiye_name

        #判断是否有这个标题
        title_list = []
        cdes_list = soup.select('.content .cdes')
        for item in cdes_list:
            title_list.append(item.get_text())
        cvlu = soup.select(".row .cvlu")

        if title_list.index('电话：') < 0 :
            dianhua = []
        else:
            index = title_list.index('电话：')
            dianhua=cvlu[index].select('span')
        if len(dianhua) == 0 :
            print('企业电话:无')
            # write_str = '"enterprisePhone"' + ':' + '"无",' + '\n'
            # file.write(write_str)
            dataJson["enterprisePhone"] = "无"
        else:
            data1 = dianhua[0].get_text().strip()
            if data1 == None:
                data1 = '无'
            print('企业电话:',data1)
            # 判断电话来看是否登陆
            # if is_login(data1):
            #     count = count - 1
            #     article_num = article_num - 1
            #     login()
            #     raise Exception("登陆失效，重新登陆")
            # write_str = '"enterprisePhone"' + ':"' +data1 + '",\n'
            # file.write(write_str)
            dataJson["enterprisePhone"] = data1

        if title_list.index('官网：') < 0:
            guanwang = []
        else:
            index = title_list.index('官网：')
            guanwang = cvlu[index].select('a')
        if len(guanwang) == 0:
            print('企业官网：无')
            # write_str = '"enterpriseOfficialNetwork"' + ':' + '"无",' + '\n'
            # file.write(write_str)
            dataJson["enterpriseOfficialNetwork"] = "无"
        else:
            data1 = guanwang[0].get('href')
            if data1 == None:
                data1 = '无'
            print('企业官网：',data1)
            # write_str = '"enterpriseOfficialNetwork"' + ':"' + data1 + '",\n'
            # file.write(write_str)
            dataJson["enterpriseOfficialNetwork"] = data1

        if title_list.index('邮箱：') < 0:
            youxiang = []
        else:
            index = title_list.index('邮箱：')
            youxiang = cvlu[index].select('a')
        if len(youxiang) == 0 :
            print('企业邮箱：无')
            # write_str = '"enterpriseEmail"' + ':"' + '无' + '",\n'
            # file.write(write_str)
            dataJson["enterpriseEmail"] =  '无'
        else:
            data=youxiang[0].get('href')
            if data == None:
                data = '无'
            print('企业邮箱：', data)
            # write_str = '"enterpriseEmail"' + ':"' + data + '",\n'
            # file.write(write_str)

            dataJson["enterpriseEmail"] = data

        if title_list.index('地址：') < 0:
            dizhi = []
        else:
            index = title_list.index('地址：')
            dizhi = cvlu[index].select('a')
        if len(dizhi) == 0:
            print('企业地址：无')
            # write_str = '"enterpriseAddress"' + ':' + '"无",' + '\n'
            # file.write(write_str)
            dataJson["enterpriseAddress"] = '无'
        else:
            data1 = dizhi[0].get_text().strip()
            if data1 == None:
                data1 = '无'
            print('企业地址：', data1)
            # write_str = '"enterpriseAddress"' + ':"' + data1 + '",\n'
            # file.write(write_str)
            dataJson["enterpriseAddress"] = data1
            latLng = QQMapHelp.getLatAndLng(data1)
            dataJson['lat'] = latLng['lat']
            dataJson['lng'] = latLng['lng']

        jianjie=soup.select('#textShowMore')
        if len(jianjie) == 0:
            print('企业简介：无')
            # write_str = '"enterpriseIntroduce"' + ':' + '"无",' + '\n'
            # file.write(write_str)
            dataJson["enterpriseIntroduce"] = "无"
        else:
            data1 = jianjie[0].get_text()
            print('企业简介：', data1)
            # write_str = '"enterpriseIntroduce"' + ':"' + data1 + '",\n'
            # file.write(write_str)
            dataJson["enterpriseIntroduce"] = data1

        #百度简介
        url_baidubaike='%s%s' % ('https://baike.baidu.com/item/', quote(qiye_name))
        req_baidubaike = request.Request(url_baidubaike)
        html_data=request.urlopen(req_baidubaike,timeout=30)
        html_baidubaike = BeautifulSoup(html_data.read(), 'html.parser')
        article_baibubaike=html_baidubaike.select('div.lemma-summary > div.para')
        qiyearticle_baibubaike=[]
        if len(article_baibubaike)==0:
            print('企业百度百科简介：无')
            # write_str = '"enterpriseBaiDuIntroduce"' + ':' + '"无",' + '\n'
            # file.write(write_str)
            dataJson["enterpriseBaiDuIntroduce"] = "无"
        else:
            delimiter = ''
            for i in article_baibubaike:
                data1=i.get_text().strip('\n\t\r').strip().split()
                qiyearticle_baibubaike.append(delimiter.join(data1))
            qiyearticle_baibubaike=delimiter.join(qiyearticle_baibubaike)
            print('企业百度百科简介：',qiyearticle_baibubaike)
            # write_str = '"enterpriseBaiDuIntroduce"' + ':"' + qiyearticle_baibubaike + '",\n'
            # file.write(write_str)
            dataJson["enterpriseBaiDuIntroduce"] = qiyearticle_baibubaike


        gsxx=soup.select('#Cominfo table')[1].select('td')
        if len(gsxx) == 0:
            print('企业工商信息：无')
            # write_str = '"enterpriseBusinessInformation"' + ':' + '"无",' + '\n'
            # file.write(write_str)
            dataJson["enterpriseBusinessInformation"] = "无"
        else:
            enterpriseBusinessInformation = {}

            print('注册资本:', gsxx[1].get_text().strip())
            # write_str = '"registeredCapital"' + ':"' + gsxx[1].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["registeredCapital"] = gsxx[1].get_text().strip()

            print('实缴资本:', gsxx[3].get_text().strip())
            # write_str = '"paidCapital"' + ':"' + gsxx[3].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["paidCapital"] = gsxx[3].get_text().strip()

            print('经营状态:', gsxx[5].get_text().strip())
            # write_str = '"operationState"' + ':"' + gsxx[5].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["operationState"] =  gsxx[5].get_text().strip()

            print('成立日期:', gsxx[7].get_text().strip())
            # write_str = '"createTime"' + ':"' + gsxx[7].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["createTime"] = gsxx[7].get_text().strip()

            print('统一社会信用代码:', gsxx[9].get_text().strip())
            # write_str = '"unifiedSocialCreditCode"' + ':"' + gsxx[9].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["unifiedSocialCreditCode"] = gsxx[9].get_text().strip()


            print('纳税人识别号:', gsxx[11].get_text().strip())
            # write_str = '"taxpayerIdentificationNumber"' + ':"' + gsxx[11].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["taxpayerIdentificationNumber"] = gsxx[11].get_text().strip()

            print('注册号:', gsxx[13].get_text().strip())
            # write_str = '"registrationNumber"' + ':"' + gsxx[13].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["registrationNumber"] = gsxx[13].get_text().strip()

            print('组织机构代码:', gsxx[15].get_text().strip())
            # write_str = '"organizationCode"' + ':"' + gsxx[15].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["organizationCode"] = gsxx[15].get_text().strip()

            print('公司类型:', gsxx[17].get_text().strip())
            # write_str = '"companyType"' + ':"' + gsxx[17].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["companyType"] = gsxx[17].get_text().strip()

            print('所属行业:', gsxx[19].get_text().strip())
            # write_str = '"industry"' + ':"' + gsxx[19].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["industry"] = gsxx[19].get_text().strip()


            print('核准日期:', gsxx[21].get_text().strip())
            # write_str = '"dateOfApproval"' + ':"' + gsxx[21].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["dateOfApproval"] = gsxx[21].get_text().strip()

            print('登记机关:', gsxx[23].get_text().strip())
            # write_str = '"registrationAuthority"' + ':"' + gsxx[23].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["registrationAuthority"] = gsxx[23].get_text().strip()

            print('所属地区:', gsxx[25].get_text().strip())
            # write_str = '"affiliatedArea"' + ':"' + gsxx[25].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["affiliatedArea"] = gsxx[25].get_text().strip()

            print('英文名称:', gsxx[27].get_text().strip())
            # write_str = '"englishName"' + ':"' + gsxx[27].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["englishName"] = gsxx[27].get_text().strip()

            print('曾用名:', gsxx[29].get_text().strip())
            # write_str = '"nameUsedBefore"' + ':"' + gsxx[29].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["nameUsedBefore"] = gsxx[29].get_text().strip()

            print('参保人数:', gsxx[31].get_text().strip())
            # write_str = '"insuredNumber"' + ':"' + gsxx[31].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["insuredNumber"] = gsxx[31].get_text().strip()

            print('人员规模:', gsxx[33].get_text().strip())
            # write_str = '"personnelScale"' + ':"' + gsxx[33].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["personnelScale"] = gsxx[33].get_text().strip()

            print('营业期限:', gsxx[35].get_text().strip())
            # write_str = '"timeLimitForBusiness"' + ':"' + gsxx[35].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["timeLimitForBusiness"] = gsxx[35].get_text().strip()

            print('企业地址:', gsxx[37].get_text().strip().split('\n')[0])
            # write_str = '"enterpriseAddress"' + ':"' + gsxx[37].get_text().strip().split('\n')[0] + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["enterpriseAddress"] = gsxx[37].get_text().strip().split('\n')[0]


            print('经营范围:', gsxx[39].get_text().strip())
            # write_str = '"scopeOfOperation"' + ':"' + gsxx[39].get_text().strip() + '",\n'
            # file.write(write_str)
            enterpriseBusinessInformation["scopeOfOperation"] = gsxx[39].get_text().strip()

            dataJson['enterpriseBusinessInformation'] = enterpriseBusinessInformation

        #企业高管信息
        ggxx = soup.select('#Mainmember table tr')
        gg=[]
        if len(ggxx) == 0:
            print('企业高管信息：无')
            # write_str = '"enterpriseExecutivesInformation"' + ':' + '"无",' + '\n'
            # file.write(write_str)
            dataJson["enterpriseExecutivesInformation"] = "无"
        else:
            for i in range(len(ggxx)):
                if i == 0 :
                    continue
                data=ggxx[i].select('td')
                name=data[2].get_text().strip()
                zhiwei=data[1].select('a')[0].get_text().strip()
                xx={'position':name,'executiveName':zhiwei}
                gg.append(xx)
            print('企业高管信息：',gg)
            # write_str = '"enterpriseExecutivesInformation"' + ':"' + AjaxJson.toJsonStrData(gg) + '",\n'
            # file.write(write_str)
            dataJson["enterpriseExecutivesInformation"] = gg

        #企业股东信息
        gdxx= soup.select('#Sockinfo table tr')
        gd = []
        if len(gdxx) == 0:
            print('企业股东信息：无')
            # write_str = '"enterpriseShareholderInformation"' + ':' + '"无",' + '\n'
            # file.write(write_str)
            dataJson["enterpriseShareholderInformation"] = "无"
        else:
            for i in range(len(gdxx)):
                if i == 0:
                    continue
                data=gdxx[i].select('td')
                name=data[1].select('a')[0].get_text().strip().split('\n')[0]
                bili=data[2].get_text().strip()
                jine=data[3].get_text().strip()
                time=data[4].get_text().strip()
                # xx = {'股东': name, '出资比例': bili, '认缴出资': jine, '出资时间': time}
                xx={'shareholder':name,'proportionOfCapital ':bili,'subscribeContribution':jine,'investmentTime':time}
                gd.append(xx)
            print('企业股东信息：', gd)
            # write_str = '"enterpriseShareholderInformation"' + ':"' + AjaxJson.toJsonStrData(gd).replace('"',"'") + '",\n'
            # file.write(write_str)
            dataJson["enterpriseShareholderInformation"] = gd


        tzxx=soup.select('#touzilist > table tr')
        tz=[]
        if len(tzxx) == 0:
            print('企业投资信息：无')
            # write_str = '"enterpriseInvestmentInformation"' + ':' + '"无",' + '\n'
            # file.write(write_str)
            dataJson["enterpriseInvestmentInformation"] = '无'
        else:
            for i in range(len(tzxx)):
                if i == 0:
                    continue
                data=tzxx[i].select('td')
                gsname=data[0].get_text().strip()
                frname=data[1].get_text().strip().split('\n')[0]
                ziben=data[2].get_text().strip()
                zhanbi=data[3].get_text().strip()
                time=data[4].get_text().strip()
                zhuangtai = data[5].get_text().strip()
                # xx = {'被投资公司名称': gsname, '被投资法定代表人': frname, '注册资本': ziben, '投资占比': zhanbi, '注册时间': time,
                #       '状态': zhuangtai}
                xx={'nameOfInvestedCompany':gsname,'legalRepresentativeInvested':frname,'registeredCapital':ziben,'investmentRatio':zhanbi,'registrationTime':time,'status':zhuangtai}
                tz.append(xx)
            print('企业投资信息：',tz)
            # write_str = '"enterpriseInvestmentInformation"' + ':"' + AjaxJson.toJsonStrData(tz).replace('"',"'") + '",\n'
            # file.write(write_str)
            dataJson["enterpriseInvestmentInformation"] = tz

        #诉讼信息
        nav_heads = soup.select('.company-nav-tab .company-nav-head')
        head_names = []
        for nav_head in nav_heads:
            head_names.append(nav_head.select("h2")[0].get_text())
        ss_index = head_names.index("法律诉讼")
        if ss_index > 0:
            susongSoup = nav_heads[ss_index].select("span")
        else:
            susongSoup = []
        if len(susongSoup) > 0:
            #防止有999+的情况
            sifaNum = re.sub("\D", "", susongSoup[0].get_text())
            # sifaNum = soup.select('#susong_title span')[0].get_text()
        else:
            sifaNum = '0'
        if int(sifaNum) > 0:
            sys_time.sleep(get_random_time())
            tab = 'susong'
            #https://www.qichacha.com/company_getinfos?unique=9cce0780ab7644008b73bc2120479d31&companyname=%E5%B0%8F%E7%B1%B3%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E8%B4%A3%E4%BB%BB%E5%85%AC%E5%8F%B8&tab=susong
            url_sfx = 'https://www.qichacha.com/company_getinfos?unique=%s&companyname=%s&tab=susong' % (unique,qiye_name)
            url_sfx = quote(url_sfx, safe=";/?:@&=+$,", encoding="utf-8")
            headers['referer'] = url_sfx
            reponse = request.Request(url=url_sfx, headers=headers, origin_req_host=proxymiddlewares.get_that_random_ip())
            htmls = request.urlopen(reponse, timeout=30).read()
            htmls = str(htmls,encoding="utf-8")
            soup = BeautifulSoup(htmls, 'html.parser')
            #企业司法信息   无 #wenshulist > table
            sffx = soup.select('#wenshulist > table > tr')
        else:
            sffx = []
        sf = []
        if len(sffx) == 0:
            print('企业司法信息：无')
            # write_str = '"enterpriseJudicialInformation' + ':' + '"无",' + '\n'
            # file.write(write_str)
            dataJson["enterpriseJudicialInformation"] = '无'
        else:
            for i in range(len(sffx)):
                if i == 0:
                    continue
                data = sffx[i].select('td')
                time=data[2].get_text().strip()
                caseName=data[1].select('a')[0].get_text().strip()
                caseNum=data[3].get_text().strip()
                caseIndentity= data[4].get_text().strip()
                executePlace=data[5].get_text().strip()
                xx = {'createDate': time, 'caseName': caseName, 'caseNumber': caseNum, 'caseIdentity': caseIndentity, 'courtOfExecution': executePlace}
                sf.append(xx)
            print('企业司法信息：',sf)
            # write_str = '"enterpriseJudicialInformation"' + ':"' + AjaxJson.toJsonStrData(sf).replace('"',"'") + '",\n'
            # file.write(write_str)
            dataJson["enterpriseJudicialInformation"] = sf

        # 产品信息
        ss_index = head_names.index("经营状况")
        if ss_index > 0:
            produceSoup = nav_heads[ss_index].select("span")
        else:
            produceSoup = []
        if len(produceSoup) > 0:
            jinpinNum = re.sub("\D", "", produceSoup[0].get_text())
            # jinpinNum = produceSoup[0].get_text()
        else:
            jinpinNum = '0'
        if int(jinpinNum) > 0 :
            sys_time.sleep(get_random_time())
            tab = 'run'
            url_sfx = 'https://www.qichacha.com/company_getinfos?unique=%s&companyname=%s&tab=run' % (unique,qiye_name)
            url_sfx = quote(url_sfx, safe=";/?:@&=+$,", encoding="utf-8")
            headers['referer'] = url_sfx
            reponse = request.Request(url=url_sfx, headers=headers, origin_req_host=proxymiddlewares.get_that_random_ip())
            htmls = request.urlopen(reponse, timeout=30).read()
            htmls = str(htmls, encoding="utf-8")
            soup = BeautifulSoup(htmls, 'html.parser')
            #企业竞品信息
            jpxx = soup.select('#productlist  table  tr')
        else:
            jpxx = []
        jp = []
        if len(jpxx) == 0:
            print('企业竞品信息：无')
            # write_str = '"enterprisesCompetitiveInformation"' + ':' + '"无",' + '\n'
            # file.write(write_str)
            dataJson["enterprisesCompetitiveInformation"] = '无'
        else:
            for i in range(len(jpxx)):
                if i == 0:
                    continue
                data = jpxx[i].select('td')
                name = data[2].get_text().strip()
                area = data[5].get_text().strip()
                ronzi = data[3].get_text().strip()
                time = data[4].get_text().strip()
                introduce =data[6].get_text().strip()
                xx = {'product': name, 'area': area, 'financingInformation': ronzi, 'createTime':time,'productIntroduce': introduce}
                jp.append(xx)
            print('企业竞品信息：',jp)
            dataJson["enterprisesCompetitiveInformation"] = jp


    except IndexError as e:
        print("无法提取信息的企业有:",url)
        file_error = open(error_url_file,'a',encoding='utf-8')
        file_error.write(url + '\n')
        file_error.close()
        print('找不到企业信息，请查看关键字是否有误！'+ e)
    except Exception as e:
        print("无法提取信息的企业有:", url)
        file_error = open(error_url_file, 'a', encoding='utf-8')
        file_error.write(url + '\n')
        file_error.close()
        print('标签信息有误！')
    #写入文件,也可以返回数据
    jsonStr = AjaxJson.toJsonStrData(dataJson)
    return jsonStr

#是否登陆
def is_login(phone):
    if "*" in phone:
        return True
    return False

def login():
    # 企查查
    url = 'https://www.qichacha.com/user_login'
    # login_note_path = file_path.login_note_path
    # phone, password = qichachalogin.get_login_id(login_note_path)
    login_accounts = qichachaLoginServcie.getLoginAccount()
    if not isinstance(login_accounts,list) and not login_accounts:
        raise Exception("账号次数已用完")
    if len(login_accounts) < 1:
        print("账号还可以使用，不用切换")
        return
    phone = login_accounts[0]["phone"]
    password = login_accounts[0]["pwd"]
    qichachalogin.login_qichacha(url=url,phone=phone,password=password)
    cookie_str = qichachalogin.getCookieStr()
    file = open(qichachaloginfile, 'w', encoding="utf-8")
    file.write(cookie_str)
    file.close()

#获取企业url
def getQiyeUrl(qiyeName,cookie):
    headers = {
        'User-Agent': proxymiddlewares.get_random_user_agent(),
        'cookie': cookie,
        'referer': 'http://www.qichacha.com/',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'accept-encoding': 'json, br',
        'accept': '*/*',
        'Connection': 'keep-alive',
        'x-requested-with': 'XMLHttpRequest',
        'Cache-Control': 'max-age=0',
        'Host': 'www.qichacha.com'
    }
    search_url = "https://www.qichacha.com/search?key=%s" % qiyeName
    #url加编码
    search_url = quote(search_url, safe=";/?:@&=+$,", encoding="utf-8")
    headers['referer'] = search_url
    req = request.Request(url=search_url, headers=headers, origin_req_host=proxymiddlewares.get_that_random_ip())
    response = request.urlopen(req, timeout=30)
    htmls = response.read()
    htmls = str(htmls,encoding="utf-8")
    soup = BeautifulSoup(htmls, 'html.parser')
    tr_list = soup.select("#searchlist .ma_h1")
    #如果没有企业数据
    if len(tr_list) < 1:
        return None
    firm = tr_list[0].get("href")
    company_url = "https://www.qichacha.com%s" % firm
    return company_url

def getCompanyInfoByName(companyName):
    #使用过期cookie
    company_url = getQiyeUrl(companyName, cookie)
    print(company_url)
    #使用已登录cookie
    login()
    cookies = QQMapHelp.readtxt(qichachaloginfile)[0]
    # cookies = "UM_distinctid=166874914cc184-0dacf51440c092-50432518-144000-166874914ce641; zg_did=%7B%22did%22%3A%20%22166874916b2352-0cd5136442ea5c-50432518-144000-166874916b3357%22%7D; _uab_collina=153986800731707481766078; _umdata=ED82BDCEC1AA6EB929ABC678D494A3E7684F3EBEDE804B9CC7D1A9AA607ADD06AA1FC4199CF791E0CD43AD3E795C914C43CABECA53314B10109FB7667078870D; acw_tc=1b9f44dc15425886161346656e70a6377dd2eaf3c92c25c1e13b90278d; QCCSESSID=an0dd30fpc2mgnie8r05eulje4; CNZZDATA1254842228=1413727944-1542776995-https%253A%252F%252Fwww.qichacha.com%252F%7C1542776995; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1542779505; hasShow=1; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201542779505018%2C%22updated%22%3A%201542779837635%2C%22info%22%3A%201542779505020%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22667cb9cf5d4b1089f3389685a7628931%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1542779838"
    data_json = company_infoget(company_url,cookies)
    #增加一次次数
    qichachaLoginServcie.addOneTimes()
    return data_json


#获取企业url列表
def getQiyeUrlList(qiyeName,cookie):
    headers = {
        'User-Agent': proxymiddlewares.get_random_user_agent(),
        'cookie': cookie,
        'referer': 'http://www.qichacha.com/',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'accept-encoding': 'json, br',
        'accept': '*/*',
        'Connection': 'keep-alive',
        'x-requested-with': 'XMLHttpRequest',
        'Cache-Control': 'max-age=0',
        'Host': 'www.qichacha.com'
    }
    search_url = "https://www.qichacha.com/search?key=%s" % qiyeName
    #url加编码
    search_url = quote(search_url, safe=";/?:@&=+$,", encoding="utf-8")
    headers['referer'] = search_url
    req = request.Request(url=search_url, headers=headers, origin_req_host=proxymiddlewares.get_that_random_ip())
    response = request.urlopen(req, timeout=30)
    htmls = response.read()
    htmls = str(htmls,encoding="utf-8")
    print(htmls)
    soup = BeautifulSoup(htmls, 'html.parser')
    tr_list = soup.select(".ma_h1")
    #如果没有企业数据
    if len(tr_list) < 1:
        return None
    data_list = []
    for item in tr_list:
        firm = item.get("href")
        relaCompanyName = item.get_text()
        #firm = /firm_9cce0780ab7644008b73bc2120479d31.html
        # company_url = "https://www.qichacha.com%s" % firm
        union = firm.split('_')[1].replace('.html', '')
        data = {
            "relaCompanyName":relaCompanyName,
            "union":union
        }
        data_list.append(data)
    return data_list


if __name__ == '__main__':
    # url = "https://www.qichacha.com/firm_9cce0780ab7644008b73bc2120479d31.html"
    # jsonStr = company_infoget(url, cookie)
    # print(jsonStr)
    # company_url = getQiyeUrl("小米",cookie)
    # print(company_url)
    data_json = getCompanyInfoByName("小米")
    print(data_json)

