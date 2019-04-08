
from . import longest_repeating_strings

"""
[
{
"content1":"",
"content2":"",
"id":""
}
]

"""

def similar(data_list):
    result = []
    for item in data_list:
        data = {}
        data["id"] = item["id"]
        gailv = longest_repeating_strings.find_longest_repeating_strings(string1=item["content1"],string2=item["content2"])
        data["gailv"] = gailv
        # print(data)
        result.append(data)
    print(result)
    return result