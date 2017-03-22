import requests
import json
import datetime
import re

# EX: woodie_flowers:match_scraper:5
tbakey = 'frc-global:chatbot:2.0'


_TBA_URL_BASE = 'https://www.thebluealliance.com/api/v2/%s/%s?X-TBA-App-Id=%s'
# Team Requests
class Team():
    def __init__(self, num, year=None):
        self.teamnumber = num
        # If year isn't input, set it to current year
        if not year:
            self.year = datetime.date.today().year
        else:
            self.year = year
        data = self._retrieve_team_data()
        teamevents = '*Event List for %s*\n' % data['nickname']
        for event in self._retrieve_team_events():
            teamevents += '*' + event['short_name'] + '*: _' + event['event_code'] + '_\n'
        pics = self._retrieve_team_pics()
        self.info = {
            'school'       :  data['name'], 
            'location'     :  data['location'], 
            'name'         :  data['nickname'],
            'website'      :  data['website'],
            'rookie_year'  :  data['rookie_year'],
            'motto'        :  data['motto'],
            'events'       :  teamevents,
            'pics'         :  pics
        }
        if self.info['website'] == 'http://www.firstinspires.org/':
            self.info['website'] = 'No website set'
            
    def _retrieve_team_data(self):
        data = requests.get(_TBA_URL_BASE % ('team', 'frc' + str(self.teamnumber), tbakey))
        return json.loads(data.text)
    def _retrieve_team_events(self):
        data = requests.get(_TBA_URL_BASE % ('team', 'frc' + str(self.teamnumber) + '/'+ str(self.year) +'/events', tbakey))
        return json.loads(data.text)
    def _retrieve_team_pics(self):
        data = requests.get(_TBA_URL_BASE % ('team', 'frc' + str(self.teamnumber) + '/' + str(self.year) + '/media', tbakey))
        return json.loads(data.text)
# Event Requests
class Event():
    def __init__(self, code, year=None):
        self.event_year = year
        self.event_code = code
        if not year:
            self.year = datetime.date.today().year
        else:
            self.year = year
        data = self._retrieve_event_data()
        print(data)
        streams = ''
        for stream in data['webcast']:
            streams += 'twitch.tv/%s\n' % stream['channel']
        self.info= {
            'name'         :  data['name'], 
            'location'     :  data['location'], 
            'address'      :  data['venue_address'],
            'website'      :  data['website'],
            'start_date'   :  data['start_date'],
            'stream'       :  streams,
            'key'          :  data['key']
        }
        if self.info['website'] == 'http://www.firstinspires.org/':
            self.info['website'] = 'No website set'

                
    def _retrieve_event_data(self):
        data = requests.get(_TBA_URL_BASE % ('event', str(self.event_year) + str(self.event_code), tbakey))
        return json.loads(data.text)


# Match Requests
class Match():
    def __init__(self, event, match, year=None):
        if not year:
            self.year = datetime.date.today().year
        else:
            self.year = year
        self.event = event
        
        newmatch = re.sub('Qf{0}(ual)?(ification)? ?\d* ?', 'q', match, flags=re.IGNORECASE)
        newmatch = re.sub('Q(uarter)?f(inal)?s? ?', 'qf', newmatch, flags=re.IGNORECASE)
        newmatch = re.sub(' ?M(atch)? ?','m', newmatch, flags=re.IGNORECASE)
        
        self.match = newmatch
        print(newmatch)
        self.data = self._retrieve_match()
        print(json.dumps(self.data, indent=4, sort_keys=True))
        
        self.info = {
            'teams' :{
                'red': self.data['alliances']['red']['teams'],
                'blue': self.data['alliances']['blue']['teams']
            },
            'score':{
                'red': self.data['alliances']['red']['score'],
                'blue': self.data['alliances']['blue']['score']
            },
            'match_num':self.data['match_number'],
        }
    def _retrieve_match(self):
        data = requests.get(_TBA_URL_BASE % ('match', str(self.year) + self.event + '_' + self.match, tbakey))
        return json.loads(data.text)
        

# District Requests
class District():
    
    def __init__(self, district, year):
        self.districts = [
        'fim',
        'mar',
        'ne',
        'pnw',
        'in',
        'chs',
        'nc',
        'pch',
        'ont',
        'isr'
        ]
        
        self.district_code = district
        self.district_year = year
        if(self.districts.count(self.district_code) == 0):
            print('Invalid District')
        data = self._retrieve_district_events()
        self.events = ''
        for event in data:
            print(event['name'] + ': ' + event['event_code'])
            self.events = self.events + event['name'] + ': ' + event['event_code'] + '\n'
            
        
    def _retrieve_district_events(self):
        data = requests.get(_TBA_URL_BASE % ('district', str(self.district_code) + '/' + str(self.district_year) + '/events', tbakey))
        return json.loads(data.text)
        
        
        
def isintable(value):
  try:
    int(value)
    return True
  except:
    return False
    