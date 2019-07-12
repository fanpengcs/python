import os
import sys
import requests
from bs4 import BeautifulSoup
import bs4
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import pickle
import my_log

class Extract():
    """ 多线程 抓取图片
    pickle 可序列化python原生对象
    ThreadPoolExecutor 线程池
    """
    #全局变量
    rootPwd = os.path.join(os.getcwd(), "Extract")
    save_last = None
    save_last = rootPwd + '\\save_last'

    class SaveItem:
        def __init__(self):
            self.save_num = 0
            self.save_urls = []

    def __init__(self):
        #初始化目录
        self.mkdir(self.rootPwd)
        #初始化日志
        log_path = os.path.join(self.__class__.rootPwd, "log")
        self.mkdir(log_path)
        log_path += '\\extract.log'
        self.log = my_log.Logger(log_path, "debug")
        #初始化线程池
        self.executor = ThreadPoolExecutor(max_workers=20)
        #加载以保存url
        self.save_urls = self.__class__.SaveItem()
        try:
            with open(self.__class__.save_last, 'rb') as save:
                self.save_urls = pickle.load(save)
                save.close()
        except:
            self.log.logger.debug("not find save_last")

    def extract_all(self, url):
        html = self.request(url)
        div_all = BeautifulSoup(html.text, 'lxml').find('div', class_='all')
        if isinstance(div_all, bs4.element.Tag):
            all_a = div_all.find_all('a')
            #去除保存
            do_a = []
            if self.save_urls.save_num == 0:
                do_a = all_a
            else:
                for a_item in all_a:
                    if a_item['href'] in self.save_urls.save_urls:
                        self.log.logger.debug('------已经保存---%s---%s' %(a_item.get_text(), a_item['href']))
                        continue
                    do_a.append(a_item)

            self.tasks = {self.executor.submit(self.all_url, a): a for a in do_a} 
            for future in concurrent.futures.as_completed(self.tasks):
                url = self.tasks[future]
                try:
                    data = future.result()
                except Exception as err:
                    self.log.logger.debug('%r generated an exception: %s' % (url, err))
                else:
                    self.log.logger.debug('%s --- %r--- done:%s' % (data, url, future.done()))


    def all_url(self, a):
        title = a.get_text()
        self.log.logger.debug('------开始保存：%s' %title) 
        path = str(title).replace("?", '_')
        self.mkdir(path)
        href = a['href']
        self.html(href)
        self.save_urls.save_urls.append(a['href'])
        return " ------目录保存完成" + path

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
        img_url = 0
        try:
            img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        except:
            self.log.logger.debug(" %s img_url error!!!" %img_html.text)
        else:
            self.save(img_url)

    def save(self, img_url): ##保存图片
        name = img_url[-9:-4]
        img = self.request(img_url)
        with open(name + '.jpg', 'ab') as f:
            f.write(img.content)
            f.close()
            self.save_urls.save_num+=1
            self.log.logger.debug('------ %s--保存完成 %d 张' %(name, self.save_urls.save_num))

    def mkdir(self, path): ##创建文件夹
        path = path.strip()
        all_path = os.path.join(self.__class__.rootPwd, path)
        isExists = os.path.exists(all_path)
        if not isExists:
            os.makedirs(all_path)
        os.chdir(all_path) ##切换到目录
     
    def request(self, url): ##这个函数获取网页的response 然后返回
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
            'referer': "http://www.mzitu.com/100260/2"
        }
        content = requests.get(url, headers=headers)
        return content
    
def main():
    sys.setrecursionlimit(1000000)  # set the maximum depth as 1000000
    extract = Extract()
    try:
        extract.extract_all('http://www.mzitu.com/all')
    except Exception as err:
        extract.log.logger.debug(err)
    finally:
        with open(extract.save_last, 'wb') as save:
            print(extract.save_urls.save_urls)
            saves = extract.save_urls
            pickle.dump(saves, save)
            save.close()
            extract.log.logger.debug("done save save_last")
        input('Press the enter key to exit.')

if __name__ == "__main__":
    main()