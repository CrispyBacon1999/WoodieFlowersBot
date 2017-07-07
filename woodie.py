from vyper import vyper
from plugins import betatba, user, admin
import botconfig
import time
import dbhandler
import logger as l
import re
from plugins import xp


def init():
	l.init_log('Initializing Plugins')
	for plugin in botconfig.plugins:
		if callable(init):
			l.init_log('Initializing plugin: %s' % plugin.command)
			plugin.init()
	botconfig.init_plugins(bot)
	pluginnames = [plugin.__class__.__name__ for plugin in botconfig.plugins]
	for plugin in pluginnames:
		l.init_log(plugin + ': INITIALIZED')
	botconfig.USERNAME = '@' + bot.getMe()['username']


def chat(msg):
	if 'text' in msg['message']:
		l.log(msg['message'])
		if 'username' in msg['message']['from']:
		  dbhandler.refreshuser_id(msg['message']['from']['username'], msg['message']['from']['id'])
		#xp.add_xp(msg['message']['from']['id'])
		for plugin in botconfig.plugins:
			plugin.test_command(msg['message'], 0)


def inline_button(msg):
	msg = msg['callback_query']
	match = re.search('^(team|event)_', msg['data'])
	if match:
		for plugin in botconfig.plugins:
			if isinstance(plugin, betatba.Tba):
				message = {
					'text': msg['data'],
					'entities': [
						{'type': 'callback'}],
					'chat': {
						'id': msg['message']['chat']['id'],
						'type': msg['message']['chat']['type']
					},
					'message_id': msg['message']['message_id'],
					'from': {
						'first_name': msg['from']['first_name'],
						'id': msg['from']['id']
					},
					'callback_id': msg['id']
				}
				plugin.execute(message)
	match = re.search('^user_', msg['data'])
	if match:
		for plugin in botconfig.plugins:
			if isinstance(plugin, user.User):
				message = {
					'text': msg['data'],
					'entities': [
						{'type': 'callback'}],
					'chat': {
						'id': msg['message']['chat']['id'],
						'type': msg['message']['chat']['type']
					},
					'message_id': msg['message']['message_id'],
					'from': {
						'first_name': msg['from']['first_name'],
						'id': msg['from']['id']
					}
				}
				plugin.execute(message)
	match = re.search('^admin_', msg['data'])
	if match:
		for plugin in botconfig.plugins:
			if isinstance(plugin, admin.Admin):
				message = {
					'text': msg['data'],
					'entities': [
						{'type': 'callback'}],
					'chat': {
						'id': msg['message']['chat']['id'],
						'type': msg['message']['chat']['type']
					},
					'message_id': msg['message']['message_id'],
					'from': {
						'first_name': msg['from']['first_name'],
						'id': msg['from']['id']
					}
				}
				plugin.execute(message)
			
			
			
			
l.init_log(botconfig.logo)
l.init_log('	  ---	Starting Woodie Flowers Bot - %s   ---' % botconfig.VERSION)
l.init_log('Connecting to Telegram Servers with Bot Token...')
bot = vyper.API().configure(botconfig.TOKEN, functions={'message': chat,
														'callback_query': inline_button})
init()
l.init_log('Connected to Telegram Servers!')
l.init_log('Starting webhook loop to receive new messages.')
while True:
	bot.getUpdates()
	time.sleep(.05)
