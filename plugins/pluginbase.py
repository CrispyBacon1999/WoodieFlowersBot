import config



prefixes = [
    '@FRCGlobalBot, ',
    'woodie, ',
    'woodie ',
    'hey woodie ',
    'hey woodie, '
]

class PluginBase:
    def __init__(self, bot):
        self.bot = bot
        self.command = ''
        self.command_level = 0
        self.help_mess = config.default_help_mess
    
    def execute(self, msg, natlang=False):
        pass
    
    def help_message(self, msg):
        self.bot.sendMessage(msg['chat']['id'], self.help_mess, parse_mode='Markdown', disable_web_page_preview=True)
    
    def test_command(self, user_level, msg):
        txt = msg['text'].split()[0]
        if txt == '/' + self.command or txt == '/' + self.command + '@FRCGlobalAdminBot':
            if user_level >= self.command_level:
                self.execute(msg)
        self.test_help(msg)
                
    def test_help(self, msg):
        txt = msg['text']
        if txt == '/halp ' + self.command:
            self.help_message(msg)
        if txt == '/halp@FRCGlobalAdminBot ' + self.command:
            self.help_message(msg)
            