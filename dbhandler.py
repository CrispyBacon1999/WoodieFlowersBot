import sqlite3
import botconfig

dblink = 'woodie.db'
def addUser(user_id, team):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    inDb = checkifindb(user_id)
    if not inDb:
        c.execute('INSERT INTO teams VALUES (?, ?)', (user_id, int(team)))
        con.commit()
    else:
        c.execute('DELETE FROM teams WHERE user_id = ?', (user_id,))
        con.commit()
        c.execute('INSERT INTO teams VALUES (?, ?)', (user_id, int(team)))
        con.commit()
    
def checkifindb(user_id):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT user_id FROM teams WHERE user_id = ?', (user_id,))
    data = c.fetchall()
    if data:
        return True
    else:
        return False

def getmembersfrom(team):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT user_id FROM teams WHERE team = ?', (str(team),))
    members = c.fetchall()
    return members
    
def warn(user_id, num):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT user_id FROM warns WHERE user_id = ?', (user_id,))
    if c.fetchall:
       c.execute('DELETE FROM warns WHERE user_id = ?', (user_id,))
    c.execute('INSERT INTO warns VALUES (?, ?)', (user_id, num))
    con.commit()
def getwarns(user_id):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT num FROM warns WHERE user_id = ?', (user_id,))
    warns = c.fetchall()
    if warns == []:
        warns = 0
    else:
        warns = warns[0][0]
    return warns
    
def refreshuser_id(username, user_id):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT username FROM usernames WHERE username = ? AND user_id = ?', (username, user_id))
    uname = c.fetchone()
    if uname is None:
        c.execute('SELECT username FROM usernames WHERE user_id = ?', (user_id,))
        uname = c.fetchone()
        if uname is not None:
            c.execute('DELETE FROM usernames WHERE user_id = ?', (user_id, ))
        c.execute('INSERT INTO usernames VALUES (?, ?)', (user_id, username))
    con.commit()

def adduser_info(user_id, value, type):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT value FROM userdata WHERE user_id = ? AND type = ? AND value = ?', (user_id, type, value))
    value_pulled = c.fetchone()
    if value_pulled is None:
        c.execute('SELECT value FROM userdata WHERE user_id = ? AND type = ?', (user_id, type))
        value_pulled = c.fetchone()
        if value_pulled is not None:
            c.execute('DELETE FROM userdata WHERE user_id = ? AND type = ?', (user_id, type))
        c.execute('INSERT INTO userdata VALUES (?, ?, ?)', (user_id, value, type))
    con.commit()

def getuser_info(user_id, type):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT value FROM userdata WHERE user_id = ? AND type = ?', (user_id, type))
    return c.fetchone()

def getuid(username):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT user_id FROM usernames WHERE username = ?', (username,))
    user_id = c.fetchone()
    con.commit()
    return user_id

def getusername(user_id):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT username FROM usernames WHERE user_id = ?', (user_id,))
    uname = c.fetchone()
    con.commit()
    return uname

def getmemberteam(user_id):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT team FROM teams WHERE user_id = ?', (user_id,))
    team = c.fetchone()
    con.commit()
    return team

def addrank(user_id, rank):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    #Remove old rank
    c.execute('DELETE FROM ranks WHERE user_id = ?', (user_id, ))
    #Add new rank
    c.execute('INSERT INTO ranks VALUES (?, ?)', (user_id, rank))
    con.commit()

def getrank(user_id):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT rank FROM ranks WHERE user_id = ?', (user_id, ))
    rank = c.fetchone()
    if not rank:
        return ("Default",)
    else:
        return rank
        
def getdistinctteams():
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT DISTINCT team FROM teams')
    teams = c.fetchall()
    return teams
    
def addxp(user_id, xp):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT user_id FROM userxp WHERE user_id = ?', (user_id,))
    if(c.fetchone() is None):
        c.execute('INSERT INTO userxp VALUES (?, ?)', (user_id, xp))
    else:
        c.execute('SELECT xp FROM userxp WHERE user_id = ?', (user_id,))
        uxp = c.fetchone()
        # Add xp to current xp
        c.execute('UPDATE userxp SET xp = ? WHERE user_id = ?', (uxp + xp, user_id))
    con.commit()
    
def addrequest(user_id, request):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('INSERT INTO requests VALUES (?, ?)', (user_id, str(request)))
    con.commit()
    
def addbind(sticker, command):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT sticker FROM stickerbinds WHERE sticker = ?', (sticker,))
    if(c.fetchone()):
        print('Sticker already bound')
        return False
    else:
        print('Inserting Sticker')
        c.execute('INSERT INTO stickerbinds VALUES (?, ?)', (sticker, command))
        con.commit()
        return True
def isbind(sticker):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT sticker FROM stickerbinds WHERE sticker = ?', (sticker,))
    if(c.fetchone()):
        return True
    else:
        return False

def getbind(sticker):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT command FROM stickerbinds WHERE sticker = ?', (sticker,))
    return c.fetchone()