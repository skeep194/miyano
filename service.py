import json
from request.er_request import get_request
import time
from PIL import Image, ImageDraw, ImageFont

character = get_request('data/Character')['data']

def get_game_data(game_id: int) -> str:
    try:
        req = get_request(f'games/{game_id}')
    except:
        return '잘못된 gameid'
    user_games = req['userGames']
    game_mode = req['userGames'][0]['matchingTeamMode']
    try:
        if game_mode == 4:
            return get_cobalt_data(user_games)
        elif 1 <= game_mode <= 3:
            return get_lumia_data(user_games, game_mode)
    except:
        return '알 수 없는 에러 발생'
    return '진짜 말도안되는 에러 발생 이 문장이 출력될일은 없어야함'

def get_lumia_data(user_games: list, game_mode: int):
    ret = ''
    user_games.sort(key= lambda x:x['gameRank'])
    for idx, user in enumerate(user_games):
        if idx % game_mode == 0:
            ret += f'{idx//game_mode+1}등\n'
        ret += f"{user['nickname']} {character[user['characterNum']-1]['name']} 딜량: {user['damageToPlayer']}\n"
    return ret

def get_cobalt_data(user_games: list):
    data: list = user_games
    ret = "승리\n"
    data.sort(key= lambda x:x['gameRank'])
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

def get_cobalt_image(user_games: list):
    user_games.sort(key= lambda x:x['gameRank'])
    size_value = conf['image']['cobalt']

    im = Image.new('RGBA', tuple(size_value['background_size']))

    background = Image.open('/root/Miyano/image/background/s7.png')
    background_gray = Image.open('/root/Miyano/image/background/transparent_gray.png')
    charactor_image = Image.open('/root/Miyano/image/character/Jackie_mini.png')

    im.paste(background)
    im.paste(background_gray, mask=background_gray)

    win = user_games[0:4]
    lose = user_games[4:8]
    fnt = ImageFont.truetype('/root/Miyano/font/NanumGothic.ttf', 30)
    background_draw = ImageDraw.Draw(im)

    for i, user in enumerate(win):
        charactor_image = Image.open(f"/root/Miyano/image/character/{character[user['characterNum']-1]['name']}_mini.png")
        background_draw.text((size_value['margin_side'], 65 + i*size_value['character_interval']), f"{user['nickname']}", font=fnt)
        im.paste(charactor_image, (size_value['margin_side'], size_value['margin_top']+i*size_value['character_interval']), charactor_image)
    im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    for i, user in enumerate(lose):
        charactor_image = Image.open(f"/root/Miyano/image/character/{character[user['characterNum']-1]['name']}_mini.png").transpose(0)
        temp = background_draw.textbbox((0, 0), f"{user['nickname']}", font=fnt)
        textim = Image.new('RGBA', (temp[0]+temp[2], temp[1]+temp[3]), (0, 0, 0, 0))
        d = ImageDraw.Draw(textim)
        d.text((0, 0), f"{user['nickname']}", font=fnt)
        textim = textim.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        im.paste(textim, (size_value['margin_side'], 65 + i*size_value['character_interval']), textim)
        im.paste(charactor_image, (size_value['margin_side'], size_value['margin_top']+i*size_value['character_interval']), charactor_image)
    im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    
    im.save('/root/Miyano/temp.png')

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