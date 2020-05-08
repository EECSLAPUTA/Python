import urllib.request

response = urllib.request.urlopen("http://www.baidu.com")
# print(response)    #返回的是一个object对象
print(response.read().decode('utf-8'))     #对获取到的网页源码进行utf-8解码