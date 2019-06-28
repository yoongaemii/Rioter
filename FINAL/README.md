# Riot api를 활용한 게임 데이터 분석
三人成虎 - 옛 말에 사람이 셋이면 호랑이도 만들 수 있다고 했습니다. 롤에서는 둘만있어도 게임을 승리로 이끌 수 있죠,  정치 없이 게임할 수 있는 것은 보너스~ 지금 바로 rioter.gg에서 당신의 운명의 짝궁을 찾아보세요!

아이디어: 플레이 시각으로 시각화를 해 본 결과 플레이 시간에 패턴이 명확히 존재하는 것으로 확인됨
`filename.ipynb`
-->  주 플레이 시간대가 비슷한 사람끼리 매칭해주는 프로덕트를 기획

## 1. 데이터 수집
### `RiotRequest.py`  

Riot에서는 게임 데이터를 크롤링할 수 있는 API key를 제공합니다. LOL 아이디가 있으면 누구나 발급받을 수 있지만 엄격한 Rate Limiting이 존재합니다.
참고: [Riot의 Rate Limiting 관련 정책](https://developer.riotgames.com/rate-limiting.html)
> In order to control the use of the Riot Games API, we set limits on how many times endpoints can be accessed within a given time period. These limits are put in place to minimize abuse, to maintain a high level of stability, and to protect the underlying systems that back the API from being overloaded. The underlying systems are the same systems that power League of Legends, so if they are overloaded, player experience suffers, and our first priority is to protect that experience.  

일반적으로 발급받은 API key로는 1초에 20개 이내, 2분에 100개 이내의 리퀘스트를 보낼 수 있습니다. 이 제한을 초과하여 반복적으로 요청을 보낼 경우 API key 자체의 접근이 금지될 수 있으므로 제한을 지키기 위해 모든 함수는 `RiotReqeust`라는 함수를 통해 요청하도록 설계했습니다.

`RiotRequest` 함수는 파이썬 내장 라이브러리 request의 status_code를 활용해 reponse code의 종류에 따라 데이터를 반환하거나 에러에 대응합니다. 예를 들면 html 헤더가 200일 경우 json 데이터를 decode한 뒤 반환하고 429일 경우 상황에 따라 몇 초 후에 동일한 요청을 다시 시도합니다.

### `RiotAPI`  

RiotAPI는 공식 document에 포함되어있는 API call을 사용하기 쉽도록 함수로 정리한 파일입니다. 데이터 내용이 수시로 업데이트 되는 Dynamic Call과 영웅 정보, 아이템 정보 등 패치 이후 바뀌지 않는 Static Call이 있습니다. Dynamic Call은 모두 Rate Limiting을 준수하기 위해 `RiotRequest` 함수를 사용합니다. 다른 코드에서 필요한 함수를 선택적으로 import해서 사용합니다.


### `DataCollection.ipynb`
기본적으로 필요한 정보는 1) 랭크 별 사용자 정보 2) 사용자 별 게임 기록 입니다. 이들은 모두 수집 후에 pickle로 저장한 뒤 활용했습니다.
#### 1) 랭크 별 사용자 정보
Riot API는 랭크 별 사용자의 summoner ID 의 목록을 제공합니다. 이 summoner ID는 게임 상에 닉네임으로 노출되는 summoner name과는 다른 정보로 각 계정 마다 고유하게 부여되는 string입니다. 하지만 사용자별 게임 기록을 수집하는 요청 뿐 아니라 대부분의 Riot API 요청에서 사용자의 정보는 account id로 전달하거나 표시합니다. 그러므로 각 랭크 별로 summoner id를 수집한 뒤에는 account id로 변환했습니다.
#### 2) 사용자 별 게임 기록
참고: [공식 도큐먼트](https://developer.riotgames.com/api-methods/#match-v4/GET_getMatchlist)  
이후 사용자가 참여한 게임 기록을 수집합니다. 한 번의 요청으로 100개의 매치 기록을 불러올 수 있으며, 2019년 6월 기준 현재 진행 중인 시즌 9의 게임 기록만을 수집했습니다.


### 데이터 수집의 맹점
- API key의 수집 속도 제한
- API key 마다 summoner id와 account id의 encrypt 방식이 상이


## 2. 데이터 가공

### 주요 포지션 `DataProcessing-Position.ipynb`
롤에는 다섯 가지 포지션이 존재합니다. 포지션에 따라 플레이어는 긴밀하게 협력하기도 하고 비교적 서로에게 영향을 받지 않고 플레이하기도 합니다. 그러므로 각 계정마다 이번 시즌 게임에 플레이한 포지션을 종합해 '주요 포지션'을 추출했습니다. 이 포지션에 따라 아래와 같이 듀오를 추천합니다. 예를 들면 원거리 딜러를 주로 플레이하는 사용자에게는 같은 바텀 라인에서 협력해서 플레이하는 서포터를 추천해줍니다.

| 추천 받는 사용자의 포지션 | 추천해주는 사용자의 포지션 |
| ----------- | ----------- |
| 미드 | 정글 |
| 정글 | 미드 |
| 탑 | 정글 |
| 서폿 | 원딜 |
| 원딜 | 서폿 |

### 플레이 시간 `DataProcessing-Time.ipynb`
함께 플레이를 하기 위해서는 주로 플레이하는 시간이 어느 정도 겹쳐야합니다. 플레이 시간대는 개별 사용자의 사정에 따라 변하므로 1월 28일에 시작한 최근 시간의 플레이 시간대만 활용했습니다.
구체적으로 사용자 별로 요일을 column으로, 30분 단위로 자른 시간대를 row로 하는 행렬을 만든 뒤, 모든 쌍의 행렬에 대해 euclidean distance를 계산하여 비슷한 시간대에 플레이하는 사용자를 알아냈습니다.


### 주요 챔피언: `DataProcessing-Champion.ipynb`
챔피언은 롤에서 고유한 스킬과 특성을 가진 캐릭터로, 게임마다 사용자가 선택할 수 있습니다. 챔피언 숙련도는 특정 챔피언을 사용할 수록 점수가 누적됩니다. 그러므로 한 사용자의 챔피언 숙련도를 비교해서 주로 사용하는 챔피언을 알 수 있습니다.
Rioter.gg에서는 추천하는 사용자의 주챔피언을 보여줍니다. 주챔피언을 통해 해당 사용자의 플레이스타일을 짐작할 수 있고, 본인이 주로 사용하는 챔피언과의 조합을 고려해 듀오를 탐색할 수 있습니다.


### 승률 `DataProcessing-Winrate.ipynb`
사용자를 추천 받은 뒤 추천한 사용자의 최근 100 경기의 승률을 같이 표시해줍니다.

## 3. 서비스 구축

### `ServiceUtility.py`
챔피언의 이미지를 불러오는 등 실제 서비스 구현에 필요한 함수를 담은 코드입니다.


