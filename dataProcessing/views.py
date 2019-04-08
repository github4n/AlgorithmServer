from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.



#分词算法
from django.views.decorators.csrf import csrf_exempt

from utils import AjaxJson,file_path
from algorithmApp.npl import NLP_API
import logging
logger = logging.getLogger('django')

@csrf_exempt
def getFenciWord(request):
    content = request.POST.get("content")
    if content == None or content == "":
        return HttpResponse(AjaxJson.getUnSuccessData("文章不能为空"))
    filePath = file_path.stopwords_file_path
    keyWords = NLP_API.fenci_get(content, filePath)
    logger.info('获取文章分词+participle+完成')
    jsonInfo = AjaxJson.getDumpsAjaxJsonByData(keyWords)
    return HttpResponse(jsonInfo)