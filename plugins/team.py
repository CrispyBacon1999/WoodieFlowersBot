from plugins.pluginbase import PluginBase
from plugins.tba import Team as Tm
from theblueallianceapi import Team as Tm
import dbhandler
import config

class Team(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'team'
        self.command_level = 0
        self.help_mess = config.team_help_mess
        
    def execute(self, msg):
        text = msg['text']
        text = text.split()
        if len(text) > 1:
            lookupmethod = str(text[1])
            if len(text) >= 2:
                if len(text) > 2:
                    if text[2].isdigit():
                        team = Tm(str(text[2]), None)
                    else:
                        if(str(text[2][0]) == '@'):
                            uname = str(text[2][1:])
                        searchuid = dbhandler.getuid(uname)
                        try:
                            tm = dbhandler.getmemberteam(searchuid[0])
                        except TypeError:
                            pass
            if(lookupmethod == 'get'):
                print(tm)
                try:
                    self.bot.sendMessage(msg['chat']['id'], str(tm[0]), reply_to_message_id=msg['message_id'])
                except UnboundLocalError:
                    self.bot.sendMessage(msg['chat']['id'], 'Error: Username or name does not exist in system.', reply_to_message_id=msg['message_id'])
            elif(lookupmethod == 'set'):
                if isintable(text[2]):
                    t_team = Tm(text[2], None)
                    if not t_team.info['name'] == None:
                        try:
                            dbhandler.addUser(msg['from']['id'], text[2])
                        except Exception as err:
                            pass
                        self.bot.sendMessage(msg['chat']['id'], 'You are now listed as a member of team ' + text[2])
                    else:
                        self.bot.sendMessage(msg['chat']['id'], 'Not a valid team.')
                else:
                    self.bot.sendMessage(msg['chat']['id'], 'Not a valid team.')
            elif(lookupmethod == 'list'):
                if len(text) == 2:
                    txt = 'All teams in this chat:\n\n'
                    teams = dbhandler.getdistinctteams()
                    teams = [int(x[0]) for x in teams]
                    teams.sort()
                    for team in teams:
                        txt += str(team) + '\n'
                    self.bot.sendMessage(msg['chat']['id'], txt)
                else:
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
            
            

def isintable(value):
  try:
    int(value)
    return True
  except:
    return False