import config
from plugins.pluginbase import PluginBase

class Best(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = '1369best'
        self.command_level = 0
        self.help_mess = config.minitaur_best_help_mess
    
    def execute(self, msg):
        self.bot.sendMessage(msg['chat']['id'], '/1369best')