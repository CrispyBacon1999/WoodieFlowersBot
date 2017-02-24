from plugins.pluginbase import PluginBase
from theblueallianceapi import *
import config

class Tba(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'tba'
        self.command_level = 0
        self.help_mess = '*Help For *[The Blue Alliance](http://thebluealliance.com/)\n`/tba team name|location|school|website|rookie_year|motto XXXX YYYY\n\n/tba event name|location|address|website|start_date|stream event_code YYYY\n\n/tba district district_code YYYY`\n\n_Coming soon: Match Data\n\nYYYY is optional_'
    def execute(self, msg):
        text = msg['text'].split()
        if len(text) >= 4:
            if text[1] == 'team':
                if len(text) < 5:
                    team = Team(text[3], None)
                else:
                    team = Team(text[3], text[4])
                if(text[2] == 'info'):
                    info = '*Information for Team %s:*\n\n*Name:* _%s_\n*Location:* _%s_\n*Motto:* _%s_\n*Website:* _%s_\n*Rookie Year:* _%s_' % (text[3], team.info['name'],team.info['location'],team.info['motto'],team.info['website'],team.info['rookie_year'])
                    self.bot.sendMessage(msg['chat']['id'], info, parse_mode='Markdown', disable_web_page_preview=True)
                else:
                    self.bot.sendMessage(msg['chat']['id'], team.info[text[2]], parse_mode='Markdown')
            if text[1] == 'event':
                event = Event(str(text[4]),str(text[3]))
                self.bot.sendMessage(msg['chat']['id'], event.info[text[2]], parse_mode='Markdown')
            if text[1] == 'district':
                district = District(str(text[2]), str(text[3]))
                self.bot.sendMessage(msg['chat']['id'], district.info['eventcodes'], parse_mode='Markdown')