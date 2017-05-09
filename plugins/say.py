import config
import dbhandler
from plugins.pluginbase import PluginBase

class Say(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'say'
        self.command_level = 0
        self.help_mess = config.default_help_mess
    
    def execute(self, msg):
        text = msg['text'].split()
        if(len(text) > 1):
            message = ' '.join(text[1:])
            print(message)
            self.bot.sendMessage(msg['chat']['id'], message)