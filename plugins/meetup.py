import config
from plugins.pluginbase import PluginBase
import dbhandler
from theblueallianceapi import *
import re
import itertools

class Meetups(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'meetup'
        self.command_level = 0
        self.help_mess = config.default_help_mess
    
    def execute(self, msg):
        teams = dbhandler.getdistinctteams()
        teamevents = []
        teamorder = []
        i = 0
        for team in teams:
            if is_number(team[0]):
                print(team[0])
                teamobj = Team(team[0], None)
                if 'events' in teamobj.info:
                    events = re.findall('_(.*?)_',teamobj.info['events'])
                    teamevents.append([])
                    for event in events:
                        event = re.sub('([\*_])+', '', event)
                        print(event)
                        teamevents[i].append(event)
                    teamorder.append(team[0])
                    i+=1
        print(teamevents)
        sameevents = []
        
        for x, left in enumerate(teamevents):
            for y, right in enumerate(teamevents):
                n = 0
                for h in left:
                    for k in right:
                        if(h == k):
                            n += 1
                common = len(set(left) & set(right))
                if(common > 0):
                    if(not teamorder[x] == teamorder[y]):
                        sameevents.append('%s and %s.' % (teamorder[x], teamorder[y]))
        
        print(sameevents)
        txt = '*The following teams will both be at one or more events together:*\n\n'
        for teams in sameevents:
            txt += teams + '\n'
        self.bot.sendMessage(msg['chat']['id'], txt, reply_to_message_id=msg['message_id'],parse_mode='Markdown')
                        
            
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
    
def lists_overlap(a, b):
    for i in a:
        if i in b:
            return True
        return False