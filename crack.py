from PIL import Image
import hashlib
import time
import os
import math

# 实现矢量求模和相似度
class VectorCompare:
    # 获取样本大小
    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.items():
            total += count ** 2
        return math.sqrt(total)
    
    # 获取两个样本之间的相似度，以样本特征矢量间的cos值表示
    def relation(self,concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2.keys():
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

# 将图片转化为矢量
def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1

v = VectorCompare()
# 训练集
iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

imageset = []

for letter in iconset:
    for img in os.listdir('./iconset/%s/'%(letter)):
        temp = []
        if img != "Thumbs.db" and img != ".DS_Store": # windows check...
            temp.append(buildvector(Image.open("./iconset/%s/%s"%(letter,img))))
        imageset.append({letter:temp})

# 将图像转化为二维黑白灰度图
im = Image.open("captcha.gif")
im2 = Image.new("P",im.size,255)
im.convert("P")
temp = {}
for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y,x))
        temp[pix] = pix
        if pix == 220 or pix == 227: # 220表示红色，227表示灰色
            im2.putpixel((y,x),0)

# 处理字符的边界，获取到开始列和结束列（纵向切分）
inletter = False
foundletter=False
start = 0
end = 0
letters = []
for y in range(im2.size[0]): # slice across
    for x in range(im2.size[1]): # slice down
        pix = im2.getpixel((y,x))
        if pix != 255:
            inletter = True

    if foundletter == False and inletter == True:
        foundletter = True
        start = y

    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start,end))

    inletter=False

# 识别验证码
count = 0
for letter in letters:
    m = hashlib.md5()
    im3 = im2.crop((letter[0], 0, letter[1],im2.size[1]))

    guess = []

    for image in imageset:
        for x,y in image.items():
            if len(y) != 0:
                guess.append((v.relation(y[0],buildvector(im3)),x))

    guess.sort(reverse=True)
    print("",guess[0])

    count += 1