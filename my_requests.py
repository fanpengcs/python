#encoding:utf-8

import os
import requests

class MyRequests():
    def get_url(self, rul):
        re = self.request(rul)

def main():
    # re= requests.get("https://www.baidu.com")
    # print(type(re))
    # print(re.status_code)
    # print(type(re.text))
    # print(re.text)
    # print(re.cookies)
    # print(re.content)
    # print(re.content.decode("utf-8"))
    req = MyRequests()
    re = req.get_url("https://www.baidu.com")
    print(type(re))
    print(re.status_code)
    print(type(re.text))
    print(re.text)
    print(re.cookies)
    print(re.content)
    print(re.content.decode("utf-8"))

if ("__main__"==__name__):
    main()