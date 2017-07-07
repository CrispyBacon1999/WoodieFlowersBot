from plugins import plugin
import lang
import botconfig



class Info(plugin.Plugin):

    def __init__(self, bot):
        self.lng = lang.info
        plugin.Plugin.__init__(self, bot, command='info')

    def execute(self, msg):
        self.bot.sendMessage(msg['chat']['id'], self.lng['information'] % (botconfig.VERSION, botconfig.USERNAME),
         parse_mode='Markdown', disable_web_page_preview=True)
