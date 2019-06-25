#!/usr/bin/env python
# coding: utf-8

# ## App Rate
# app rate에 적용을 받는 리퀘스트만 헤더에 아래 항목이 나타난다  
# Included in any 429 response where the rate limit was enforced by the API infrastructure. Not included in any 429 response where the rate limit was enforced by the underlying service to which the request was proxied.  
# * X-App-Rate-Limit: the number of calls your API key is allowed to make during that bucket and the duration of the bucket in seconds, separated by a colon(예: '20:1, 100:120')
# * X-App-Rate-Limit-Count: the number of request you actually made: bucket limit in seconds  
# 
# ## Method Rate
# Included in the response for all API calls that enforce a method rate limit
# * X-Method-Rate-Limit
# * X-Method-Rate-Limit-Count  
# 
# 현재는 우선 error가 발생했을 때 retry-after만큼 sleep했다가 다시 시도하는 메소드

# In[2]:


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
            # print('Successful')
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

