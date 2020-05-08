from bs4 import BeautifulSoup           #网页解析，获取数据
import re                               #正则表达式
import urllib.request, urllib.error     #指定URL，获取网页数据
import xlwt                             #excel操作

def main():
    print("开始爬取...")
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    savepath = ".\\豆瓣电影TOP250.xls"
    saveData(datalist,savepath)  

findLink = re.compile(r'<a href="(.*?)">')    #影片详情链接的规则
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)    #影片图片  re.S让换行符包含在字符中
findTitle = re.compile(r'<span class="title">(.*)</span>')    #影片详情链接的规则
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')    #影片评分
findJudge = re.compile(r'<span>(\d*)人评价</span>')    #影片评价人数
findInq = re.compile(r'<span class="inq">(.*)</span>')    #影片概况
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)    #影片相关内容

#获得网页源码
def askURL(url):
    head = {     #模拟浏览器头部信息，进行伪装
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363"
   }
    request = urllib.request.Request(url,headers=head)
    #html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):  #判断e对象里是否包含code这个属性
            print(e.code)      #错误代码，如果识别是爬虫，就是418
        if hasattr(e,"reason"):
            print(e.reason)
    return html


#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):
        url = baseurl + str(i*25)   #调用10次获取10页的信息
        html = askURL(url)          #保存获取到的网页源码
        #逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            data = []   #保存一部电影的所有信息
            item = str(item)   #将对象转化为字符串，方便用正则表达式进行匹配
            #影片中文名,影片外文名
            titles = re.findall(findTitle,item)   #片名可能有中文名，外文名，其他国家名字。我们只保存中文英文
            if len(titles) >= 2:
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/","")     #去掉斜杠符号
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')              #留空
            #评分
            rating = re.findall(findRating,item)[0]
            data.append(rating)
            #评分人数
            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)
            #概况
            inq = re.findall(findInq,item)   #inq可能不只有一个
            if len(inq) != 0:
                inq = inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(' ')
            #影片中文链接
            link = re.findall(findLink,item)[0]
            data.append(link)
            #图片链接
            imgsrc = re.findall(findImgSrc,item)[0]
            data.append(imgsrc)
            #相关信息
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?',' ',bd)   #替换<br>
            bd = re.sub('/',' ',bd)        #替换/
            data.append(bd.strip())    #去掉前后的空格 
            datalist.append(data)   #处理好的一部电影信息放入datalist
    return datalist

#保存数据
def saveData(datalist,savepath):
    print("正在保存...")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)    #创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)   #创建工作表
    col = ("影片中文名","影片外文名","评分","评分人数","概况","影片中文链接","图片链接","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])  #写列名
    for i in range(0,250):
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save(savepath)


if __name__ == "__main__":
    main()
    print("爬取完毕")
