import os

from AlgorithmServer import settings

#文件路径统一管理
qichachaloginfile = os.path.join(settings.BASE_DIR,'utils/files/qichacha/qichacha_cookie.txt')

error_url_file = os.path.join(settings.BASE_DIR,"utils/files/utils/error_url.txt")

login_note_path = os.path.join(settings.BASE_DIR,"utils/files/qichacha/login_note.txt")

stopwords_file_path = os.path.join(settings.BASE_DIR,"utils/files/npl/stopwords.txt")

random_ip_file_path = os.path.join(settings.BASE_DIR,"utils/files/utils/label_ip.txt")


qichacha_drive_cookie_path = os.path.join(settings.BASE_DIR,"utils/files/qichacha/qichacha_drive_cookie.txt")


not_user_file = os.path.join(settings.BASE_DIR,"utils/files/utils/notuser.txt")

doc_type_file = os.path.join(settings.BASE_DIR,"utils/files/utils/filetype.txt")

#下载文件路径
down_load_file = os.path.join(settings.BASE_DIR,"utils/files/download/file_suffix.txt")
#噪声去除
noise_ad_file = os.path.join(settings.BASE_DIR,"utils/files/utils/removeAd.txt")

correct_testdata_file = os.path.join(settings.BASE_DIR,"utils/files/correct/testdata.data")

correct_train_model_file = os.path.join(settings.BASE_DIR,"utils/files/correct/train_model.m")

setting_dir_path = os.path.join(settings.BASE_DIR,"utils/files/correct/")