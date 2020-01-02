import cv2,os
import pytesseract
from PIL import Image
import numpy as np
import uiautomator2  as u2
from framework.logger import Logger

logger = Logger(logger="Sliding").getlog()
d = u2.connect()
def Screen():
    file_path = './logs/1.png'
    sv_path = './logs/1.1.png'
    img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    sp=(img.shape)
    y0=int(760-(2160-sp[0])/2)
    y1=int(840-(2160-sp[0])/2)
    x0=int(40-(1080-sp[1])/2)
    x1=int(1030-(1080-sp[1])/2)
    cropped = img[y0:y1, x0:x1] # 裁剪坐标为[y0:y1, x0:x1]
    cv2.imencode('.png',  cropped)[1].tofile(sv_path)  # #路径不能为中文解决方法
def origin(imgae):
    d.screenshot("./logs/1.png")
    # 读取目标图片
    target = cv2.imread("./logs/1.png")
    # 读取模板图片
    template = cv2.imread("./tool/"+imgae)
    result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    # 对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法min_val越趋近与0匹配度越好，匹配位置取min_loc
    # 对于其他方法max_val越趋近于1匹配度越好，匹配位置取max_loc

    x1 = ((min_loc[0]) / target.shape[1])
    y1 = ((min_loc[1]) / target.shape[0])
    return (x1,y1)

def Sliding():
    d.screenshot("./logs/1.png")
    list_dic =[]
    # 读取目标图片
    target = cv2.imread("./logs/1.png")
    sp = (target.shape)
    for i in os.listdir("./pic_m"):

        # 读取模板图片
        template = cv2.imread("./pic_m"+"/"+i)
        # 获得模板图片的高宽尺寸
        theight, twidth = template.shape[:2]
        result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        # 对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法min_val越趋近与0匹配度越好，匹配位置取min_loc
        # 对于其他方法max_val越趋近于1匹配度越好，匹配位置取max_loc
        dic_ls={
            "val":min_val,
            "x":((min_loc[0] ) / target.shape[1]),
            "imgae":i,
        }
        list_dic.append(dic_ls)
    datasort = sorted(list_dic, key=lambda e: e.__getitem__('val'))  #

    i = 0
    while (datasort[i]["x"] > 0.45):
        logger.info(datasort[i])
        x=datasort[i]["x"]
        logger.info("起点"+str(origin("hdan.png")))
        logger.info('目标点(%s,%s)'%(x, origin('hdan.png')[1]))
        d.swipe_points([origin('hdan.png'), (x, origin('hdan.png')[1])], 0.05)

        Screen()
        file_path = "./logs/1.1.png"
        image = Image.open(file_path)
        vcode = pytesseract.image_to_string(image, lang="chi_sim")
        logger.info(vcode)

        if "拖 动 下 方 滑 块 完 成 拼 图"in vcode:
            x = int(869.4 - (1080 - sp[1]) / 2)/sp[1]
            y = int(1511.04 - (1920 - sp[0]) / 2)/sp[0]
            logger.info("刷新"+str((x,y)))
            d.click(x,y)
            Sliding()

        i = i + 1
        if i > len(datasort)-1:  # 当i大于10时跳出循环
            break






