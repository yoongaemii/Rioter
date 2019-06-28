import requests
import json
from PIL import Image
from io import BytesIO
import config

api_key = config.api_key

def get_champion_image(championId):
    '''
    parameter
    championId: string으로 된 id
    ---
    output: png 형식의 챔피언의 이미지
    '''

    championName = get_champion_name(championId)
    
    api_data = requests.get("http://ddragon.leagueoflegends.com/cdn/6.24.1/img/champion/{0}.png".format(championName))
    
    img = Image.open(BytesIO(api_data.content))
    
    return img


def get_champion_name(championId):
    
    api_data = requests.get("http://ddragon.leagueoflegends.com/cdn/9.12.1/data/ko_KR/champion.json")
    
    json_data = json.loads(api_data.content.decode("utf-8"))
    
    champions_info = list(json_data.values())[3]

    # champion Id를 key, champion name을 value로 하는 dictionary 생성

    champion_dict = {}

    for champion, data in champions_info.items():
    
        champion_dict[data['key']] = data['id']

    # parameter로 전달된 championId에 매치되는 name 찾기

    for champion, champion_name in champion_dict.items():
        
        if championId == champion:
            
            championName = champion_name
            
    return championName
#챔피언 Id를 챔피언 Name으로 바꿔주는 함수 --> 숙련도로 챔피언 뽑아왔을 때 Id로 나오기 때문에 이를 Name으로 바꿔줘야 image를 불러올 수 있다


if '__name__' == '__main__':
    get_champion_image('266')



