import request.get_data as get_data
from result_text.cobalt import get_cobalt_text
from result_text.lumia import get_lumia_text
from result_image.cobalt import get_cobalt_image

def get_game_data(game_id: int, type: str) -> str:
    try:
        req = get_data.get_game(game_id)
    except:
        return '잘못된 gameid'
    user_games = req
    game_mode = req[0]['matchingTeamMode']
    try:
        if type == "text":
            if game_mode == 4:
                return get_cobalt_text(user_games)
            elif 1 <= game_mode <= 3:
                return get_lumia_text(user_games, game_mode)
        elif type == "image":
            if game_mode == 4:
                return get_cobalt_image(user_games, "temp")
            elif 1 <= game_mode <= 3:
                return "lumia image"
    except:
        return '알 수 없는 에러 발생'
    return '진짜 말도안되는 에러 발생 이 문장이 출력될일은 없어야함'