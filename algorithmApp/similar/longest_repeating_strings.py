# encoding=utf8

def find_longest_repeating_strings(string1,string2):
    len1=len(string1)
    len2=len(string2)
    if len1>=len2:
        str1=string2
        str2=string1
    else:
        str1=string1
        str2=string2
    longest_num=[0]
    for i in range(len(str1)):
        for j in range(i+1,len(str1)+1):
            try:
                if str1[i:j] in str2:
                    longest_num.append(j-i)
            except:
                pass
    res= float(max(longest_num))/len(str1)
    # print(max(longest_num),len(str1),res)
    return res

def sum(num1,num2):
    sum_num = num1 + num2
    return sum_num




if __name__ == '__main__':
    s1='国网信息通信产业集团有限公司2018年第九批集中采购项目公开竞争性谈判（物资）'
    s2='[福建亿力电力科技有限责任公司]国网信息通信产业集团有限公司2018年第九批集中采购项目公开竞争性谈判...'
    res = find_longest_repeating_strings(s1,s2)
    print(res)