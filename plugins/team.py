from plugins.pluginbase import PluginBase
from plugins.tba import Team as Tm
import dbhandler
import config

class Team(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'team'
        self.command_level = 0
        self.help_mess = '*Help for team commands*\n/team name|motto|location|region|set|website|list XXXX'
        
    def execute(self, msg):
        text = msg['text']
        text = text.split()
        print(text)
        if len(text) > 1:
            lookupmethod = str(text[1])
            if len(text) > 2:
                if text[2].isdigit():
                    team = Tm(str(text[2]), None)
                else:
                    searchuid = dbhandler.getuid(str(text[2]))
                    try:
                        tm = dbhandler.getmemberteam(str(searchuid[0]))
                        print(tm)
                    except TypeError:
                        pass
            if(lookupmethod == 'get'):
                try:
                    self.bot.sendMessage(msg['chat']['id'], str(tm[0]), reply_to_message_id=msg['message_id'])
                except UnboundLocalError:
                    self.bot.sendMessage(msg['chat']['id'], 'Error: Username or name does not exist in system.', reply_to_message_id=msg['message_id'])
            elif(lookupmethod == 'set'):
                try:
                    dbhandler.addUser(msg['from']['id'], text[2])
                except Exception as err:
                    pass
                self.bot.sendMessage('@FRCGlobal', 'You are now listed as a member of team ' + text[2])
            elif(lookupmethod == 'list'):
                txt = "Members of %s in this chat: \n"%(text[2])
                members = dbhandler.getmembersfrom(text[2])
                for member in members:
                    try:
                        mem = self.bot.getChatMember(str(msg['chat']['id']), str(member[0]))
                    except:
                        mem = 'Nope'
                    if mem != "Nope":
                        memb = mem['user']['first_name']
                        if 'last_name' in mem['user']:
                             memb = memb + ' ' + mem['user']['last_name']
                        txt = txt +memb + '\n'
                self.bot.sendMessage(msg['chat']['id'], txt)
            else:
                self.bot.sendMessage(msg['chat']['id'], "Correct syntax:\n/team set|get|list XXXX")
        else:
            self.bot.sendMessage(msg['chat']['id'], "Correct syntax:\n/team set|get|list XXXX")