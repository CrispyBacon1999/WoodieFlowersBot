import lang
from plugins import plugin
import re
import logger as l
import botconfig
import dbhandler
import json

class Admin(plugin.Plugin):
	def __init__(self, bot):
		self.lng = lang.admin
		plugin.Plugin.__init__(self, bot, command='admin', help_mess=self.lng['help'], command_level=3)

	def execute(self, msg):
		if msg['entities'][0]['type'] == 'callback':
			#try:
			admins = self.bot.getChatAdministrators(msg['chat']['id'])
			adminids = [admin['user']['id'] for admin in admins]
			if msg['from']['id'] in adminids:
				user_level = 3
			if user_level >= 3:
				text = re.sub('^[a-z]+_', '', msg['text'])
				l.temp_log(text)
				if text != 'done':
					command = re.sub('(_-?[0-9]+){2}', '', text)
					user = re.sub('_[0-9]+$', '', re.sub('^[a-z]+_', '', text))
					chat = re.sub('[a-z]+_[0-9]+_', '', text)
					if command == 'kick':
						self._kick(chat, user)
						self.bot.deleteMessage(msg['chat']['id'], msg['message_id'])
					if command == 'ban':
						self._ban(chat, user)
						self.bot.deleteMessage(msg['chat']['id'], msg['message_id'])
					if command == 'warnadd':
						self._warn(chat, user, 1)
						self.bot.deleteMessage(msg['chat']['id'], msg['message_id'])
					if command == 'warnsub':
						self._warn(chat, user, -1)
						self.bot.deleteMessage(msg['chat']['id'], msg['message_id'])
				else:
					self.bot.deleteMessage(msg['chat']['id'], msg['message_id'])
			else:
				self.bot.answerCallbackQuery(msg['callback_id'], text=self.lng['admin_only'])
			#except:
		#		self.bot.answerCallbackQuery(msg['callback_id'], text=self.lng['unknown_error'])
		else:
			chat_id = msg['chat']['id']
			try:
				replied_user = msg['reply_to_message']['from']['id']
				adminkeyboard = json.dumps({'inline_keyboard':[
							[{'text': 'Kick', 'callback_data': 'admin_kick_%s_%s' % (str(replied_user), str(chat_id))},
							 {'text': 'Ban', 'callback_data': 'admin_ban_%s_%s' % (str(replied_user), str(chat_id))}],
							 [{'text': '+ Warn', 'callback_data': 'admin_warnadd_%s_%s' % (str(replied_user), str(chat_id))}, 
							 {'text': '- Warn', 'callback_data': 'admin_warnsub_%s_%s' % (str(replied_user), str(chat_id))}],
							[{'text': 'Done', 'callback_data': 'admin_done'}]
						]})
				self.bot.sendMessage(chat_id, self.lng['keyboard'], reply_to_message_id=msg['reply_to_message']['message_id'], reply_markup=adminkeyboard)
			except KeyError:
				self.bot.sendMessage(chat_id, self.lng['no_reply'])
				
				
	def _kick(self, chat_id, user):
		name = self.bot.getChatMember(chat_id, user)['user']['first_name']
		self.bot.kickChatMember(chat_id, user)
		self.bot.unbanChatMember(chat_id, user)
		self.bot.sendMessage(chat_id, self.lng['kick'] % name)
		
	def _ban(self, chat_id, user):
		name = self.bot.getChatMember(chat_id, user)['user']['first_name']
		self.bot.kickChatMember(chat_id, user)
		self.bot.sendMessage(chat_id, self.lng['ban'] % name)
	
	
	def _warn(self, chat_id, user, warns):
		name = self.bot.getChatMember(chat_id, user)['user']['first_name']
		current_warns = dbhandler.getwarns(user)
		dbhandler.warn(user, current_warns + warns)
		current_warns = dbhandler.getwarns(user)
		self.bot.sendMessage(chat_id, self.lng['warn'] % (name, current_warns, botconfig.maxwarns))
		if(botconfig.banwarns > current_warns >= botconfig.maxwarns):
			self.bot.kickChatMember(chat_id, user)
			self.bot.sendMessage(chat_id, self.lng['kick'] % name)
			self.bot.unbanChatMember(chat_id, user)
		elif(botconfig.banwarns <= current_warns):
			self.bot.kickChatMember(chat_id, user)
			self.bot.sendMessage(chat_id, self.lng['ban'] % name)
			