#encoding:utf-8

import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

#headers = {"Content-Type": 'application/json'}
headers = {"Content-Type": 'application/x-www-form-urlencoded'}
#url = 'http://10.10.10.248:5000/gmcommand'
url = 'http://10.0.150.189:5000/gmcommand'

def main():
        try:
            forbidden()
        except Exception as err:
            print('%r generated an exception: %s' % (url, err))
        else:
            print("success")

'''
Opt:
forbidden:封号
nospeak:禁言
mail:指定角色邮件
mailall:全服邮件
itemchange:道具修改
wordnotice:公告(暂无)
accpermission:权限修改（暂无）
'''
def forbidden():
    form_data = {
        'data_packet' : '''{
            "head":{
                "opt":"forbidden"
                },
            "body":{
                "uid":["mine_1","mine_2"],
                "gid":[2001,2002],
                "sec":60,
                "theme":"标题",
                "msg":"message",
                "prop":[{"type":1,"propId":2,"propCount":1000},{"type":1,"propId":3,"propCount":2000}],
                "serverId":1,
                "level":10,
                "endTime":"2020-05-19 23:00:00"
                }
            }'''
        }
    #results = requests.post(url, data=json.dumps(form_data), headers=headers).text
    results = requests.post(url, data=form_data, headers=headers).text
    print(results)

if __name__ == "__main__":
    main()