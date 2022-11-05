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