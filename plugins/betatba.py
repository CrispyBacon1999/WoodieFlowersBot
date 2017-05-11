import config
from plugins.pluginbase import PluginBase
import tbaapi3 as tba3
from telepot.namedtuple import InlineKeyboardButton as IKB
from telepot.namedtuple import InlineKeyboardMarkup as IKM 
import re
from telepot.exception import TelegramError
from utils import bcolors as col

class Beta(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'beta'
        self.command_level = 0
        self.help_mess = config.default_help_mess
    
    def execute(self, msg):
        # If the message type is a callback, then run message editing
        if msg['entities'][0]['type'] == 'callback':
            chat = self.bot.getChat(msg['chat']['id'])
            if chat['type'] == 'supergroup':
                print(col.OKBLUE + chat['title'] + col.HEADER + ' - ' + col.OKGREEN + msg['from']['first_name'] + ' (%s)' % str(msg['from']['id']) + col.HEADER +' - CALLBACK : ' + col.WARNING + msg['text'] + col.ENDC)
            else:
                print(col.OKGREEN + msg['from']['first_name'] + ' (%s)' % str(msg['from']['id']) + col.HEADER +' - CALLBACK : ' + col.WARNING + msg['text'] + col.ENDC)
            callback = msg['text']
            # Is Team
            if re.search('^team_', callback):
                # Remove irrelevant information
                callback = re.sub('^team_', '', callback)
                teamnum = re.sub('[^0-9]*', '', callback)
                callback = re.sub('_\d+', '', callback)
                team = tba3.Team(teamnum)
                # Create keyboard for the team
                teambuttons = IKM(inline_keyboard = [
                    [IKB(text='Nickname', callback_data='team_nickname_' + team.team_number),IKB(text='Motto', callback_data='team_motto_' + team.team_number),IKB(text='Name', callback_data='team_name_' + team.team_number)],
                    [IKB(text='Rookie Year', callback_data='team_rookie_year_' + team.team_number),IKB(text='Website', callback_data='team_website_' + team.team_number), IKB(text='Champs', callback_data='team_champs_' + team.team_number)],
                    [IKB(text='Address', callback_data='team_address_' + team.team_number),IKB(text='City', callback_data='team_city_' + team.team_number), IKB(text='State', callback_data='team_state_' + team.team_number)],
                    [IKB(text='ZIP Code', callback_data='team_postal_code_' + team.team_number),IKB(text='Country', callback_data='team_country_' + team.team_number), IKB(text='Coords', callback_data='team_coords_' + team.team_number)],
                    [IKB(text='Maps Link', callback_data='team_gmaps_url_' + team.team_number),IKB(text='Loc Name', callback_data='team_location_name_' + team.team_number), IKB(text='Maps ID', callback_data='team_gmaps_place_id_' + team.team_number)]
                ])
                # Ensure that the message isn't being updated to the current value, which throws an error
                try:
                    # If the callback request isn't asking for coordinates, which are calculated seperately from the dictionary, 
                    # send the dictionary value for the callback query
                    if not callback == 'coords':
                        self.bot.editMessageText((msg['chat']['id'], msg['message_id']),'Team ' + team.team_number + '\n\n' + team.data[callback], reply_markup=teambuttons)
                    # If the callback request asks for coordinates, send the team.coords variable instead of the dictionary value
                    else:
                        self.bot.editMessageText((msg['chat']['id'], msg['message_id']),'Team ' + team.team_number + '\n\n' + str(team.coords), reply_markup=teambuttons)
                except TelegramError:
                    pass
            # Is Event
            elif re.search('^event_', callback):
                # Remove irrelevant information
                callback = re.sub('^event_', '', callback)
                eventkey = re.sub('([a-z]*_)*[0-9]*', '', callback)
                callback = re.sub('_[0-9]*[a-z]*$', '', callback)
                event = tba3.Event(eventkey)
                # Create keyboard for the event
                eventbuttons = IKM(inline_keyboard = [
                    [IKB(text='Short Name', callback_data='event_short_name_' + event.key),IKB(text='Week', callback_data='event_week_' + event.key),IKB(text='Name', callback_data='event_name_' + event.key)],
                    [IKB(text='District', callback_data='event_district_' + event.key),IKB(text='Website', callback_data='event_website_' + event.key), IKB(text='Timezone', callback_data='event_timezone_' + event.key)],
                    [IKB(text='Event Code', callback_data='event_event_code_' + event.key),IKB(text='Event Type', callback_data='event_event_type_string_' + event.key), IKB(text='Playoff Type', callback_data='event_playoff_type_string_' + event.key)],
                    [IKB(text='Address', callback_data='event_address_' + event.key),IKB(text='City', callback_data='event_city_' + event.key), IKB(text='State', callback_data='event_state_prov_' + event.key)],
                    [IKB(text='ZIP Code', callback_data='event_postal_code_' + event.key),IKB(text='Country', callback_data='event_country_' + event.key), IKB(text='Coords', callback_data='event_coords_' + event.key)],
                    [IKB(text='Maps Link', callback_data='event_gmaps_url_' + event.key),IKB(text='Loc Name', callback_data='event_location_name_' + event.key), IKB(text='Date', callback_data='event_date_' + event.key)]
                ])
                # Ensure that the message isn't being updated to the current value, which throws an error
                try:
                    # If the callback request asks for coordinates, send the event.coords variable instead of the dictionary value
                    if callback == 'coords':
                        self.bot.editMessageText((msg['chat']['id'], msg['message_id']),'Event: ' + event.short_name + '\n\n' + str(event.coords), reply_markup=eventbuttons)
                    # If the callback request asks for the event dates, send the event.date variable instead of the dictionary value
                    elif callback == 'date':
                        self.bot.editMessageText((msg['chat']['id'], msg['message_id']),'Event: ' + event.short_name + '\n\n' + str(event.date), reply_markup=eventbuttons)
                    # If the callback request isn't asking for coordinates or the dates, which are calculated seperately from the dictionary, 
                    # send the dictionary value for the callback query
                    else:
                        self.bot.editMessageText((msg['chat']['id'], msg['message_id']),'Event: ' + event.short_name + '\n\n' + str(event.data[callback]), reply_markup=eventbuttons)
                except TelegramError:
                    pass
        # If the message type is not a callback, run regular message handling
        else:
            text = msg['text'].split()
            # Check if the parameter passed is a number, meaning it's a team
            if text[1].isdigit():
                team = tba3.Team(text[1])
                # Generate Initial Team Keyboard with Team Number in Callback Data
                teambuttons = IKM(inline_keyboard = [
                    [IKB(text='Nickname', callback_data='team_nickname_' + team.team_number),IKB(text='Motto', callback_data='team_motto_' + team.team_number),IKB(text='Name', callback_data='team_name_' + team.team_number)],
                    [IKB(text='Rookie Year', callback_data='team_rookie_year_' + team.team_number),IKB(text='Website', callback_data='team_website_' + team.team_number), IKB(text='Champs', callback_data='team_home_championship_' + team.team_number)],
                    [IKB(text='Address', callback_data='team_address_' + team.team_number),IKB(text='City', callback_data='team_city_' + team.team_number), IKB(text='State', callback_data='team_state_' + team.team_number)],
                    [IKB(text='ZIP Code', callback_data='team_postal_code_' + team.team_number),IKB(text='Country', callback_data='team_country_' + team.team_number), IKB(text='Coords', callback_data='team_coords_' + team.team_number)],
                    [IKB(text='Maps Link', callback_data='team_gmaps_url_' + team.team_number),IKB(text='Loc Name', callback_data='team_location_name_' + team.team_number), IKB(text='Maps ID', callback_data='team_gmaps_place_id_' + team.team_number)]
                ])
                self.bot.sendMessage(msg['chat']['id'], 'Click button below for team info', reply_markup=teambuttons)
            # Check if the parameter passed is a string, meaning it's an event
            else:
                event = tba3.Event(text[1])
                # Generate Initial Event Keyboard with Event Key in Callback Data
                eventbuttons = IKM(inline_keyboard = [
                    [IKB(text='Short Name', callback_data='event_short_name_' + event.key),IKB(text='Week', callback_data='event_week_' + event.key),IKB(text='Name', callback_data='event_name_' + event.key)],
                    [IKB(text='District', callback_data='event_district_' + event.key),IKB(text='Website', callback_data='event_website_' + event.key), IKB(text='Timezone', callback_data='event_timezone_' + event.key)],
                    [IKB(text='Event Code', callback_data='event_event_code_' + event.key),IKB(text='Event Type', callback_data='event_event_type_string_' + event.key), IKB(text='Playoff Type', callback_data='event_playoff_type_string_' + event.key)],
                    [IKB(text='Address', callback_data='event_address_' + event.key),IKB(text='City', callback_data='event_city_' + event.key), IKB(text='State', callback_data='event_state_prov_' + event.key)],
                    [IKB(text='ZIP Code', callback_data='event_postal_code_' + event.key),IKB(text='Country', callback_data='event_country_' + event.key), IKB(text='Coords', callback_data='event_coords_' + event.key)],
                    [IKB(text='Maps Link', callback_data='event_gmaps_url_' + event.key),IKB(text='Loc Name', callback_data='event_location_name_' + event.key), IKB(text='Date', callback_data='event_date_' + event.key)]
                ])
                self.bot.sendMessage(msg['chat']['id'], 'Click button below for event info', reply_markup=eventbuttons)