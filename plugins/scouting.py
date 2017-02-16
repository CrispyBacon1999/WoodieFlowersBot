import config
from plugins.pluginbase import PluginBase
from buttonhandler import Keyboard

from telepot.namedtuple import InlineKeyboardMarkup as IKM
from telepot.namedtuple import InlineKeyboardButton as IKB

check = '✔️️'
cross = '❌'


class Scouting(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'scout'
        self.command_level = 0
        self.help_mess = config.default_help_mess
    
    def execute(self, msg):
        kb = Keyboard(self.bot)
        kb.message = 'Test'
        kb.keyboard = IKM(inline_keyboard = [
            [IKB(text='Drive Train', callback_data='None'),IKB(text=cross, callback_data='driveTrain')],
            [IKB(text='Vision Tracking', callback_data='None'),IKB(text=cross, callback_data='visionTracking')],
            [IKB(text='Type of Shooter', callback_data='None'),IKB(text=cross, callback_data='None')],
            [IKB(text='None', callback_data='None'),IKB(text=cross, callback_data='None')],
            [IKB(text='None', callback_data='None'),IKB(text=cross, callback_data='None')]
        ])
        kb.sendKeyboard(msg['chat']['id'])

class ScoutAdmin(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'scoutadmin'
        self.command_level = 0
        self.help_mess = config.default_help_mess
    
    def execute(self, msg):
        pass