import lang
from plugins import plugin
import re
import dbhandler
import sys
import json
import logger


class User(plugin.Plugin):
    def __init__(self, bot):
        self.lng = lang.user
        plugin.Plugin.__init__(self, bot, command='user', help_mess=self.lng['help'])

    def execute(self, msg):
        if msg['entities'][0]['type'] == 'callback':
            logger.log_callback(msg)
            callback = msg['text']
            callback = re.sub('^user_', '', callback)
            username = re.sub('[a-z]+_', '', callback, 1)
            callback = re.sub('_[A-z]+', '', callback)

            keyboard = json.dumps({'inline_keyboard': [
                [
                    {'text': 'Team Number', 'callback_data': 'user_team_' + username}],[
                    {'text': 'Github', 'callback_data': 'user_github_' + username},
                    {'text': 'Reddit', 'callback_data': 'user_reddit_' + username}
                ]
            ]})

            if callback == 'team':
                try:
                    userid_from_uname = dbhandler.getuid(username)[0]
                    member_team = dbhandler.getmemberteam(userid_from_uname)[0]
                    member_name = self.bot.getChatMember(msg['chat']['id'], userid_from_uname)['user']['first_name']
                    self.bot.editMessageText(self.lng['team']['message'] % (member_name, member_team),
                                             chat_id=msg['chat']['id'], message_id=msg['message_id'],
                                             reply_markup=keyboard)
                except:
                    
                    self.bot.editMessageText(self.lng['team']['error'],
                                             chat_id=msg['chat']['id'], message_id=msg['message_id'],
                                             reply_markup=keyboard)
            if callback == 'github':
                user_id = dbhandler.getuid(username)[0]
                ghusername = dbhandler.getuser_info(user_id, 'github')[0]
                if ghusername:
                    self.bot.editMessageText(self.lng['github']['message'] % ghusername,
                                             chat_id=msg['chat']['id'], message_id=msg['message_id'],
                                             reply_markup=keyboard)
                else:
                    self.bot.editMessageText(self.lng['github']['error'],
                                             chat_id=msg['chat']['id'], message_id=msg['message_id'],
                                             reply_markup=keyboard)
            if callback == 'reddit':
                user_id = dbhandler.getuid(username)[0]
                redusername = dbhandler.getuser_info(user_id, 'reddit')[0]
                if redusername:
                    self.bot.editMessageText(self.lng['reddit']['message'] % redusername,
                                             chat_id=msg['chat']['id'], message_id=msg['message_id'],
                                             reply_markup=keyboard)
                else:
                    self.bot.editMessageText(self.lng['reddit']['error'],
                                             chat_id=msg['chat']['id'], message_id=msg['message_id'],
                                             reply_markup=keyboard)
        else:
            text = msg['text']
            # If Variable is username
            if re.search('@?[A-z]{5,}', text.split()[1]):
                username = re.sub('@', '', text.split()[1])
                keyboard = json.dumps({'inline_keyboard': [
                    [
                        {'text': 'Team Number', 'callback_data': 'user_team_' + username}], [
                        {'text': 'Github', 'callback_data': 'user_github_' + username},
                        {'text': 'Reddit', 'callback_data': 'user_reddit_' + username}
                    ]
                ]})
                self.bot.sendMessage(msg['chat']['id'], self.lng['keyboard'], reply_markup=keyboard)


class Set(plugin.Plugin):
    def __init__(self, bot):
        self.lng = lang.set
        plugin.Plugin.__init__(self, bot, command='set', help_mess=self.lng['help'])

    def execute(self, msg):
        text = msg['text']
        # Set Team Number
        if re.search('^[0-9]{1,4}$', text.split()[1]):
            number = int(text.split()[1])
            dbhandler.addUser(msg['from']['id'], number)
            if number == dbhandler.getmemberteam(msg['from']['id'])[0]:
                self.bot.sendMessage(msg['chat']['id'], self.lng['team']['success'] % number)
            else:
                self.bot.sendMessage(msg['chat']['id'], self.lng['team']['error'])
        # Set Github Username
        if re.search('(git|gh|github|ghub):([A-z]|[0-9]|-)+', text.split()[1], flags=re.IGNORECASE):
            username = text.split()[1].split(':')[-1]
            dbhandler.adduser_info(msg['from']['id'], username, 'github')
            if username == dbhandler.getuser_info(msg['from']['id'], 'github')[0]:
                self.bot.sendMessage(msg['chat']['id'], self.lng['github']['success'] % username)
            else:
                self.bot.sendMessage(msg['chat']['id'], self.lng['github']['error'])
        if re.search('(reddit|r|red|rdit):([A-z]|[0-9]|-)+', text.split()[1], flags=re.IGNORECASE):
            username = text.split()[1].split(':')[-1]
            dbhandler.adduser_info(msg['from']['id'], username, 'reddit')
            if username == dbhandler.getuser_info(msg['from']['id'], 'reddit')[0]:
                self.bot.sendMessage(msg['chat']['id'], self.lng['reddit']['success'] % username)
            else:
                self.bot.sendMessage(msg['chat']['id'], self.lng['reddit']['error'])
