import config
import dbhandler
from plugins.pluginbase import PluginBase

class Bind(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'bind'
        self.command_level = 0
        self.help_mess = config.default_help_mess
    
    def execute(self, msg):
        text = msg['text'].split()
        if(len(text) > 1):
            if(msg['reply_to_message']):
                if(msg['reply_to_message']['sticker']):
                    sticker = msg['reply_to_message']['sticker']['file_id']
                    command = ' '.join(text[1:])
                    dbhandler.addbind(sticker, command)