#!/usr/bin/env python
# coding: utf-8

##### Riot API Call Functions
# Documentation: https://developer.riotgames.com/api-methods/

##### Dynamic Data

import config
import requests
import json
from pprint import pprint
from RiotRequest import RiotRequest

api_key = config.api_key
# game_id = 3309773060


def get_account_id(summoner_name):
    '''
    input: 접근할 수 있는 summoner name
    output: account_id
    '''
    json_data = RiotRequest("https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{0}?api_key={1}".format(summoner_name, api_key))
    return json_data['accountId']


def get_account_id_by_summonerId(summonerId):
    '''
    input: Encrypted summoner id
    output: account_id
    '''
    json_data = RiotRequest("https://kr.api.riotgames.com/lol/summoner/v4/summoners/{0}?api_key={1}".format(summonerId, api_key))
    return json_data['accountId']

def get_entry(queue, tier, division):
    '''
    tiers = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND']
    divisions = ['I', 'II', 'III', 'IV']
    queue = ['RANKED_SOLO_5x5', 'RANKED_FLEX_SR', 'RANKED_FLEX_TT']
    API doc: https://developer.riotgames.com/api-methods/#league-v4/GET_getLeagueEntries 
    '''
    json_data = RiotRequest("https://kr.api.riotgames.com/lol/league/v4/entries/{0}/{1}/{2}?api_key={3}".format(queue, tier, division, api_key))
    summoners = [usr['summonerId'] for usr in json_data]
    return summoners

def get_match_ids(account_id):
    '''
    matches라는 key 안에 최대 최근 100개의 match id만
    API doc: https://developer.riotgames.com/api-methods/#match-v4/GET_getMatchlist
    '''
    json_data = RiotRequest("https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{0}?api_key={1}".format(account_id, api_key))
    game_id_list = [match['gameId'] for match in json_data['matches']]
    return game_id_list

def get_match_history(account_id):
    '''
    account_id: str. accound id of the user
    output: List[MatchReferenceDto]
    MatchReferenceDto: {'platformId', 'gameId', 'champion', 'queue', 'season', 'timestamp', 'role', 'lane'}
    API doc: https://developer.riotgames.com/api-methods/#match-v4/GET_getMatchlist
    '''   
    # initialize
    beginIndex = 0
    matchList = []

    # make multiple requests to get all matches
    while True: 
        url = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{0}?api_key={1}&beginIndex={2}".format(account_id, api_key, beginIndex)
        json_data = RiotRequest(url)
        
        # save match data into list
        matchList.extend(json_data['matches'])

        if json_data['endIndex'] >= json_data['totalGames']: # if endIndex reaches the number of total games
            break # terminate the while loop
        else: # make a request on previous 100 matches
            beginIndex += 100
    
    return matchList

def get_this_season_match_history(account_id):
    # beginTime/endTime of each season: https://rankedboost.com/season-end-league-of-legends/
    '''
    account_id: str. accound id of the user
    output: List[MatchReferenceDto]
    MatchReferenceDto: {'platformId', 'gameId', 'champion', 'queue', 'season', 'timestamp', 'role', 'lane'}
    API doc: https://developer.riotgames.com/api-methods/#match-v4/GET_getMatchlist
    '''   
    # initialize
    beginIndex = 0
    matchList = []

    # make multiple requests to get all matches
    while True: 
        url = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{0}?api_key={1}&beginIndex={2}".format(account_id, api_key, beginIndex)
        json_data = RiotRequest(url)
        
        # save match data into list
        

        if json_data['matches'][-1]['season'] != 13: # if season goes beyond 13
            # Additional Filtering - extend only matches in season 13
            matchList.extend([match for match in json_data['matches'] if match['season'] == 13]) 
            break # terminate the while loop
        else:
            matchList.extend(json_data['matches'])

        if json_data['endIndex'] >= json_data['totalGames']: # if endIndex reaches the number of total games
            break # terminate the while loop
        else: # make a request on previous 100 matches
            beginIndex += 100
    
    return matchList

def get_game_detail(game_id):
    json_data = RiotRequest("https://kr.api.riotgames.com/lol/match/v4/matches/{0}?api_key={1}".format(game_id, api_key))
    return json_data

def get_match_timeline(game_id):
    '''
    1분 단위로 나뉘어진 프레임의 리스트를 반환
    List[{'timestamp': int, 'participantFrames': Map[String, MatchParticipantFrameDto], 'events': List[MatchEventDto]}]
    '''
    json_data = RiotRequest("https://kr.api.riotgames.com/lol/match/v4/timelines/by-match/{0}?api_key={1}".format(game_id, api_key))
    return json_data['frames']



###### Static Data
# static data documnetation: https://developer.riotgames.com/static-data.html#languages   

# cf) dictionary를 리스트로 바꾸기  
# dictionary에 .values() 적용하면 'dict_values'라는 형태의 자료형 반환. 이를 실제 리스트처럼 접근하기 위해서는 list(dict.values())로 명시적인 형변환 해줘야


def get_champion_json():
    '''
    champion id(string)를 key로, champion name(string)을 value로 갖는 dictionary 반환
    '''
    
    json_data = RiotRequest("http://ddragon.leagueoflegends.com/cdn/9.8.1/data/ko_KR/champion.json")
    
    champions_info = list(json_data.values())[3]
    champions_list = list(champions_info.values())
    champion_dict={}
    for champion in champions_list:
        champion_dict[champion['key']] = champion['id']
    
    return champion_dict

def get_item_json(): 
    '''
    key: 아이템번호
    value: 'name', 'description', 'colloq', 'plaintext', 'into', 'image', 'gold', 'tags', 'maps', 'stats'를 key로 하는 dictionary
    'map': {'1': False,'8': True, '10': True, ... } 이런 식으로 각 맵에서 지원이 되는지 여부
    '''
    api_data = requests.get("http://ddragon.leagueoflegends.com/cdn/6.24.1/data/ko_KR/item.json")
    json_data = json.loads(api_data.content.decode("utf-8"))
    return json_data['data']

def get_profile_icons_json(): 
    api_data = requests.get("http://ddragon.leagueoflegends.com/cdn/6.24.1/data/ko_KR/profileicon.json")
    json_data = json.loads(api_data.content.decode("utf-8"))
    return json_data['data']
    
def get_individual_champions(champion):
    api_data = requests.get("http://ddragon.leagueoflegends.com/cdn/6.24.1/data/ko_KR/champion/%s.json" % champion)
    json_data = json.loads(api_data.content.decode("utf-8"))
    return json_data['data']

def get_masteries():
    api_data = requests.get("http://ddragon.leagueoflegends.com/cdn/6.24.1/data/ko_KR/mastery.json")
    json_data = json.loads(api_data.content.decode("utf-8"))
    return json_data['data']

def get_runes():
    api_data = requests.get("http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/rune.json")
    json_data = json.loads(api_data.content.decode("utf-8"))  
    return json_data['data']

def get_summoner_spells():
    api_data = requests.get("http://ddragon.leagueoflegends.com/cdn/6.24.1/data/ko_KR/summoner.json")
    json_data = json.loads(api_data.content.decode("utf-8"))
    return json_data['data']


if __name__ == "__main__":
    summoner_name = "야너어어어엌"
    url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{0}?api_key={1}".format(summoner_name, api_key)
    r = requests.get(url)
    json_data = json.loads(r.content.decode("utf-8"))
    print(json_data)
    # print(get_account_id("야너어어어엌"))