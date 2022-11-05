import request.get_data as get_data
from conf import conf

def get_cobalt_text(user_games: list):
    data: list = user_games
    character = get_data.get_character()
    ret = "승리\n"
    data.sort(key= lambda x:x['gameRank'])
    cnt = 0
    season = conf['season']
    for user in data:
        cnt += 1
        ret += f"솔로 {get_data.get_user_rank(user['userNum'], season, 1)['name']} 듀오 {get_data.get_user_rank(user['userNum'], season, 2)['name']} 스쿼드 {get_data.get_user_rank(user['userNum'], season, 3)['name']}"
        ret += "\n"
        ret += user["nickname"] + " " + character[user["characterNum"]-1]["name"] + " 딜량: " + str(user["damageToPlayer"])
        if cnt == 4:
            ret += "\n\n패배"
        ret += "\n"
    return ret