import telepot
from telepot.namedtuple import InlineKeyboardMarkup as IKM
from telepot.namedtuple import InlineKeyboardButton as IKB

class Keyboard():
    def __init__(self, bot):
        self.bot = bot
        self.message = ''
        self.keyboard = None
        
    def sendKeyboard(self,chatid):
        self.bot.sendMessage(chatid, self.message, reply_markup = self.keyboard)
    
    def recieveInput(self, msg):
        pass
    
    def updateButton(self, msg):
        pass
