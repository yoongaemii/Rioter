#!/usr/bin/env python
# coding: utf-8

# Response Code: https://developer.riotgames.com/response-codes.html 
# Rate Limiting: https://developer.riotgames.com/rate-limiting.html 

# ## App Rate
# app rate에 적용을 받는 리퀘스트만 헤더에 아래 항목이 나타난다  
# Included in any 429 response where the rate limit was enforced by the API infrastructure. Not included in any 429 response where the rate limit was enforced by the underlying service to which the request was proxied.  
# * X-App-Rate-Limit: the number of calls your API key is allowed to make during that bucket and the duration of the bucket in seconds, separated by a colon(예: '20:1, 100:120')
# * X-App-Rate-Limit-Count: the number of request you actually made: bucket limit in seconds  

# 현재 기본 App rate
# 20 requests every 1 seconds
# 100 requests every 2 minutes

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
    404 Error: Match Not Found
    Other Errors: to be handled
    '''
    while True:
        r = requests.get(url)

        if r.status_code == 200: # Successful
            print('Successful')
            json_data = json.loads(r.content.decode("utf-8"))
            return json_data

        elif r.status_code == 429: # rate limit exceeded
            retry = r.headers['Retry-After']
            print('Exceeded Rate Limiting. Will retry After {} seconds'.format(retry))
            time.sleep(int(retry))
            continue # continue the while loop. try from the beginning.

        elif r.status_code == 404: # Match Not Found
            print('No Match Found for '+ url)
            return # return Nonetype object and terminate
        
        else:
            print('Unhandled Error '+ str(r.status_code) + ' : ' + url)
            return # return Nonetype object and terminate


if __name__ == "__main__":
    import config
    api_key = config.api_key

    summoner_name = "야너어어어엌"
    url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{0}?api_key={1}".format(summoner_name, api_key)
    for i in range(200):
        print(i)
        RiotRequest(url)