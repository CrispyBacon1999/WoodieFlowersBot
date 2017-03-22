import config
from plugins.pluginbase import PluginBase
import dbhandler


class Request(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'request'
        self.command_level = 0
        self.help_mess = config.request_help_mess
    
    def execute(self, msg):
        if(len(msg['text'].split()) > 1):
            dbhandler.addrequest(msg['from']['id'], ' '.join(msg['text'].split()[1:]))
            self.bot.sendMessage(msg['chat']['id'], 'Sent new request!')
            self.bot.forwardMessage(config.admin_uid, msg['chat']['id'], msg['message_id'], disable_notification=True)
        else:
            self.bot.sendMessage(msg['chat']['id'], 'Input a request after the command!')