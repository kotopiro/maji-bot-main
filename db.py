import sqlite3

conn = sqlite3.connect("bot.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    guild_id INTEGER,
    user_id INTEGER,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    coins INTEGER DEFAULT 0,
    item TEXT,
    PRIMARY KEY(guild_id, user_id)
)
""")

conn.commit()


def get_user(g, u):
    cur.execute(
        "SELECT xp, level, coins FROM users WHERE guild_id=? AND user_id=?",
        (g, u)
    )
    r = cur.fetchone()

    if not r:
        cur.execute(
            "INSERT INTO users (guild_id,user_id,xp,level,coins) VALUES (?,?,?,?,?)",
            (g, u, 0, 1, 0)
        )
        conn.commit()
        return (0, 1, 0)

    return r


def update_user(g, u, xp=None, level=None, coins=None):

    if xp is not None:
        cur.execute(
            "UPDATE users SET xp=? WHERE guild_id=? AND user_id=?",
            (xp, g, u)
        )

    if level is not None:
        cur.execute(
            "UPDATE users SET level=? WHERE guild_id=? AND user_id=?",
            (level, g, u)
        )

    if coins is not None:
        cur.execute(
            "UPDATE users SET coins=? WHERE guild_id=? AND user_id=?",
            (coins, g, u)
        )

    conn.commit()
