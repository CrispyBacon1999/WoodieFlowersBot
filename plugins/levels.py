from plugins import plugin
import lang
import botconfig



class Levels(plugin.Plugin):

    def __init__(self, bot):
        self.lng = lang.levels
        plugin.Plugin.__init__(self, bot, command='level')

    def execute(self, msg):
        self.bot.sendMessage(msg['chat']['id'], self.lng['level'] % botconfig.userlevels[self.user_level], reply_to_message_id=msg['message_id'])
