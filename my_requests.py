#encoding:utf-8

import os
import requests

class MyRequests():
    def get_url(self, url, headers):
        re = self.request(url, headers)
        return re
    
    def request(self, url, headers):
        re = requests.get(url, headers=headers)
        return re

def main():
    url = "https://www.baidu.com"
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN',
        'Connection': 'Keep-Alive',
        'Cookie': 'BD_CK_SAM=1; BD_HOME=1; BD_UPN=1d314753; ispeed_lsm=2; delPer=0; H_PS_645EC=d5bbSBejmXxPM1%2BsCmVEyoFLm39JwsP3AbAlAoSW0b0%2BplUfviS57%2FLdlE4b6KwhNKa176%2BUEcGq; H_PS_PSSID=; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=5; BDRCVFR[4r8LXJfwh-6]=I67x6TjHwwYf0; BAIDUID=79468E69F21EBFAC3378FA10DD014840:FG=1; BIDUPSID=79468E69F21EBFAC3378FA10DD014840; PSTM=1529030279; MCITY=-%3A; BDUSS=DRWYnNvNHh2ZnJJdEdFT1BQTndGa3pnYUF4ZUhoLUwwaUVYZU5JNlJvcHZERlJiQVFBQUFBJCQAAAAAAAAAAAEAAACZ9sEfcGVuZ2ZhbjEyMzc4MwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG9~LFtvfyxbd; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598',
        'Host': 'www.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
    }
    req = MyRequests()
    re = req.get_url(url, headers=headers)
    print("retype:%s\n" %(type(re)))
    print("status_code:%s\n" %(re.status_code))
    print("texttype:%s\n" %(type(re.text)))
    print("text:%s\n" %(re.text))
    print("cookies:%s\n" %(re.cookies))
    print("content:%s\n" %(re.content))
    print("decode:%s\n" %(re.content.decode("utf-8")))

if ("__main__"==__name__):
    main()