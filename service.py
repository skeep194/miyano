import json
from er_request import get_request
import time
from conf import conf

character = get_request('data/Character')["data"]

def get_cobalt_data(gameId: int):
    req = get_request(f'games/{gameId}')
    data: list = req["userGames"]
    ret = "승리\n"
    data.sort(key= lambda x:x["gameRank"])
    cnt = 0
    season = 13
    for user in data:
        cnt += 1
        ret += f"솔로 {get_user_rank(user['userNum'], season, 1)['name']} 듀오 {get_user_rank(user['userNum'], season, 2)['name']} 스쿼드 {get_user_rank(user['userNum'], season, 3)['name']}"
        ret += "\n"
        ret += user["nickname"] + " " + character[user["characterNum"]-1]["name"] + " 딜량: " + str(user["damageToPlayer"])
        if cnt == 4:
            ret += "\n\n패배"
        ret += "\n"
    return ret

def get_user_rank(userNum: int, seasonId: int, matchingTeamMode: int):
    req = get_request(f'rank/{userNum}/{seasonId}/{matchingTeamMode}')
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


def get_user_num(nickname: str):
    req = get_request(f'user/nickname?query={nickname}')
    userNum: int = req["user"]["userNum"]
    return userNum