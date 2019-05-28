from RiotAPI import *
from datetime import timedelta
from datetime import datetime
import pytz

def convert_timedelta(milisecs):
    '''
    convert milisecond timestamp into python timedelta object
    for sake of compatiability, convert into only minutes and seconds (without hours)
    '''
    minDelta = timestamp // 60000 # 60000 miliseconds == 1 minute
    secDelta = (timestamp % 60000) // 1000 # 1000 miliseconds == 1 second
    return timedelta(minutes = minDelta, seconds = secDelta)

def convert_timestamp(timestamp):
    '''convert unix timestamp(long) into python datetime object with Korean Timezone'''
   
    # dealing with miliseconds part
    timestamp = timestamp/1000
    # convert from utc into datetime timestamp
    dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    
    # convert into Korean timezone
    tz = pytz.timezone("Asia/Seoul")
    dt_kr = dt.astimezone(tz)
    
    return dt_kr

def win_match(accountId, matchId):
    '''
    accountId가 matchId에서 이겼으면 True, 졌으면 False를 반환.
    내부에서 get_game_detail 리퀘스트를 보낸다 
    '''
    
    detail = get_game_detail(matchId)
    
    # get the participant Id of the user in the specific match
    for p in detail['participantIdentities']:
        if p['player']['accountId'] == accountId:
            participantId = p['participantId']
            break
            
    # team 100의 결과('Fail' or 'Win')
    team100 = detail['teams'][0]['win'] 
    
    # participant belongs to team 100
    if participantId <= 5:    
        return team100 == 'Win' 
    
    # participant belongs to team 200
    else:            
        return team100 == 'Fail'