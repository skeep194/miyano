from conf import conf
from PIL import Image, ImageFont, ImageDraw, ImageColor
import copy
import request.get_data
import secrets
import string
from general.math import internal_division

size_value = conf['image']['cobalt']
character = request.get_data.get_character()

im = Image.new('RGBA', tuple(size_value['background_size']))
background = Image.open('/root/Miyano/image/background/s8.png')
background_gray = Image.open('/root/Miyano/image/background/transparent_gray.png')
fnt = ImageFont.truetype('/root/Miyano/font/NanumGothic.ttf', 30)

im.paste(background)
im.paste(background_gray, mask=background_gray)

result = im

def get_text_box(text: str, flip: bool) -> Image:
    background_draw = ImageDraw.Draw(result)
    bbox = background_draw.multiline_textbbox((0, 0), text, font=fnt)
    textim = Image.new('RGBA', (bbox[0]+bbox[2], bbox[1]+bbox[3]), (0, 0, 0, 0))
    d = ImageDraw.Draw(textim)
    d.multiline_text((0, 0), text, font=fnt, align="right" if flip else "left")
    if flip:
        textim = textim.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    return textim

def draw_nickname(i: int, user, flip: bool):
    background_draw = ImageDraw.Draw(result)
    tier_solo: str = request.get_data.get_user_rank(user['userNum'], conf['season'], 1)['name']
    tier_duo: str = request.get_data.get_user_rank(user['userNum'], conf['season'], 2)['name']
    tier_squad: str = request.get_data.get_user_rank(user['userNum'], conf['season'], 3)['name']
    kill: str = user['playerKill']
    death: str = user['playerDeaths']
    assist: str = user['playerAssistant']

    nickname: str = f"{user['nickname']} ({tier_solo}/{tier_duo}/{tier_squad})\nK {kill}/D {death}/A {assist}"
    textbox = get_text_box(nickname, flip)
    result.paste(textbox, (size_value['margin_side'], size_value['nickname_start'] + i*size_value['character_interval']), textbox)
    return

def draw_character(i: int, user, flip: bool):
    character_image = Image.open(f"/root/Miyano/image/character/{character[user['characterNum']-1]['name']}_mini.png")
    if flip:
        character_image.transpose(0)
    result.paste(character_image, (size_value['margin_side'], size_value['character_start']+i*size_value['character_interval']), character_image)
    return

def draw_graph(i: int, user, flip: bool):
    background_draw = ImageDraw.Draw(result)
    values = [
        {"value": 'damageToPlayer', "color": "red", "text": "가한 데미지"},
        {"value": 'damageFromPlayer', "color": "blue", "text": "입은 데미지"},
        {"value": 'healAmount', "color": "green", "text": "회복량"}
    ]
    cnt = len(values)
    base = size_value['graph_base']

    text_start_x = size_value['margin_side']+size_value['character_x']+size_value['margin_character_graph_text']
    graph_start_x = text_start_x + size_value['margin_character_graph']
    start_y = size_value['character_start']+i*size_value['character_interval']

    j = 0
    for v in values:
        value = v['value']
        color = v['color']
        text = v['text']
        if flip:
            text = f"{user[value]} {text}"
        else:
            text = f"{text} {user[value]}"

        graph_y = size_value['graph_y']
        textbox = get_text_box(text, flip)
        text_y = textbox.height
        graph_start_y = start_y + (size_value['character_y']) // cnt * j + 10
        background_draw.rounded_rectangle([(graph_start_x-10, graph_start_y), (internal_division(graph_start_x-10, size_value['background_size'][0]//2, user[value], base-user[value]), graph_start_y+text_y)], radius=10, fill=ImageColor.getrgb(color))
        result.paste(textbox, (text_start_x, graph_start_y), textbox)
        j += 1
    return

def draw_data(i: int, user, flip: bool):
    draw_nickname(i, user, flip)
    draw_character(i, user, flip)
    draw_graph(i, user, flip)

def get_cobalt_image(user_games: list) -> str:
    global result
    result = copy.deepcopy(im)

    user_games.sort(key= lambda x:x['gameRank'])
    win = user_games[0:4]
    lose = user_games[4:8]
    
    for i, user in enumerate(win):
        draw_data(i, user, False)
    result = result.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    for i, user in enumerate(lose):
        draw_data(i, user, True)
    result = result.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    
    file_name = ''.join((secrets.choice(string.ascii_letters) for i in range(8)))
    result.save(f'/root/Miyano/temp_image/{file_name}.png')
    return file_name