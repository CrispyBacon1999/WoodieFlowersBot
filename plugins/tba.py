from plugins.pluginbase import PluginBase
from theblueallianceapi import *
import config
from imgurpython import ImgurClient


class Tba(PluginBase):
    def __init__(self, bot):
        self.bot = bot
        self.command = 'tba'
        self.command_level = 0
        self.help_mess = config.tba_help_mess

    def execute(self, msg):
        text = msg['text'].split()
        if len(text) >= 4:
            if text[1] == 'team':
                if len(text) < 5:
                    team = Team(text[3])
                else:
                    team = Team(text[3], year=text[4])
                if (text[2] == 'info'):
                    info = '*Information for Team %s:*\n\n*Name:* _%s_\n*Location:* _%s_\n*Motto:* _%s_\n*Website:* _%s_\n*Rookie Year:* _%s_' % (
                        text[3], team.info['name'], team.info['location'], team.info['motto'], team.info['website'],
                        team.info['rookie_year'])
                    self.bot.sendMessage(msg['chat']['id'], info, parse_mode='Markdown', disable_web_page_preview=True)
                elif (text[2] == 'pics'):
                    pics = ''
                    yespics = False
                    if not team.info['pics'] == []:
                        for pic in team.info['pics']:
                            yespic = False
                            print(pic)
                            if(pic['type'] == 'imgur'):
                                yespics = True
                                yespic = True
                                pics = 'i.' + 'imgur' + '.com/' + pic['foreign_key'] + '.jpg'
                            if(pic['type'] == 'cdphotothread'):
                                yespics = True
                                yespic = True
                                pics = 'chiefdelphi.com/media/img/' + pic['details']['image_partial']
                            if(yespic):
                                self.bot.sendPhoto(msg['chat']['id'], pics)
                    if not yespics:
                        self.bot.sendMessage(msg['chat']['id'], 'This team has no pictures.')
                elif (text[2] == 'vids'):
                    vids = ''
                    yesvids = False
                    for vid in team.info['pics']:
                        if(vid['type'] == 'youtube'):
                            yesvids = True
                            vids = 'youtube.com/watch?v=' + vid['foreign_key']
                        if(yesvids):
                            self.bot.sendMessage(msg['chat']['id'], vids, disable_web_page_preview=True)
                    if not yesvids:
                        self.bot.sendMessage(msg['chat']['id'], 'Team has no videos.')
                else:
                    self.bot.sendMessage(msg['chat']['id'], team.info[text[2]], parse_mode='Markdown')
            if text[1] == 'event':
                if len(text) < 5:
                    event = Event(str(text[3]))
                else:
                    event = Event(str(text[3]), year=text[4])
                if (str(text[2]) == 'teamstats'):
                    teamstats(event.info['key'])
                    self.bot.sendDocument(msg['chat']['id'],
                                          open('woodieV2.0/tmpeventstats/' + event.info['key'] + '.xls', 'rb'),
                                          reply_to_message_id=msg['message_id'])
                else:
                    self.bot.sendMessage(msg['chat']['id'], event.info[text[2]], parse_mode='Markdown')
            if text[1] == 'district':
                district = District(str(text[2]), str(text[3]))
                self.bot.sendMessage(msg['chat']['id'], district.events, parse_mode='Markdown')
        if text[1] == 'match':
            match = Match(str(text[2]), str(" ".join(text[3:7])))
            matchdata = '*Information for Match %d:*\n\n*Red:*\n  *Score:* _%s_\n  *Teams:* \n    _%s_\n    _%s_\n    _%s_\n\n*Blue:*\n  *Score:* _%s_\n  *Teams:*\n    _%s_\n    _%s_\n    _%s_' % (
                match.info['match_num'], match.info['score']['red'], match.info['teams']['red'][0],
                match.info['teams']['red'][1], match.info['teams']['red'][2], match.info['score']['blue'],
                match.info['teams']['blue'][0], match.info['teams']['blue'][1], match.info['teams']['blue'][2])
            self.bot.sendMessage(msg['chat']['id'], matchdata, parse_mode="Markdown")


import requests, json
import os
import xlwt

tbakey = 'frc-global:chatbot:2.0'
TBA_URL_BASE = 'https://www.thebluealliance.com/api/v2/%s/%s?X-TBA-App-Id=%s'

matchreq = 'https://www.thebluealliance.com/api/v2/team/%s/event/%s/matches?X-TBA-App-Id=%s' % ('%s', '%s', tbakey)


def teamstats(event):
    scoutingevent = event
    teams = json.loads(requests.get(TBA_URL_BASE % ('event/' + scoutingevent, 'teams', tbakey)).text)
    book = xlwt.Workbook()
    for team in teams:
        print('Current Team: ' + str(team['team_number']))
        eventreq = requests.get(TBA_URL_BASE % ('team/' + team['key'] + '/2017', 'events', tbakey))
        events = json.loads(eventreq.text)
        mobility = []
        autoFuelHigh = []
        autoRotors = []
        match_nums = []
        teleopFuelHigh = []
        teleopFuelLow = []
        teleopRotorPoints = []
        teleopTakeoffPoints = []
        for event in events:
            req = requests.get(matchreq % (team['key'], event['key']))
            matches = json.loads(req.text)

            # print(matches)
            for match in matches:
                # Check Alliance
                if team['key'] in match['alliances']['blue']['teams']:
                    alliance = 'blue'
                elif team['key'] in match['alliances']['red']['teams']:
                    alliance = 'red'
                else:
                    continue
                try:
                    all_brkd = match['score_breakdown'][alliance]
                    match_nums.append(match['match_number'])
                    autoFuelHigh.append(all_brkd['autoFuelHigh'])
                    autoRotors.append(all_brkd['autoRotorPoints'])
                    mobility.append(all_brkd['autoPoints'] - all_brkd['autoFuelHigh'] - all_brkd['autoRotorPoints'])

                    teleopFuelHigh.append(all_brkd['teleopFuelHigh'] / 3)
                    teleopFuelLow.append(all_brkd['teleopFuelLow'] / 9)
                    teleopRotorPoints.append(all_brkd['teleopRotorPoints'])
                    teleopTakeoffPoints.append(all_brkd['teleopTakeoffPoints'])
                except:
                    pass

        sh = book.add_sheet(str(team['team_number']))
        row_captions = ["Match Num", "Auto High Fuel", "Auto Rotor Points", "Auto Mobility", "Teleop High Fuel",
                        "Teleop Low Fuel",
                        "Teleop Rotor Points", "Climb Points"]
        for num, cap in enumerate(row_captions):
            sh.write(0, num, label=cap)
        for num, match in enumerate(match_nums):
            num = num + 1
            sh.write(num, 0, label=match_nums[num - 1])
            sh.write(num, 1, label=autoFuelHigh[num - 1])
            sh.write(num, 2, label=autoRotors[num - 1])
            sh.write(num, 3, label=mobility[num - 1])
            sh.write(num, 4, label=teleopFuelHigh[num - 1])
            sh.write(num, 5, label=teleopFuelLow[num - 1])
            sh.write(num, 6, label=teleopRotorPoints[num - 1])
            sh.write(num, 7, label=teleopTakeoffPoints[num - 1])
    book.save('woodieV2.0/tmpeventstats/' + scoutingevent + '.xls')
