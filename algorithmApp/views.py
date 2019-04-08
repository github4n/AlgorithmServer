
from django.http import HttpResponse
# Create your views here.


#分词算法
#post请求
from django.views.decorators.csrf import csrf_exempt

from utils import AjaxJson,file_path
from .npl import NLP_API
from .similar import main
from .qichacha import qichachastart
from .finddownurl import download as downloadUtil
from .correct import Correct
from .language_identification import language_identification
from .polarity_en import polarity_en
from .auto_select import autoselect
from .longest import longest_repeating_strings
import simplejson
import logging
logger = logging.getLogger('django')

#分词算法
@csrf_exempt
def participle(request):
    content = request.POST.get("content")
    if content == None or content == "":
        return HttpResponse(AjaxJson.getUnSuccessData("文章不能为空"))
    filePath = file_path.stopwords_file_path
    keyWords = NLP_API.fenci_get(content, filePath)
    logger.info('获取文章分词+participle+完成')
    jsonInfo = AjaxJson.getDumpsAjaxJsonByData(keyWords)
    return HttpResponse(jsonInfo)

#相似度算法
@csrf_exempt
def similar(request):
    content = request.POST.get("content")
    if content == None or content == "":
        logger.info("数据不能为空")
        return HttpResponse(AjaxJson.getUnSuccessData("数据不能为空"))
    data_list = simplejson.loads(content,encoding='utf-8')
    if len(data_list) < 1:
        return HttpResponse(AjaxJson.getUnSuccessData("数据不能为空"))
    result = main.similar(data_list=data_list)
    logger.info('数据similar加工完成')
    jsonInfo = AjaxJson.getDumpsAjaxJsonByData(result)
    return HttpResponse(jsonInfo)

#获取企业信息
@csrf_exempt
def getCompany(request):
    content = request.POST.get("content")
    if content == None or content == "":
        logger.info("数据不能为空")
        return HttpResponse(AjaxJson.getUnSuccessData("数据不能为空"))
    result = qichachastart.getCompanyInfoByName(content)
    jsonInfo = AjaxJson.getDumpsAjaxJsonByData(result)
    return HttpResponse(jsonInfo)

#解析下载文件正则
@csrf_exempt
def findDownLoadUrl(request):
    content = request.POST.get("content")
    if content == None or content == "":
        logger.info("数据不能为空")
        return HttpResponse(AjaxJson.getUnSuccessData("数据不能为空"))
    data_json = simplejson.loads(content, encoding='utf-8')
    result = {}
    jsonInfo = AjaxJson.getDumpsAjaxJsonByData(result)
    return HttpResponse(jsonInfo)

#下载
@csrf_exempt
def download(request):
    # content = request.POST.get("content")
    if not request.body:
        logger.info("数据不能为空")
        return HttpResponse(AjaxJson.getUnSuccessData("数据不能为空"))
    body = str(request.body,encoding="utf-8")
    data_json = AjaxJson.loadsJsonByStrData(body)
    down_load_path = file_path.down_load_file
    result = downloadUtil.geturllist(contents=data_json["content"], url_in=data_json["url"],suffix_path=down_load_path)
    jsonInfo = AjaxJson.getDumpsAjaxJsonByData(result)
    return HttpResponse(jsonInfo)

#自动校正框选区域
@csrf_exempt
def correctArea(request):
    if not request.body:
        logger.info("数据不能为空")
        return HttpResponse(AjaxJson.getUnSuccessData("数据不能为空"))
    body = str(request.body,encoding="utf-8")
    data_json = AjaxJson.loadsJsonByStrData(body)
    point = data_json["point"]
    url = data_json["url"]
    result = Correct.return_area(url,point)
    jsonInfo = AjaxJson.getDumpsAjaxJsonByData(result)
    return HttpResponse(jsonInfo)

#英文情感判别
@csrf_exempt
def polarityEn(request):
    if not request.body:
        logger.info("数据不能为空")
        return HttpResponse(AjaxJson.getUnSuccessData("数据不能为空"))
    body = str(request.body,encoding="utf-8")
    data_json = AjaxJson.loadsJsonByStrData(body)
    st = data_json["st"]
    if language_identification.language_identification(st)=='en':
        result = polarity_en.polarity_en(st)
        data={'polarity_en':result}
        jsonInfo = AjaxJson.getDumpsAjaxJsonByData(data)
        return HttpResponse(jsonInfo)

#自动框选主体内容
@csrf_exempt
def autoSelect(request):
    if not request.body:
        logger.info("数据不能为空")
        return HttpResponse(AjaxJson.getUnSuccessData("数据不能为空"))
    body = str(request.body,encoding="utf-8")
    data_json = AjaxJson.loadsJsonByStrData(body)
    html = data_json["html"]
    result = autoselect.Auto_select(html)
    jsonInfo = AjaxJson.getDumpsAjaxJsonByData(result)
    return HttpResponse(jsonInfo)

#找到最长的重复字符串
@csrf_exempt
def findLongest(request):
    if not request.body:
        logger.info("数据不能为空")
        return HttpResponse(AjaxJson.getUnSuccessData("数据不能为空"))
    body = str(request.body,encoding="utf-8")
    data_json = AjaxJson.loadsJsonByStrData(body)
    string1 = data_json["string1"]
    string2 = data_json["string2"]
    if not string1 or not string2:
        logger.info("string1或者string2不能为空")
        return HttpResponse(AjaxJson.getUnSuccessData("string1或者string2不能为空"))
    result = longest_repeating_strings.find_longest_repeating_strings(string1,string2)
    jsonInfo = AjaxJson.getDumpsAjaxJsonByData(result)
    return HttpResponse(jsonInfo)

#测试
def index(request):
    # print(request)
    return HttpResponse("Hello, world. You're at the polls index.")