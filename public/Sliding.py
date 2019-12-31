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
def Sliding():
    d.screenshot("./logs/1.png")
    list_dic =[]
    for i in os.listdir("./pic_m"):
        # 读取目标图片
        target = cv2.imread("./logs/1.png")
        # 读取模板图片
        template = cv2.imread("./pic_m"+"/"+i)
        # 获得模板图片的高宽尺寸
        theight, twidth = template.shape[:2]
        result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        cv2.rectangle(target, min_loc, (min_loc[0] + twidth, min_loc[1] + theight), (0, 0, 225), 2)
        dic_ls={
            "val":min_val,
            "x":((min_loc[0] + twidth) / target.shape[1]),
            "imgae":i
        }
        list_dic.append(dic_ls)
    datasort = sorted(list_dic, key=lambda e: e.__getitem__('val'))  # 排序
    logger.info(datasort)
    logger.info(datasort[0])
    x=datasort[0]["x"]
    d.swipe_points([(0.224, 0.686), (x, 0.686)], 0.05)
    Screen()
    file_path = "./logs/1.1.png"
    image = Image.open(file_path)
    vcode = pytesseract.image_to_string(image, lang="chi_sim")
    if vcode in "拖 动 下 方 滑 块 完 成 拼 图":
        d.click(0.785, 0.745)
        Sliding()



