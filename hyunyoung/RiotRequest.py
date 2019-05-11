#!/usr/bin/env python
# coding: utf-8

# Rate Limiting: https://developer.riotgames.com/rate-limiting.html 

# ## App Rate
# app rate에 적용을 받는 리퀘스트만 헤더에 아래 항목이 나타난다  
# Included in any 429 response where the rate limit was enforced by the API infrastructure. Not included in any 429 response where the rate limit was enforced by the underlying service to which the request was proxied.  
# * X-App-Rate-Limit: the number of calls your API key is allowed to make during that bucket and the duration of the bucket in seconds, separated by a colon(예: '20:1, 100:120')
# * X-App-Rate-Limit-Count: the number of request you actually made: bucket limit in seconds  
 
# ## Method Rate
# Included in the response for all API calls that enforce a method rate limit
# * X-Method-Rate-Limit
# * X-Method-Rate-Limit-Count  

# 2019.05.08
# 현재는 우선 error가 발생했을 때 retry-after만큼 sleep했다가 다시 시도하는 메소드.
# 아예 api 하나에 해당하는 클래스를 만들어서 각 리퀘스크를 인스턴스로 하고 클래스 변수로 count를 업데이트하는 방향으로 수정 필요
# Dynamic Method에만 적용

import requests
import json
import time

def RiotRequest(url):
    '''
    Make a request handling errors and return python dictionary object
    429 Error: Exceeded Rate Limiting. Retry after sleeping few seconds.
    Other Errors: to be handled
    '''
    while True:
        try: 
            r = requests.get(url)
            print(r.status_code + ' : ' + url)
            json_data = json.loads(r.content.decode("utf-8"))
            return json_data
        except:
            # python에는 switch문이 없나
            if r.status_code == 429: # rate limiting error
                time.sleep(r.headers['Retry-After'])
                print('Exceeded Rate Limiting. Retry After {} seconds'.format(r.headers['Retry-After']))
                continue
            else: # unidentified error
                return # terminate function call 

