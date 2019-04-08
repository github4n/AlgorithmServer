# coding:utf-8
import nltk
import numpy
import jieba
import codecs
import jieba.analyse
from snownlp import SnowNLP
import jieba
import codecs

#分词
def fenci_get(text,filePath):
    fenci_text = jieba.cut(text)
    # 去停用词
    # 这里是有一个文件存放要改的文章，一个文件存放停用表，然后和停用表里的词比较，一样的就删掉，最后把结果存放在一个文件中
    stopwords = {}.fromkeys([line.strip() for line in codecs.open(filePath, 'r', encoding='utf8').readlines()])
    final = ""
    for word in fenci_text:
        if word not in stopwords:
            if (word != "。" and word != "，" and word != "、"):
                final = final + " " + word
    print(final)
    return final

#关键词
def keyword_get(text,number,filePath):
    fenci_text = jieba.cut(text)
    # 去停用词
    # 这里是有一个文件存放要改的文章，一个文件存放停用表，然后和停用表里的词比较，一样的就删掉，最后把结果存放在一个文件中
    stopwords = {}.fromkeys([line.strip() for line in codecs.open(filePath, 'r', encoding='utf8').readlines()])
    final = ""
    for word in fenci_text:
        if word not in stopwords:
            if (word != "。" and word != "，"):
                final = final + " " + word
    # 第三步：提取关键词
    a = jieba.analyse.extract_tags(text, topK=number, withWeight=True, allowPOS=())
    print(a)
    return a

def abstract_get(text,number,filePath):
    dict = summarize(text,number,filePath)
    print('-----------摘 要-------------')
    for sent in dict['top_n_summary']:
        print(sent)
    return dict

#分句
def sent_tokenizer(texts):
    start=0
    i=0#每个字符的位置
    sentences=[]
    punt_list='!?。！？' #',.!?:;~，。！？：；～'.decode('utf8')
    for text in texts:
        if text in punt_list and token not in punt_list: #检查标点符号下一个字符是否还是标点
            sentences.append(texts[start:i+1])#当前标点符号位置
            start=i+1#start标记到下一句的开头
            i+=1
        else:
            i+=1#若不是标点符号，则字符位置继续前移
            token=list(texts[start:i+2]).pop()#取下一个字符
    if start<len(texts):
        sentences.append(texts[start:])#这是为了处理文本末尾没有标点符号的情况
    return sentences

#停用词
def load_stopwordslist(path):
    stoplist=[line.strip() for line in codecs.open(path,'r',encoding='utf8').readlines()]
    stopwrods={}.fromkeys(stoplist)
    return stopwrods

#摘要
def summarize(text,number,filePath):
    N = 100  # 单词数量
    TOP_SENTENCES = number  # 返回的top n句子
    stopwords=load_stopwordslist(filePath)
    sentences=sent_tokenizer(text)
    words=[w for sentence in sentences for w in jieba.cut(sentence) if w not in stopwords if len(w)>1 and w!='\t']
    wordfre=nltk.FreqDist(words)
    topn_words=[w[0] for w in sorted(wordfre.items(),key=lambda d:d[1],reverse=True)][:N]
    scored_sentences=_score_sentences(sentences,topn_words)
    #approach 1,利用均值和标准差过滤非重要句子
    avg=numpy.mean([s[1] for s in scored_sentences])#均值
    std=numpy.std([s[1] for s in scored_sentences])#标准差
    mean_scored=[(sent_idx,score) for (sent_idx,score) in scored_sentences if score>(avg+0.5*std)]
    #approach 2，返回top n句子
    top_n_scored=sorted(scored_sentences,key=lambda s:s[1])[-TOP_SENTENCES:]
    top_n_scored=sorted(top_n_scored,key=lambda s:s[0])
    return dict(top_n_summary=[sentences[idx] for (idx,score) in top_n_scored],mean_scored_summary=[sentences[idx] for (idx,score) in mean_scored])

 #句子得分
def _score_sentences(sentences,topn_words):
    CLUSTER_THRESHOLD = 5  # 单词间的距离
    scores=[]
    sentence_idx=-1
    for s in [list(jieba.cut(s)) for s in sentences]:
        sentence_idx+=1
        word_idx=[]
        for w in topn_words:
            try:
                word_idx.append(s.index(w))#关键词出现在该句子中的索引位置
            except ValueError:#w不在句子中
                pass
        word_idx.sort()
        if len(word_idx)==0:
            continue
        #对于两个连续的单词，利用单词位置索引，通过距离阀值计算族
        clusters=[]
        cluster=[word_idx[0]]
        i=1
        while i<len(word_idx):
            if word_idx[i]-word_idx[i-1]<CLUSTER_THRESHOLD:
                cluster.append(word_idx[i])
            else:
                clusters.append(cluster[:])
                cluster=[word_idx[i]]
            i+=1
        clusters.append(cluster)
        #对每个族打分，每个族类的最大分数是对句子的打分
        max_cluster_score=0
        for c in clusters:
            significant_words_in_cluster=len(c)
            total_words_in_cluster=c[-1]-c[0]+1
            score=1.0*significant_words_in_cluster*significant_words_in_cluster/total_words_in_cluster
            if score>max_cluster_score:
                max_cluster_score=score
        scores.append((sentence_idx,max_cluster_score))
    return scores


if __name__ == '__main__':
    filePath = 'stopwords.txt'
    text = '了子子子字无臂，表示断、绝断，结束绝断'
    num = 10
    fenci_get(text,filePath)
