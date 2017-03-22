import config
from plugins.pluginbase import PluginBase
import dbhandler
class Warn(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'warn'
        self.command_level = 0
        self.help_mess = config.warn_help_mess
    
    def execute(self, msg):
        user = self.bot.getChatMember(msg['chat']['id'], msg['from']['id'])
        if(user['status'] == 'administrator' or user['status'] == 'creator'):
            if(msg['reply_to_message']):
                replied_message = msg['reply_to_message']
                kick_uid = replied_message['from']['id']
                current_warns = dbhandler.getwarns(kick_uid)
                try:
                    numwarn = int(msg['text'].split()[1])
                except:
                    numwarn = 1
                dbhandler.warn(kick_uid, current_warns + numwarn)
                current_warns = dbhandler.getwarns(kick_uid)
                self.bot.sendMessage(msg['chat']['id'], '%s now have %d warns! If you get %d, you will get kicked!' % (replied_message['from']['first_name'],current_warns, config.maxwarns))
                if(config.banwarns > current_warns >= config.maxwarns):
                    self.bot.kickChatMember(msg['chat']['id'], kick_uid)
                    self.bot.sendMessage(msg['chat']['id'], '%s has been kicked!' % replied_message['from']['first_name'])
                    self.bot.unbanChatMember(msg['chat']['id'], kick_uid)
                elif(config.banwarns <= current_warns):
                    self.bot.kickChatMember(msg['chat']['id'], kick_uid)
                    self.bot.sendMessage(msg['chat']['id'], '%s has been banned!' % replied_message['from']['first_name'])
            else:
                self.bot.sendMessage(msg['chat']['id'], 'Reply to a user!')
        else:
            self.bot.sendMessage(msg['chat']['id'], 'You must be an administrator to use this command!')