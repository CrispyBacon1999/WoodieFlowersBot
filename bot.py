import telepot
import time
from plugins import team,tba,meetup,scouting
import sys
from utils import bcolors as col


# Handle Messages
def handle(msg):
    content_type = telepot.glance(msg, long=True)
    chatid = msg['chat']['id']
    textfull = msg['text']
    uid = msg['from']['id']
    chat = bot.getChat(chatid)
    if chat['type'] == 'supergroup':
        print(col.OKBLUE + chat['title'] + col.HEADER + ' - ' + col.OKGREEN + msg['from']['first_name'] + ' (%s)' % str(msg['from']['id']) + col.HEADER +' : ' + col.WARNING + textfull + col.ENDC)
    else:
        print(col.OKGREEN + msg['from']['first_name'] + ' (%s)' % str(msg['from']['id']) + col.HEADER +' : ' + col.WARNING + textfull + col.ENDC)
    for plugin in plugins:
        plugin.test_command(0,msg)
# Handle Inline Buttons
def on_callback_query(msg):
    pass
# Handle New Chat Members
def new_chat_member(msg):
    pass
# Handle Leaving Chat Members
def left_chat_member(msg):
    pass
msgprefix = '/'
print(col.HEADER + 'Initializing Bot...')
TOKEN = sys.argv[1]
bot = telepot.Bot(TOKEN)
L = []
bot.message_loop({'chat': handle,
                  'callback_query': on_callback_query,
                  'new_chat_member': new_chat_member,
                  'left_chat_member': left_chat_member,
                  'edited_chat': handle})
print(col.HEADER + 'Initializing plugins...')
# Empty Plugins List
plugins = []
# Add Plugins to list
plugins.append(team.Team(bot))
plugins.append(tba.Tba(bot))
plugins.append(meetup.Meetups(bot))
plugins.append(scouting.Scouting(bot))
plugins.append(scouting.ScoutAdmin(bot))
print(col.HEADER + 'Plugins Initialized. Waiting for messages...')
while 1:
    time.sleep(5)