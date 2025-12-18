import base64
with open("fenxi.txt",'r') as f:
    text = f.read()
decodetext =base64.b64decode(text)
with open("fenxi.jpg",'wb')as pic: #图片是二进制数据，需要写的时候加b 
    pic.write(decodetext)

#处理 txt/html/json/代码 -> 用 'w' (Write) 或 'r' (Read)。
#处理 图片/压缩包/exe/音频 -> 必须加 b，用 'wb' (Write Binary) 或 'rb' (Read Binary)。

