import requests, json
import os
import xlwt

tbakey = 'frc-global:chatbot:2.0'
TBA_URL_BASE = 'https://www.thebluealliance.com/api/v2/%s/%s?X-TBA-App-Id=%s'

matchreq = 'https://www.thebluealliance.com/api/v2/team/%s/event/%s/matches?X-TBA-App-Id=%s' % ('%s', '%s', tbakey)

class Stats:
    def teamstats(event):
        scoutingevent = event
        os.mkdir(scoutingevent)
        teams = json.loads(requests.get(TBA_URL_BASE % ('event/' + scoutingevent, 'teams', tbakey)).text)
        book = xlwt.Workbook()
        for team in teams:
            print('Current Team: ' + str(team['team_number']))
            eventreq = requests.get(TBA_URL_BASE % ('team/'+team['key'] + '/2017', 'events',tbakey))
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
        
                #print(matches)
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
        
            
            sh = book.add_sheet(team['team_number'])
            row_captions = ["Match Num", "Auto High Fuel", "Auto Rotor Points", "Auto Mobility", "Teleop High Fuel", "Teleop Low Fuel",
                 "Teleop Rotor Points", "Climb Points"]
            for num, match in enumerate(match_nums):
                sh.write(num, 0, label=match_nums[num])
                sh.write(num, 1, label=autoFuelHigh[num])
                sh.write(num, 2, label=autoRotors[num])
                sh.write(num, 3, label=mobility[num])
                sh.write(num, 4, label=teleopFuelHigh[num])
                sh.write(num, 5, label=teleopFuelLow[num])
                sh.write(num, 6, label=teleopRotorPoints[num])
                sh.write(num, 7, label=teleopTakeoffPoints[num])
        book.save(event)
