import json
from er_request import get_request
import time
from conf import conf

character = get_request('data/Character')['data']

def get_game_data(game_id: int) -> str:
    try:
        req = get_request(f'games/{game_id}')
    except:
        return '잘못된 gameid'
    if req['userGames'][0]['matchingTeamMode'] == 4:
        return get_cobalt_data(req['userGames'])
    elif req['userGames'][0]['matchingTeamMode'] == 1:
        return '솔로 아직 지원안되는'
    elif req['userGames'][0]['matchingTeamMode'] == 2:
        return '듀오 아직 지원안되는'
    elif req['userGames'][0]['matchingTeamMode'] == 3:
        return '스쿼드 아직 지원안되는'
    return '알 수 없는 에러 발생'

def get_cobalt_data(user_games: list):
    data: list = user_games
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
    rank_name = ["아이언", "브론즈", "실버", "골드", "플래티넘", "다이아몬드"]
    mmr = req["userRank"]["mmr"]
    rank = req["userRank"]["rank"]
    name = f"{rank_name[min(5, mmr//400)]} {4 - mmr%400//100} {mmr%400%100}점"
    if mmr >= 2400:
        is_eternity = mmr >= 2600 and rank <= 200
        mmr -= 2400
        if is_eternity:
            mmr -= 200
        name = ("이터니티" if is_eternity else "데미갓") + " " + str(mmr) + "점"
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