    
import requests
from bs4 import BeautifulSoup
import os
import bs4
#导入所需要的模块
class mzitu():
    """ 抓取图片 """
    rootPwd = os.getcwd()
    rootPwd = os.path.join(rootPwd, "mzitu")

    def print(self, log):
        log_path = os.path.join(self.__class__.rootPwd, "log")
        isExists = os.path.exists(log_path)
        if not isExists:
            os.makedirs(log_path)
        f = open(log_path + '\\mzitu.log', 'at')
        f.write(log)
        f.write("\n")
        f.close()
        print(log)

    def all_url(self, url):
        html = self.request(url)
        div_all = BeautifulSoup(html.text, 'lxml').find('div', class_='all')
        if isinstance(div_all, bs4.element.Tag):
            all_a = div_all.find_all('a')
            for a in all_a:
                title = a.get_text()
                self.print('------开始保存：%s' %title) 
                path = str(title).replace("?", '_') ##替换掉带有的？
                self.mkdir(path) ##调用mkdir函数创建文件夹！这儿path代表的是标题title
                href = a['href']
                self.html(href) 

    def html(self, href):   ##获得图片的页面地址
        html = self.request(href)
        pagenavi = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi')
        if isinstance(pagenavi, bs4.element.Tag):
            max_span = pagenavi.find_all('span')[-2].get_text()
            for page in range(1, int(max_span) + 1):
                page_url = href + '/' + str(page)
                self.img(page_url) ##调用img函数

    def img(self, page_url): ##处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        try:
            img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        except:
            self.print("img_url error!!!")
        self.save(img_url)

    def save(self, img_url): ##保存图片
        name = img_url[-9:-4]
        img = self.request(img_url)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self, path): ##创建文件夹
        path = path.strip()
        all_path = os.path.join(self.__class__.rootPwd, path)
        isExists = os.path.exists(all_path)
        if not isExists:
            os.makedirs(all_path)
            os.chdir(all_path) ##切换到目录
            self.print('建了一个名字叫做 %s 的文件夹！' %all_path)
        else:
            self.print('%s文件夹已经存在了！' %all_path)
            self.mkdir("{0}_1".format(path))

    def request(self, url): ##这个函数获取网页的response 然后返回
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
            'referer': "http://www.mzitu.com/100260/2"
        }
        content = requests.get(url, headers=headers)
        return content
    
#设置启动函数
def main():
    Mzitu = mzitu() ##实例化
    Mzitu.all_url('http://www.mzitu.com/all') ##给函数all_url传入参数
    input('Press the enter key to exit.')

if __name__ == "__main__":
    main()