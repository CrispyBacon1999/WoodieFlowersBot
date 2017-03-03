import telepot
from telepot.namedtuple import InputTextMessageContent as ITMC
import time
from plugins import team,tba,meetup,scouting,configure,rank
from theblueallianceapi import Team as tm
import sys
from utils import bcolors as col
import dbhandler


# Handle Messages
def handle(msg):
    content_type = telepot.glance(msg, long=True)
    chatid = msg['chat']['id']
    if(content_type[0] == 'text'): 
        textfull = msg['text']
    elif(content_type[0] == 'sticker'):
        print(msg['sticker']['file_id'])
    uid = msg['from']['id']
    chat = bot.getChat(chatid)
    dbhandler.refreshuid(msg['from']['username'],uid)
    if(int(uid) == 248754302):
        user_level = 1
    else:
        user_level = 0
    if content_type[0] == 'text':
        if chat['type'] == 'supergroup':
            print(col.OKBLUE + chat['title'] + col.HEADER + ' - ' + col.OKGREEN + msg['from']['first_name'] + ' (%s)' % str(msg['from']['id']) + col.HEADER +' : ' + col.WARNING + textfull + col.ENDC)
        else:
            print(col.OKGREEN + msg['from']['first_name'] + ' (%s)' % str(msg['from']['id']) + col.HEADER +' : ' + col.WARNING + textfull + col.ENDC)
        if textfull == '/halp' or textfull == '/halp@FRCGlobalAdminBot':
            bot.sendMessage(chat, '```Try using /halp <plugin> instead!```', parse_mode = 'Markdown')
    elif content_type[0] == 'sticker':
        try:
            sticker_team = list(stickers.keys())[list(stickers.values()).index(msg['sticker']['file_id'])]
            teamtext = '/tba team info %s'%(sticker_team)
            msg = {
                'from': msg['from'],
                'chat': msg['chat'],
                'message_id': msg['message_id'],
                'date': msg['date'],
                'text': teamtext
            }
            content_type[0] == 'text'
        except ValueError:
            msg = {
            'from': msg['from'],
            'chat': msg['chat'],
            'message_id': msg['message_id'],
            'date': msg['date'],
            'text': 'None'
        }
        if chat['type'] == 'supergroup':
            print(col.OKBLUE + chat['title'] + col.HEADER + ' - ' + col.OKGREEN + msg['from']['first_name'] + ' (%s)' % str(msg['from']['id']) + col.HEADER +' : ' + col.WARNING + 'STICKER - ' + msg['text'] + col.ENDC)
        else:
            print(col.OKGREEN + msg['from']['first_name'] + ' (%s)' % str(msg['from']['id']) + col.HEADER +' : ' + col.WARNING + 'STICKER - ' + msg['text']  + col.ENDC)
    if content_type[0] == 'text':
        for plugin in plugins:
            plugin.test_command(user_level,msg)
# Handle Inline Buttons
def on_callback_query(msg):
    pass
# Handle New Chat Members
def new_chat_member(msg):
    pass
# Handle Leaving Chat Members
def left_chat_member(msg):
    pass
# Handle Inline Messages
def inline(msg):
    try:
        team = tm(msg['query'])
        inline_response = {
            'type': 'article',
            'id': msg['query'],
            'title': 'Information for %s' % team.info['name'],
            'input_message_content':{
                'message_text':'*Information for Team %s:*\n\n*Name:* _%s_\n*Location:* _%s_\n*Motto:* _%s_\n*Website:* _%s_\n*Rookie Year:* _%s_' % (msg['query'], team.info['name'],team.info['location'],team.info['motto'],team.info['website'],team.info['rookie_year']),
                'parse_mode':'Markdown'
            }
        }
        bot.answerInlineQuery(msg['id'], [inline_response])
    except ValueError:
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
                  'edited_chat': handle,
                  'inline_query': inline
})
print(col.HEADER + 'Initializing plugins...' + col.ENDC)
# Empty Plugins List
plugins = []
# Add Plugins to list
plugins.append(team.Team(bot))
plugins.append(tba.Tba(bot))
plugins.append(meetup.Meetups(bot))
plugins.append(scouting.Scouting(bot))
plugins.append(scouting.ScoutAdmin(bot))
plugins.append(configure.Configure(bot))
plugins.append(rank.Rank(bot))
print(col.HEADER + 'Plugins Initialized. Waiting for messages...' + col.ENDC)

stickers = {
    "16": "CAADAQADUwAD5iCCDKPhTPDqPdQ2Ag",
    "254": "CAADAQADVAAD5iCCDD4TcyqYIbGZAg",
    "330": "CAADAQADUQAD5iCCDF7rY0z6h5PuAg",
    "118": "CAADAQADUgAD5iCCDDfc7QuUrVj9Ag",
    "148": "CAADAQADVQAD5iCCDDd6Fcy6_fZgAg",
    "1678": "CAADAQADVgAD5iCCDMQowZXust45Ag",
    "67": "CAADAQADVwAD5iCCDJxAY11c6iGiAg",
    "27": "CAADAQADWAAD5iCCDBhdwlWwYWi3Ag",
    "2056": "CAADAQADWQAD5iCCDDo9gVNDaj1mAg",
    "33": "CAADAQADWgAD5iCCDPfEQGCbgkgRAg",
    "2522": "CAADAQADWwAD5iCCDAEdRMDDkSJ-Ag",
    "2337": "CAADAQADXAAD5iCCDAhXdj4tPRTrAg"
    
}
while 1:
    time.sleep(5)