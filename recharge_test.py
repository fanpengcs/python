#encoding:utf-8

import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

def main():
    executor = ThreadPoolExecutor(max_workers=100)
    tasks = {executor.submit(recharge, a): a for a in range(100)} 
    for future in concurrent.futures.as_completed(tasks):
        url = tasks[future]
        try:
            data = future.result()
        except Exception as err:
            print('%r generated an exception: %s' % (url, err))
        else:
            print('%s --- %r--- done:%s' % (data, url, future.done()))

def recharge_callback():
    AccountId = 11040
    ServiceId = 211
    OrderId = 47418009711698
    RechargeId = 100
    Gold = 300
    ExtGold = 0
    probuctId = 100
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url = "http://192.168.132.145:8080/game_recharge/recharge_transparent.php"
    form_data = {
        'account' : '测试充值',
        'amount' : '0.01',
        'black_desc' : '',
        'channel' : '1',
        'currency' : '',
        'extra' : '{0}_{1}_{2}_{3}_{4}_{5}'.format(AccountId, ServiceId, OrderId, RechargeId, Gold, ExtGold),
        'game_id' : '001',
        'is_black' : '0',
        'is_cancel' : '0',
        'is_recovery' : '0',
        'is_test' : '0',
        'memo' : '',
        'openid' : '1-1234',
        'order_id' : '1399633295037630',
        'order_type' : '0',
        'original_purchase_orderid' : '',
        'product_id' : probuctId,
        'time' : '1404975144',
        'transaction_id' : '1000000110081354',
        'version' : '8.0',
        'zone_id' : '1',
        'sign' : 'MT/Wp3jz8l8HV62/OrpXdDIdEF9BGw8zCtwu8VZNaxCi52QXCC7RO2Q5yLRsQy8SmZMk0h0hsxUOXSZ8zZysUL+r/ATVknUs76zveaHROAfqhwo4sBqNA3jvnkCtbV/x9vF46vmNB7tDJcG6UDrJM5a/9Bn3Xq0ctlfSJpqJskr4dqyIlvCbQyi2YtnW2f5aNWATyNUntWtzakXYxZ7mPVT7hhspREo/3v/YcygmUHJJsJ2NnqkyWH7kV3nTTtvTQirjbzgeqnFd+KZBBHuBxOXDZInNLcaTnOQLskRddt0sYJ9/L8aDx9AvZtMe8kgQJhlNq13JOLFbCoMAEHD4Gg==',
    };
    results = requests.post(url, data=form_data, headers=headers).text
    print(results)

def recharge(index):
    accountId = 17120
    buyId = 1
    probuctId = 'HWDPID0006'
    # 添加充值记录
    url = "http://192.168.132.145:8080/game_recharge/recharge_buy.php?accountId={0}&buyId={1}&productId={2}".format(accountId, buyId, probuctId)
    result = requests.get(url)
    res = json.loads(result.text)#(result.json())
    # 充值回调
    if ('0' == res['code']):
        uniqueId = res['info'];
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        url = "http://192.168.132.145:8080/game_recharge/recharge_callback.php"
        form_data = {
            'account' : '测试充值',
            'amount' : '6.05',
            'black_desc' : '',
            'channel' : '1',
            'currency' : '',
            'extra' : '{{"accountId":{0},"uniqueId":{1}}}'.format(accountId, uniqueId),
            'game_id' : 'GMG001',
            'is_black' : '0',
            'is_cancel' : '0',
            'is_recovery' : '0',
            'is_test' : '0',
            'memo' : '',
            'openid' : '1-1234',
            'order_id' : '1399633295037630',
            'order_type' : '0',
            'original_purchase_orderid' : '',
            'product_id' : probuctId,
            'time' : '1404975144',
            'transaction_id' : '1000000110081354',
            'version' : '8.0',
            'zone_id' : '1',
            'sign' : 'MT/Wp3jz8l8HV62/OrpXdDIdEF9BGw8zCtwu8VZNaxCi52QXCC7RO2Q5yLRsQy8SmZMk0h0hsxUOXSZ8zZysUL+r/ATVknUs76zveaHROAfqhwo4sBqNA3jvnkCtbV/x9vF46vmNB7tDJcG6UDrJM5a/9Bn3Xq0ctlfSJpqJskr4dqyIlvCbQyi2YtnW2f5aNWATyNUntWtzakXYxZ7mPVT7hhspREo/3v/YcygmUHJJsJ2NnqkyWH7kV3nTTtvTQirjbzgeqnFd+KZBBHuBxOXDZInNLcaTnOQLskRddt0sYJ9/L8aDx9AvZtMe8kgQJhlNq13JOLFbCoMAEHD4Gg==',
        };
        results = requests.post(url, data=form_data, headers=headers).text
        print(results)
    else:
        print(res)

if __name__ == "__main__":
    #main()
    recharge_callback()