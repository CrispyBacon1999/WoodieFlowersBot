import sqlite3

dblink = 'woodieV2.0/frcglobal.db'

def addUser(uid, team):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    inDb = checkifindb(uid)
    if not inDb:
        c.execute('INSERT INTO memberteams VALUES (?, ?)', (uid, team))
        con.commit()
    else:
        c.execute('DELETE FROM memberteams WHERE uid = ?', (uid,))
        con.commit()
        c.execute('INSERT INTO memberteams VALUES (?, ?)', (uid, team))
        con.commit()
    
def checkifindb(uid):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT uid FROM memberteams WHERE uid = ?', (uid,))
    data = c.fetchall()
    if data:
        return True
    else:
        return False

def getmembersfrom(team):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT uid FROM memberteams WHERE team = ?', (str(team),))
    members = c.fetchall()
    return members
    
def warn(uid, num):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT uid FROM warns WHERE uid = ?', (uid,))
    if c.fetchall:
       c.execute('DELETE FROM warns WHERE uid = ?', (uid,))
    c.execute('INSERT INTO warns VALUES (?, ?)', (uid, num))
    con.commit()
def getwarns(uid):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT num FROM warns WHERE uid = ?', (uid,))
    warns = c.fetchall()
    if warns == []:
        warns = 0
    else:
        warns = warns[0][0]
    return warns
    
def refreshuid(username, uid):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT username FROM usernames WHERE username = ? AND uid = ?', (username,uid))
    uname = c.fetchone()
    if uname is None:
        c.execute('SELECT username FROM usernames WHERE uid = ?', (uid,))
        uname = c.fetchone()
        if uname is not None:
            c.execute('DELETE FROM usernames WHERE uid = ?', (uid, ))
        c.execute('INSERT INTO usernames VALUES (?, ?)', (username, uid))
    con.commit()

def getuid(username):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT uid FROM usernames WHERE username = ?', (username,))
    uid = c.fetchone()
    con.commit()
    return uid

def getusername(uid):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT username FROM usernames WHERE uid = ?', (uid,))
    uname = c.fetchone()
    con.commit()
    return uname

def getmemberteam(uid):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT team FROM memberteams WHERE uid = ?', (uid,))
    team = c.fetchone()
    con.commit()
    return team

def addrank(uid, rank):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    #Remove old rank
    c.execute('DELETE FROM ranks WHERE uid = ?', (uid, ))
    #Add new rank
    c.execute('INSERT INTO ranks VALUES (?, ?)', (uid, rank))
    con.commit()

def getrank(uid):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT rank FROM ranks WHERE uid = ?', (uid, ))
    rank = c.fetchone()
    if not rank:
        return ("Default",)
    else:
        return rank
        
def getdistinctteams():
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT DISTINCT team FROM memberteams')
    teams = c.fetchall()
    return teams
    
def addxp(uid, xp):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('SELECT uid FROM userxp WHERE uid = ?', (uid,))
    if(c.fetchone() is None):
        c.execute('INSERT INTO userxp VALUES (?, ?)', (uid, xp))
    else:
        c.execute('SELECT xp FROM userxp WHERE uid = ?', (uid,))
        uxp = c.fetchone()
        # Add xp to current xp
        c.execute('UPDATE userxp SET xp = ? WHERE uid = ?', (uxp + xp, uid))
    con.commit()
    
def addrequest(uid, request):
    con = sqlite3.connect(dblink)
    c = con.cursor()
    c.execute('INSERT INTO requests VALUES (?, ?)', (uid, str(request)))
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