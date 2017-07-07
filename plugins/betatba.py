import lang
from plugins import plugin
import tbaapi3 as tba3
import re
import logger
import json

class Tba(plugin.Plugin):
    def __init__(self, bot):
        self.lng = lang.tba
        plugin.Plugin.__init__(self, bot, command='tba', help_mess=self.lng['help'])

    def execute(self, msg):
        # If the message type is a callback, then run message editing
        if msg['entities'][0]['type'] == 'callback':
            logger.log_callback(msg)
            callback = msg['text']
            # Is Team
            if re.search('^team_', callback):
                # Remove irrelevant information
                callback = re.sub('^team_', '', callback)
                teamnum = re.sub('[^0-9]*', '', callback)
                callback = re.sub('_\d+', '', callback)
                team = tba3.Team(teamnum)
                # Create keyboard for the team
                teambuttons = json.dumps({'inline_keyboard':[
                    [{'text': 'Nickname', 'callback_data': 'team_nickname_' + team.team_number},
                     {'text': 'Motto', 'callback_data': 'team_motto_' + team.team_number},
                     {'text': 'Name', 'callback_data': 'team_name_' + team.team_number}],
                    [{'text': 'Rookie Year', 'callback_data': 'team_rookie_year_' + team.team_number},
                     {'text': 'Website', 'callback_data': 'team_website_' + team.team_number},
                     {'text': 'Champs', 'callback_data': 'team_home_championship_' + team.team_number}],
                    [{'text': 'Address', 'callback_data': 'team_address_' + team.team_number},
                     {'text': 'City', 'callback_data': 'team_city_' + team.team_number},
                     {'text': 'State', 'callback_data': 'team_state_prov_' + team.team_number}],
                    [{'text': 'ZIP Code', 'callback_data': 'team_postal_code_' + team.team_number},
                     {'text': 'Country', 'callback_data': 'team_country_' + team.team_number},
                     {'text': 'Coords', 'callback_data': 'team_coords_' + team.team_number}],
                    [{'text': 'Maps Link', 'callback_data': 'team_gmaps_url_' + team.team_number},
                     {'text': 'Loc Name', 'callback_data': 'team_location_name_' + team.team_number},
                     {'text': 'Maps ID', 'callback_data': 'team_gmaps_place_id_' + team.team_number}]
                ]})
                try:
                    # If the callback request isn't asking for coordinates, which are calculated seperately from the dictionary,
                    # send the dictionary value for the callback query
                    if not callback == 'coords':
                        self.bot.editMessageText(self.lng['team']['standard'] % (team.team_number, team.data[callback]),
                                                 chat_id=msg['chat']['id'], message_id=msg['message_id'],
                                                 reply_markup=teambuttons)
                    # If the callback request asks for coordinates, send the team.coords variable instead of the dictionary value
                    else:
                        self.bot.editMessageText(self.lng['team']['standard'] % (team.team_number, str(team.coords)),
                                                 chat_id=msg['chat']['id'], message_id=msg['message_id'],
                                                 reply_markup=teambuttons)
                except:
                    pass
            # Is Event
            elif re.search('^event_', callback):
                # Remove irrelevant information
                callback = re.sub('^event_', '', callback)
                eventkey = re.sub('([a-z]*_)*[0-9]*', '', callback)
                callback = re.sub('_[0-9]*[a-z]*$', '', callback)
                event = tba3.Event(eventkey)
                # Create keyboard for the event
                eventbuttons = json.dumps({'inline_keyboard':[
                    [
                        {'text': 'Short Name', 'callback_data': 'event_short_name_' + event.key},
                        {'text': 'Week', 'callback_data': 'event_week_' + event.key},
                        {'text': 'Name', 'callback_data': 'event_name_' + event.key}],
                    [
                        {'text': 'District', 'callback_data': 'event_district_' + event.key},
                        {'text': 'Website', 'callback_data': 'event_website_' + event.key},
                        {'text': 'Timezone', 'callback_data': 'event_timezone_' + event.key}],
                    [
                        {'text': 'Event Code', 'callback_data': 'event_event_code_' + event.key},
                        {'text': 'Event Type', 'callback_data': 'event_event_type_string_' + event.key},
                        {'text': 'Playoff Type', 'callback_data': 'event_playoff_type_string_' + event.key}],
                    [
                        {'text': 'Address', 'callback_data': 'event_address_' + event.key},
                        {'text': 'City', 'callback_data': 'event_city_' + event.key},
                        {'text': 'State', 'callback_data': 'event_state_prov_' + event.key}],
                    [
                        {'text': 'ZIP Code', 'callback_data': 'event_postal_code_' + event.key},
                        {'text': 'Country', 'callback_data': 'event_country_' + event.key},
                        {'text': 'Coords', 'callback_data': 'event_coords_' + event.key}],
                    [
                        {'text': 'Maps Link', 'callback_data': 'event_gmaps_url_' + event.key},
                        {'text': 'Loc Name', 'callback_data': 'event_location_name_' + event.key},
                        {'text': 'Date', 'callback_data': 'event_date_' + event.key}]
                ]})
                # Ensure that the message isn't being updated to the current value, which throws an error
                try:
                    # If the callback request asks for coordinates, send the event.coords variable instead of the dictionary value
                    if callback == 'coords':
                        self.bot.editMessageText(self.lng['event']['standard'] % (event.short_name, str(event.coords)),
                                                 chat_id=msg['chat']['id'], message_id=msg['message_id'],
                                                 reply_markup=eventbuttons)
                    # If the callback request asks for the event dates, send the event.date variable instead of the dictionary value
                    elif callback == 'date':
                        self.bot.editMessageText(self.lng['event']['standard'] % (event.short_name, str(event.date)),
                                                 chat_id=msg['chat']['id'], message_id=msg['message_id'],
                                                 reply_markup=eventbuttons)
                    # If the callback request isn't asking for coordinates or the dates, which are calculated seperately from the dictionary,
                    # send the dictionary value for the callback query
                    else:
                        self.bot.editMessageText(self.lng['event']['standard'] % (event.short_name, event.data[callback]),
                                                 chat_id=msg['chat']['id'], message_id=msg['message_id'],
                                                 reply_markup=eventbuttons)
                except:
                    pass
        # If the message type is not a callback, run regular message handling
        else:
            text = msg['text'].split()
            if len(text) > 1:
                # Check if the parameter passed is a number, meaning it's a team
                if text[1].isdigit():
                    team = tba3.Team(text[1])
                    # Generate Initial Team Keyboard with Team Number in Callback Data
                    teambuttons = json.dumps({'inline_keyboard':[
                        [
                            {'text': 'Nickname', 'callback_data': 'team_nickname_' + team.team_number},
                            {'text': 'Motto', 'callback_data': 'team_motto_' + team.team_number},
                            {'text': 'Name', 'callback_data': 'team_name_' + team.team_number}],
                        [
                            {'text': 'Rookie Year', 'callback_data': 'team_rookie_year_' + team.team_number},
                            {'text': 'Website', 'callback_data': 'team_website_' + team.team_number},
                            {'text': 'Champs', 'callback_data': 'team_home_championship_' + team.team_number}],
                        [
                            {'text': 'Address', 'callback_data': 'team_address_' + team.team_number},
                            {'text': 'City', 'callback_data': 'team_city_' + team.team_number},
                            {'text': 'State', 'callback_data': 'team_state_prov_' + team.team_number}],
                        [
                            {'text': 'ZIP Code', 'callback_data': 'team_postal_code_' + team.team_number},
                            {'text': 'Country', 'callback_data': 'team_country_' + team.team_number},
                            {'text': 'Coords', 'callback_data': 'team_coords_' + team.team_number}],
                        [
                            {'text': 'Maps Link', 'callback_data': 'team_gmaps_url_' + team.team_number},
                            {'text': 'Loc Name', 'callback_data': 'team_location_name_' + team.team_number},
                            {'text': 'Maps ID', 'callback_data': 'team_gmaps_place_id_' + team.team_number}]
                    ]})
                    self.bot.sendMessage(msg['chat']['id'], 'Click button below for team info', reply_markup=teambuttons)
                # Check if the parameter passed is a string, meaning it's an event
                else:
                    try:
                        event = tba3.Event(text[1])
                    
                        # Generate Initial Event Keyboard with Event Key in Callback Data
                        eventbuttons = json.dumps({'inline_keyboard':[
                            [
                                {'text': 'Short Name', 'callback_data': 'event_short_name_' + event.key},
                                {'text': 'Week', 'callback_data': 'event_week_' + event.key},
                                {'text': 'Name', 'callback_data': 'event_name_' + event.key}],
                            [
                                {'text': 'District', 'callback_data': 'event_district_' + event.key},
                                {'text': 'Website', 'callback_data': 'event_website_' + event.key},
                                {'text': 'Timezone', 'callback_data': 'event_timezone_' + event.key}],
                            [
                                {'text': 'Event Code', 'callback_data': 'event_event_code_' + event.key},
                                {'text': 'Event Type', 'callback_data': 'event_event_type_string_' + event.key},
                                {'text': 'Playoff Type', 'callback_data': 'event_playoff_type_string_' + event.key}],
                            [
                                {'text': 'Address', 'callback_data': 'event_address_' + event.key},
                                {'text': 'City', 'callback_data': 'event_city_' + event.key},
                                {'text': 'State', 'callback_data': 'event_state_prov_' + event.key}],
                            [
                                {'text': 'ZIP Code', 'callback_data': 'event_postal_code_' + event.key},
                                {'text': 'Country', 'callback_data': 'event_country_' + event.key},
                                {'text': 'Coords', 'callback_data': 'event_coords_' + event.key}],
                            [
                                {'text': 'Maps Link', 'callback_data': 'event_gmaps_url_' + event.key},
                                {'text': 'Loc Name', 'callback_data': 'event_location_name_' + event.key},
                                {'text': 'Date', 'callback_data': 'event_date_' + event.key}]
                        ]})
                        self.bot.sendMessage(msg['chat']['id'], 'Click button below for event info', reply_markup=eventbuttons)
                    except:
                        pass
