from er_request import get_request

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