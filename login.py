import requests
import re

def getContent(url):
　　#使用requests.get获取知乎首页的内容
    r = requests.get(url)
　　#request.get().content是爬到的网页的全部内容
    return r.content

#获取_xsrf标签的值
def getXSRF(url):
　　#获取知乎首页的内容
    content = getContent(url)
　　#正则表达式的匹配模式
    pattern = re.compile('.*?<input type="hidden" name="_xsrf" value="(.*?)"/>.*?')
　　#re.findall查找所有匹配的字符串
    match = re.findall(pattern, content)
    xsrf = match[0]
　　#返回_xsrf的值
    return xsrf

#登录的主方法
def login(baseurl,email,password):
　　#post需要的表单数据，类型为字典
    login_data = {
            '_xsrf': getXSRF(baseurl),
            'password': password,
            'remember_me': 'true',
            'email': email,
    }
　　#设置头信息
    headers_base = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36', 
        'Referer': 'http://www.zhihu.com/',
    }
　　#使用seesion登录，这样的好处是可以在接下来的访问中可以保留登录信息
    session = requests.session()
　　#登录的URL
    baseurl += "/login/email"
　　#requests 的session登录，以post方式，参数分别为url、headers、data
    content = session.post(baseurl, headers = headers_base, data = login_data)
　　#成功登录后输出为 {"r":0,
　　#"msg": "\u767b\u9646\u6210\u529f"
　　#}
    print content.text
　　#再次使用session以get去访问知乎首页，一定要设置verify = False，否则会访问失败
    s = session.get("http://www.zhihu.com", verify = False)
    print s.text.encode('utf-8')
　　#把爬下来的知乎首页写到文本中
    f = open('zhihu.txt', 'w')
    f.write(s.text.encode('utf-8'))

url = "http://www.zhihu.com"
#进行登录，将星号替换成你的知乎登录邮箱和密码即可
login(url,"******@***.com","************")




# import requests
# import sys
# import io
# from selenium import webdriver

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8') #改变标准输出的默认编码

# #建立Phantomjs浏览器对象，括号里是phantomjs.exe在你的电脑上的路径
# browser = webdriver.PhantomJS('d:/tool/07-net/phantomjs-windows/phantomjs-2.1.1-windows/bin/phantomjs.exe')

# #登录页面
# url = r'http://ssfw.xmu.edu.cn/cmstar/index.portal'

# # 访问登录页面
# browser.get(url)

# # 等待一定时间，让js脚本加载完毕
# browser.implicitly_wait(3)

# #输入用户名
# username = browser.find_element_by_name('user')
# username.send_keys('学号')

# #输入密码
# password = browser.find_element_by_name('pwd')
# password.send_keys('密码')

# #选择“学生”单选按钮
# student = browser.find_element_by_xpath('//input[@value="student"]')
# student.click()

# #点击“登录”按钮
# login_button = browser.find_element_by_name('btn')
# login_button.submit()

# #网页截图
# browser.save_screenshot('picture1.png')
# #打印网页源代码
# print(browser.page_source.encode('utf-8').decode())

# browser.quit()