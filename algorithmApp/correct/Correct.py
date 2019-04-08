import joblib
from utils import file_path
import os

def return_area(url,point):
    area=[]
    if 'www.cnits.net.cn' in url:
        url = url.replace('http://', '').replace('https://', '').replace('.', '').replace('/', '')
        name=url+'_train.m'
        filename=os.path.join(file_path.setting_dir_path,name)
        clf = joblib.load(filename)
        res = clf.predict([point])
        if res == 1:
            area = [296, 311, 368, 344]
        elif res == 2:
            area = [0, 656, 287, 278]
        elif res == 3:
            area = [293, 667, 373, 129]
        elif res == 4:
            area = [296, 806, 369, 130]
        elif res == 5:
            area = [676, 654, 283, 239]
        elif res == 6:
            area = [284,1148,382,372]
        elif res == 7:
            area = [0,1635,280,245]
        elif res == 8:
            area = [285,1638,370,236]
        elif res == 9:
            area = [677,1636,305,242]
        elif res == 10:
            area = [284,1929,393,425]
        elif res == 11:
            area = [0,2544,284,242]
        elif res == 12:
            area = [287, 2539, 375, 248]
        elif res == 13:
            area = [676, 2539, 305, 249]
        elif res == 14:
            area = [0,2884,282,230]
        elif res == 15:
            area = [287,2885,376,232]
        elif res == 16:
            area = [677,2881,303,233]



    elif 'www.its.china.org' in url:
        url = url.replace('http://', '').replace('https://', '').replace('.', '').replace('/', '')
        name = url + '_train.m'
        filename = os.path.join(file_path.setting_dir_path, name)
        clf = joblib.load(filename)
        res = clf.predict([point])
        if res == 1:
            area = [673,259,424,229]
        elif res == 2:
            area = [193,659,554,274]
        elif res == 3:
            area = [29,1142,509,212]
        elif res == 4:
            area = [582,1143,511,213]
        elif res == 5:
            area = [27,1575,243,220]
        elif res == 6:
            area = [308,1575,498,221]
        elif res == 7:
            area = [852,1574,229,223]
        elif res == 8:
            area = [378,1852,698,223]


    else:
        area = [0,0,0,0]

    return area

if __name__ == "__main__":
    url='www.its.china.org'
    point=[378,1852,698,223]
    area=return_area(url,point)
    print(area)

