import lang
import botconfig

prefixes = [
	'/'
	]


class Plugin:
	def __init__(self, bot, command='', command_level=0, help_mess=lang.halp['default']):
		self.bot = bot
		self.command = command
		self.command_level = command_level
		self.help_mess = help_mess
		self.user_level = 0

	def execute(self, msg):
		pass

	def help_message(self, msg):
		self.bot.sendMessage(msg['chat']['id'], self.help_mess, parse_mode='Markdown', disable_web_page_preview=True)

	def test_command(self, msg, user_level):
		for prefix in prefixes:
			if msg['text'].startswith(prefix.lower() + self.command):
				if msg['chat']['type'] == 'supergroup':
					admins = self.bot.getChatAdministrators(msg['chat']['id'])
					adminids = [admin['user']['id'] for admin in admins]
					if msg['from']['id'] in adminids:
						user_level = 3
				if user_level >= self.command_level:
					self.user_level = user_level
					self.execute(msg)
				else:
					self.bot.sendMessage(msg['chat']['id'], lang.general['plugin']['level_low'])
		self.test_help(msg)

	def test_help(self, msg):
		if msg['text'] == '/halp ' + self.command or msg['text'] == '/halp' + botconfig.USERNAME:
			self.help_message(msg)

	def inline_callback(self, callback):
		pass