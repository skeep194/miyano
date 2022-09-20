import json
import requests
import time
from conf import conf

character = json.loads(requests.get(conf["endpoint"] + 'data/Character', headers=conf["header"]).text)["data"]

def getCobaltData(gameId: int):
    req = requests.get(conf["endpoint"] + f'games/{gameId}', headers=conf["header"])
    data: list = json.loads(req.text)["userGames"]
    ret = "승리\n"
    data.sort(key= lambda x:x["gameRank"])
    cnt = 0
    season = 13
    for user in data:
        cnt += 1
        ret += f"솔로 {getUserRank(user['userNum'], season, 1)['name']} 듀오 {getUserRank(user['userNum'], season, 2)['name']} 스쿼드 {getUserRank(user['userNum'], season, 3)['name']}"
        ret += "\n"
        ret += user["nickname"] + " " + character[user["characterNum"]-1]["name"] + " 딜량: " + str(user["damageToPlayer"])
        if cnt == 4:
            ret += "\n\n패배"
        ret += "\n"
    return ret

def getUserRank(userNum: int, seasonId: int, matchingTeamMode: int):
    #when query is 1sec per 1query
   # time.sleep(1.2)
    req = json.loads(requests.get(conf["endpoint"] + f'rank/{userNum}/{seasonId}/{matchingTeamMode}', headers=conf["header"]).text)
    rankName = ["아이언", "브론즈", "실버", "골드", "플래티넘", "다이아몬드"]
    mmr = req["userRank"]["mmr"]
    rank = req["userRank"]["rank"]
    name = f"{rankName[min(5, mmr//400)]} {4 - mmr%400//100} {mmr%400%100}점"
    if mmr >= 2400:
        isEternity = mmr >= 2600 and rank <= 200
        mmr -= 2400
        if isEternity:
            mmr -= 200
        name = ("이터니티" if isEternity else "데미갓") + str(mmr) + "점"
    if rank == 0:
        name = "언랭"
    return {
        "mmr": mmr,
        "name": name
    }


def getUserNum(nickname: str):
    req = requests.get(conf["endpoint"]+f'user/nickname?query={nickname}', headers=conf["header"])
    userNum: int = json.loads(req.text)["user"]["userNum"]
    return userNum