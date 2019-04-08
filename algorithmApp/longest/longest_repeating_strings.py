# coding:utf-8

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

if __name__ == '__main__':
    res = find_longest_repeating_strings('21','213')
    print(type(res))
    print(res)

