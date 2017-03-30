import config
from plugins.pluginbase import PluginBase

class About(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'about'
        self.command_level = 0
        self.help_mess = config.default_help_mess
    
    def execute(self, msg):
        self.bot.sendMessage(msg['chat']['id'], config.about, parse_mode="Markdown", disable_web_page_preview=True)