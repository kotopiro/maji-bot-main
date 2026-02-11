import sqlite3

conn = sqlite3.connect("bot.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
guild INTEGER,
user INTEGER,
xp INTEGER,
level INTEGER,
coins INTEGER,
PRIMARY KEY(guild,user),
guild INTEGER,
user INTEGER,
item TEXT
)
""")

conn.commit()

def get_user(g,u):
    cur.execute("SELECT xp,level,coins FROM users WHERE guild=? AND user=?", (g,u))
    r = cur.fetchone()
    if not r:
        cur.execute("INSERT INTO users VALUES(?,?,?,?,?)",(g,u,0,1,0))
        conn.commit()
        return (0,1,0)
    return r

def update_user(g,u,xp=None,level=None,coins=None):
    if xp is not None:
        cur.execute("UPDATE users SET xp=? WHERE guild=? AND user=?", (xp,g,u))
    if level is not None:
        cur.execute("UPDATE users SET level=? WHERE guild=? AND user=?", (level,g,u))
    if coins is not None:
        cur.execute("UPDATE users SET coins=? WHERE guild=? AND user=?", (coins,g,u))
    conn.commit()
