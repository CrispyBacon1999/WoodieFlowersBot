import config
from plugins.pluginbase import PluginBase
class Kick(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'kick'
        self.command_level = 0
        self.help_mess = config.kick_help_mess
    
    def execute(self, msg):
        print(msg)
        user = self.bot.getChatMember(msg['chat']['id'], msg['from']['id'])
        if(user['status'] == 'administrator' or user['status'] == 'creator'):
            if(msg['reply_to_message']):
                replied_message = msg['reply_to_message']
                kick_uid = replied_message['from']['id']
                self.bot.kickChatMember(msg['chat']['id'], kick_uid)
                self.bot.unbanChatMember(msg['chat']['id'], kick_uid)
                if(len(msg.split()) == 1):
                    self.bot.sendMessage(msg['chat']['id'], '%s has been kicked!' % replied_message['from']['first_name'])
                else:
                    self.bot.sendMessage(msg['chat']['id'], '%s has been kicked for %s!' % (replied_message['from']['first_name'], msg.split()[:1]))
            else:
                self.bot.sendMessage(msg['chat']['id'], 'Reply to a user!')