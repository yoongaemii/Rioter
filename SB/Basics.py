#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import json
from pprint import pprint
from RiotRequest import RiotRequest

api_key = "RGAPI-e9082b86-f6ce-41ba-860a-c962eb529056"

def get_account_id(summoner_name):

    json_data = RiotRequest("https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{0}?api_key={1}".format(summoner_name, api_key))

#    print(json_data)

    return json_data['accountId']

def get_timeline(match_id):
    json_data = RiotRequest("https://kr.api.riotgames.com/lol/match/v4/timelines/by-match/{0}?api_key={1}".format(match_id, api_key))
    
    return json_data

def get_match_history(account_id):

    json_data = RiotRequest("https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/{0}?api_key={1}".format(account_id, api_key))

#   pprint(json_data['matches'])

    game_id_list = [match['gameId'] for match in json_data['matches']]

    return game_id_list


def get_game_detail(game_id):

    json_data = RiotRequest("https://kr.api.riotgames.com//lol/match/v4/matches/{0}?api_key={1}".format(game_id, api_key))

#    pprint(json_data['participants'])

    return json_data

def get_champion_json():
    
    api_data = requests.get("http://ddragon.leagueoflegends.com/cdn/9.8.1/data/ko_KR/champion.json")
    
    json_data = json.loads(api_data.content.decode("utf-8"))
    
    champions_info = list(json_data.values())[3]
    champions_list = list(champions_info.values())
    champion_dict={}
    for champion in champions_list:
        champion_dict[champion['key']] = champion['id']
    
    return champion_dict

def get_item_json():
    
    api_data = requests.get("http://ddragon.leagueoflegends.com/cdn/9.8.1/data/ko_KR/item.json")
    
    json_data = json.loads(api_data.content.decode("utf-8"))
    
    pprint(json_data['data'])
    
    return json_data['data']

def get_profile_icons_json(): 
    
    api_data = requests.get("http://ddragon.leagueoflegends.com/cdn/9.8.1/data/ko_KR/profileicon.json")
    
    json_data = json.loads(api_data.content.decode("utf-8"))
    
    pprint(json_data['data'])
    
    return json_data['data']
    
def get_individual_champions(champion):
    #modified by Sunny
    api_data = requests.get("http://ddragon.leagueoflegends.com/cdn/9.8.1/data/ko_KR/champion/%s.json" % champion)
    
    json_data = json.loads(api_data.content.decode("utf-8"))
    
    #pprint(json_data['data'])
    
    return json_data['data'][champion]

def get_masteries():
    
    api_data = requests.get("http://ddragon.leagueoflegends.com/cdn/9.8.1/data/ko_KR/mastery.json")
    
    json_data = json.loads(api_data.content.decode("utf-8"))
    
    pprint(json_data['data'])
    
    return json_data['data']

def get_runes():
    
    api_data = requests.get("http://ddragon.leagueoflegends.com/cdn/9.8.1/data/en_US/rune.json")
    
    json_data = json.loads(api_data.content.decode("utf-8"))
    
    pprint(json_data['data'])
    
    return json_data['data']

def get_summoner_spells():
    
    api_data = requests.get("http://ddragon.leagueoflegends.com/cdn/9.8.1/data/ko_KR/summoner.json")
    
    json_data = json.loads(api_data.content.decode("utf-8"))
    
    pprint(json_data['data'])
    
    return json_data['data']

