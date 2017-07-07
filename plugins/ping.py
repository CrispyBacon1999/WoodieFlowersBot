from plugins import plugin
import lang



class Ping(plugin.Plugin):

    def __init__(self, bot):
        self.lng = lang.ping
        plugin.Plugin.__init__(self, bot, command='ping')

    def execute(self, msg):
        self.bot.sendMessage(msg['chat']['id'], self.lng['pong'])
