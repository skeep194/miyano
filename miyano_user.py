from mongod import miyanodb

def register(discord_id: int, er_nickname: str) -> bool:
    is_user_exist = miyanodb.user.count_documents({"discord_id": discord_id}) > 0
    if is_user_exist:
        miyanodb.user.update_one({"discord_id": discord_id}, { "$set": {"er_nickname": er_nickname }}).matched_count
    else:
        miyanodb.user.insert_one({"discord_id": discord_id, "er_nickname": er_nickname})
    return True

def get_er_nickname(discord_id: int) -> str:
    doc = miyanodb.user.find_one({"discord_id": discord_id})
    if doc == None:
        raise Exception('not found')
    return doc['er_nickname']