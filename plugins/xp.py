from plugins import plugin
import sqlite3
import lang
import random
import re
import time


class XP(plugin.Plugin):

    def __init__(self, bot):
        plugin.Plugin.__init__(self, bot, command='xp')

    def execute(self, msg):
        if len(msg['text'].split()) > 1:
            username = ''.join(msg['text'].split()[1:])
            username = re.sub('@', '', username)
            con = sqlite3.connect(botconfig.database)
            c = con.cursor()
            c.execute('SELECT user_id FROM usernames WHERE username = ?', (username,))
            user_id = c.fetchone()
            if not user_id:
                if 'reply_to_message' in msg:
                    user_id = msg['reply_to_message']['from']['id']
                else:
                    user_id = msg['from']['id']
            else:
                user_id = user_id[0]
            con.commit()
        else:
            if 'reply_to_message' in msg:
                user_id = msg['reply_to_message']['from']['id']
            else:
                user_id = msg['from']['id']
        connection = sqlite3.connect(botconfig.database)
        cursor = connection.cursor()
        cursor.execute('SELECT current_xp FROM xp WHERE user_id = ?', (user_id, ))
        current_xp = cursor.fetchone()
        if not current_xp:
            self.bot.sendMessage(msg['chat']['id'], lang.xp['none'])
        else:
            try:
                user = self.bot.getChatMember(msg['chat']['id'], user_id)['user']
                if 'last_name' in user:
                    self.bot.sendMessage(msg['chat']['id'], lang.xp['firstlast'] %
                                     (user['first_name'], user['last_name'], current_xp[0]))
                else:
                    self.bot.sendMessage(msg['chat']['id'], lang.xp['nolast'] %
                                     (user['first_name'], current_xp[0]))
            except:
                pass


def add_xp(user_id):
    connection = sqlite3.connect(botconfig.database)
    cursor = connection.cursor()
    cursor.execute('SELECT time FROM xpclock WHERE user_id = ?', (user_id,))
    xptime = cursor.fetchone()
    if not xptime:
        cursor.execute('SELECT current_xp FROM xp WHERE user_id = ?', (user_id,))
        xp = cursor.fetchone()
        if xp:
            xp = xp + random.randint(1, 10)
            cursor.execute('UPDATE xp SET current_xp = ? WHERE user_id = ?', (xp, user_id))
        else:
            xp = random.randint(1, 10)
            cursor.execute('INSERT INTO xp VALUES (?, ?)', (user_id, xp))
        cursor.execute('INSERT INTO xpclock VALUES (?, ?)', (user_id, int(time.time())))
    else:
        if int(time.time()) - xptime[0] >= 60:
            cursor.execute('SELECT current_xp FROM xp WHERE user_id = ?', (user_id,))
            xp = cursor.fetchone()[0]
            xp += random.randint(1, 10)
            cursor.execute('UPDATE xp SET current_xp = ? WHERE user_id = ?', (xp, user_id))
            cursor.execute('UPDATE xpclock SET time = ? WHERE user_id = ?', (int(time.time()), user_id))

    connection.commit()
