import telepot
import botconfig
import time
import logger as l


def init():
    l.init_log('Initializing Plugins')
    for plugin in botconfig.plugins:
        if callable(init):
            l.init_log('Initializing plugin: %s' % plugin.command)
            plugin.init()


def chat(msg):
    l.log(msg)


def inline_button(msg):
    pass
l.init_log('Starting Woodie Flowers - %s...' % botconfig.VERSION)
init()
l.init_log('Connecting to Telegram Servers with Bot Token...')
bot = telepot.Bot(botconfig.TOKEN)
l.init_log('Connected to Telegram Servers!')
l.init_log('Starting webhook loop to receive new messages.')
bot.message_loop({
    'chat': chat,
    'callback_query': inline_button
})
while True:
    time.sleep(5)
