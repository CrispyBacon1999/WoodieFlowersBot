import config
from plugins.pluginbase import PluginBase

class Rank(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'rank'
        self.command_level = 0
        self.help_mess = config.rank_help_mess
    
    def execute(self, msg):
        pass