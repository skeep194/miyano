from mysql import conn, cur

def register(discord_id: int, er_nickname: str) -> bool:
    cur.execute('SELECT * FROM user WHERE discord_id=%s', (str(discord_id)))
    res = 0
    if len(cur.fetchall()) == 1:
        res = cur.execute('UPDATE user SET er_nickname=%s WHERE discord_id=%s', (er_nickname, str(discord_id)))
    else:
        res = cur.execute('INSERT INTO user(discord_id, er_nickname) VALUE(%s, %s)', (str(discord_id), er_nickname))
    conn.commit()
    return res == 1

def get_er_nickname(discord_id: int) -> str:
    cur.execute('SELECT er_nickname FROM user WHERE discord_id=%s', (str(discord_id)))
    row = cur.fetchall()
    if len(row) == 0:
        return ""
    return row[0][0]
