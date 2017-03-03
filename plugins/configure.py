import config
from plugins.pluginbase import PluginBase
import sqlite3

class Configure(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'config'
        self.command_level = 1
        self.help_mess = config.default_help_mess
    
    def execute(self, msg):
        print('Config')
        text = msg['text'].split()
        con = sqlite3.connect('woodieV2.0/frcglobal.db')
        c = con.cursor()
        c.execute('SELECT key FROM messages WHERE key = ?', (text[1], ))
        key = c.fetchone()
        if key is None:
            c.execute('INSERT INTO messages VALUES (?, ?)', (text[1], text[2:]))
        if key is not None:
            c.execute('DELETE FROM messages WHERE key = ?', (text[1], ))
            c.execute('INSERT INTO messages VALUES (?, ?)', (text[1], text[2:len(text)]))
        con.commit()