import base64


def transform(picture_name):
    # 将图片转换问base64码
    open_pic = open("%s" % picture_name, 'rb')
    b64str = base64.b64encode(open_pic.read())
    open_pic.close()
    # 注意这边b64str一定要加上.decode()
    write_data = 'img = "%s"' % b64str.decode()
    f = open('%s.py' % picture_name.replace('.', '_'), 'w+')
    f.write(write_data)
    f.close()


if __name__ == '__main__':
    pics = ["icon.ico", "Image01.jpg"]  # 这是2张用到的图片
    for i in pics:
        transform(i)
    print("ok")
