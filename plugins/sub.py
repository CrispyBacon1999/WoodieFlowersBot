import config
from plugins.pluginbase import PluginBase
import re
class Sub(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'sub'
        self.command_level = 0
        self.help_mess = config.default_help_mess
    
    def execute(self, msg):
        text = msg['text'].split()
        if len(text) > 2:
            if(msg['reply_to_message']):
                regex = text[1]
                replace = ' '.join(text[2:])
                txt = re.sub(regex, replace, msg['reply_to_message']['text'])
                print(txt)
                self.bot.sendMessage(msg['chat']['id'], '*FTFY*\n\n%s' % txt, parse_mode="Markdown")
            self.bot.sendMessage(msg['chat']['id'], 'Reply to a message first!', parse_mode='Markdown')
        else:
            self.bot.sendMessage(msg['chat']['id'], 'Use the syntax /sub _regex substitution_', parse_mode='Markdown')