import requests
import datetime
import json
import re
PREFIX = 'https://www.thebluealliance.com/api/v3/%s'
auth_key = '6mnUrR2iZZZ89TEez9f4CgTtC0nseG4V6QNufAFGhgd52KQoLhKOJbT7ijGsUvs0'

def _fetch(url):
    return json.loads(requests.get(PREFIX % url, headers={'X-TBA-Auth-Key': auth_key}).text)
    

class Team():
    def __init__(self, teamnumber, year=None, events=False, matches=False, media=False):
        if not year:
            year = datetime.date.today().year
        self.data = _fetch('team/frc' + teamnumber)
        self.rookie_year = self.data['rookie_year']
        self.address = self.data['address']
        self.city = self.data['city']
        self.state = self.data['state_prov']
        self.postal_code = self.data['postal_code']
        self.country = self.data['country']
        self.gmaps_url = self.data['gmaps_url']
        self.gmaps_place_id = self.data['gmaps_place_id']
        self.location_name = self.data['location_name']
        self.coords = (self.data['lat'], self.data['lng'])
        self.nickname = self.data['nickname']
        self.name = self.data['name']
        self.motto = self.data['motto']
        self.champs = self.data['home_championship']
        self.website = self.data['website']
        self.key = self.data['key']
        self.team_number = str(self.data['team_number'])
        if events:
            keys = _fetch('team/frc%s/events/%s/keys' % (teamnumber, year))
            comps = []
            for key in keys:
                comps.append(Event(key))

class Event():
    def __init__(self, eventkey, year=None, teams=False, matches=False, stats=False, awards=False, districtpoints=False):
        if not year:
            year = datetime.date.today().year
        eventkey = re.sub('\d{1,}', '', eventkey)
        self.data = _fetch('event/%s%s'% (year, eventkey))
        self.short_name = self.data['short_name']#
        self.coords = (self.data['lat'], self.data['lng'])#
        self.webcasts = self.data['webcasts']
        self.website = self.data['website']#
        self.key = self.data['key']
        self.division_keys = self.data['division_keys']
        self.state = self.data['state_prov']
        self.date = (self.data['start_date'], self.data['end_date'])
        self.address = self.data['address']#
        self.city = self.data['city']#
        self.state = self.data['state_prov']#
        self.postal_code = self.data['postal_code']#
        self.country = self.data['country']#
        self.gmaps_url = self.data['gmaps_url']#
        self.gmaps_place_id = self.data['gmaps_place_id']#
        self.location_name = self.data['location_name']#
        self.event_type = self.data['event_type']
        self.week = self.data['week']#
        self.name = self.data['name']#
        try:
            self.district = District(self.data['district']['abbreviation'])#
        except Exception:
            pass
        self.playoff_type_string = self.data['playoff_type_string']#
        self.playoff_type = self.data['playoff_type']
        self.event_code = self.data['event_code']#
        self.event_type_string = self.data['event_type_string']#
        self.timezone = self.data['timezone']#
        self.event_id = self.data['first_event_id']
        
class District():
    def __init__(self, districtcode):
        pass