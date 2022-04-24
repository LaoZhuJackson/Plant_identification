# 获取access token
# encoding:utf-8
import base64
import os
import tkinter as tk
from os import getcwd
from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilename
from icon_ico import img as icon
from Image01_jpg import img as Image01
# 这个包能让python加载jpg等其它各式图片,否则只能识别gif
from PIL import ImageTk, Image
import requests

host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Q3GkTfvnxF4IhWrymvv6SbGD&client_secret=9iZ2pz3R6E7GZsqtXYSwY2SFzYG3txFX'


# 植物识别

def upload():
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/plant"
    # 二进制打开图片
    if eRoute.get() == '':
        f = open('Image01.jpg', 'rb')
    else:
        f = open(eRoute.get(), 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img}
    access_token = '24.aca8f6441683bf1fe50eeb68c1744fdf.2592000.1653286981.282335-26039125'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    respond = requests.post(request_url, data=params, headers=headers).json()
    length = len(respond['result'])
    print(length)
    # post一个请求，api返回结果
    for i in range(length):
        print(i)
        score = "匹配度：" + str(respond['result'][i]['score'] * 100) + "%"
        name = "名称：" + respond['result'][i]['name']
        result_text_append(score)
        result_text_append(name)
        result_text_append("-------------")


def result_text_append(text):
    lResult.config(text=lResult.cget("text") + "\n" + text)


# def decode_picture(a, b, c):  # a为图片的临时存放路径，b为图片的base64码，c为图片的.扩展名
#     tmp = open(a + c, 'wb+')
#     tmp.write(b)
#     tmp.close()
#
#
def close_windows(path_close):
    ls = os.listdir(path_close)  # 获取该文件夹下所有图片的名称
    for i in ls:
        c_path = os.path.join(path_close, i)  # 把路径和图片的名称进行拼接
        os.remove(c_path)


# 选择路径函数
def selectPath():
    path_ = askopenfilename()  # 使用askopenfilename()方法返回文件的路径
    path.set(path_)
    img_pil = Image.open(eRoute.get())  # 以一个PIL图像对象打开 ，使文件保持打开状态，直到尝试处理数据，才会从文件中读取实际图像数据
    w_img, h_img = img_pil.size
    img_pil_resized = resize(w_img, h_img, w_label, h_label, img_pil)
    i = ImageTk.PhotoImage(img_pil_resized)  # 此时经过上一步处理这里可以识别其他类型的图片了
    lPreview.config(image=i)  # 将图片放入label
    lPreview.image = i  # keep a reference


def resize(w, h, w_box, h_box, pil_image):
    """
    对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例
    :param w:图片宽度
    :param h:图片高度
    :param w_box:label宽度
    :param h_box:label高度
    :param pil_image:需要缩放的图片
    :return:
    """
    f1 = 1.0 * w_box / w
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])  # 取较小的那个作为缩放比例
    width_ = int(w * factor)
    height_ = int(h * factor)
    return pil_image.resize((width_, height_), Image.Resampling.LANCZOS)


# tkinter图形化界面
root_window = Tk()  # 创建主窗口
root_window.title('laozhu植物识别')  # 给窗口起名字

# StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；
# 这个可以跟踪变量值的变化,以保证值的变更随时可以显示在界面上
path = StringVar()
path.set("")  # 取绝对路径
# 定义窗口长宽
global width, height
width = 530
height = 515
# 定义预览label宽高
global w_label, h_label
w_label = 350
h_label = 420

# 实现屏幕居中
screenwidth = root_window.winfo_screenwidth()
screenheight = root_window.winfo_screenheight()
size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root_window.geometry(size_geo)  # 设置窗口大小:宽x高,注,此处不能为 "*",必须使用 "x"

icon_b64 = base64.b64decode(icon)
image01_b64 = base64.b64decode(Image01)
tmp = open('./image/Image01.jpg', 'wb+')      #one.jpg为重新解压为图片后的图片名
tmp.write(image01_b64)
tmp.close()

tmp = open('./image/icon.ico', 'wb+')      #one.jpg为重新解压为图片后的图片名
tmp.write(icon_b64)
tmp.close()
#decode_picture(tem_path, icon_b64, '.ico')
root_window.iconbitmap('./image/icon.ico')  # 更改左上角图标
root_window.config(background='#e5e5e7')  # 设置背景颜色

# 添加标签
# 在最左上角添加文本框
Label(root_window, text="请选择要识别的图片:", bg="#e5e5e7", font=('ArialBold', 10)).grid(row=0, column=0, padx=5,
                                                                                 pady=5)
#decode_picture(tem_path, image01_b64, '.jpg')
img_init = Image.open("./image/Image01.jpg")  # 初始化放入一张图片，让单位转成像素方便后面缩放图片用
i_init = ImageTk.PhotoImage(img_init)
lPreview = Label(root_window, image=i_init, anchor=tk.W, bd=1, relief="ridge", width=w_label,
                 height=h_label)  # 图片预览label
lPreview.grid(row=1, column=0, columnspan=3, padx=5)
lResult = Label(root_window, text="识别结果:", height=35, width=20, anchor=tk.NW, justify='left', bd=1, relief="ridge",
                font=('ArialBold', 10))  # 显示结果标签
lResult.grid(row=0, column=3, rowspan=2, padx=5, pady=5)

# 添加文本框
eRoute = Entry(root_window, textvariable=path, state="readonly")  # 文件路径文本框,初始值为当前文件路径，状态设置为只读
eRoute.grid(row=0, column=1, padx=5, pady=5)

# 添加按钮
Button(root_window, text="选择图片", command=selectPath).grid(row=0, column=2, padx=5, pady=5)  # 选择图片按钮
Button(root_window, text="识别查询", command=upload).grid(row=10, column=0, columnspan=4, padx=5,
                                                      pady=5)  # 在底部添加关闭按钮

root_window.mainloop()  # 开启主循环，让窗口处于显示状态，放在最后
close_windows("./image/")
