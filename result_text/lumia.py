import request.get_data as get_data

def get_lumia_text(user_games: list, game_mode: int):
    character = get_data.get_character()
    ret = ''
    user_games.sort(key= lambda x:x['gameRank'])
    for idx, user in enumerate(user_games):
        if idx % game_mode == 0:
            ret += f'{idx//game_mode+1}등\n'
        ret += f"{user['nickname']} {character[user['characterNum']-1]['name']} 딜량: {user['damageToPlayer']}\n"
    return ret