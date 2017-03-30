import config
from plugins.pluginbase import PluginBase

class Rules(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'rules'
        self.command_level = 0
        self.help_mess = config.default_help_mess
    
    def execute(self, msg):
        self.bot.sendMessage(msg['chat']['id'], config.rules)