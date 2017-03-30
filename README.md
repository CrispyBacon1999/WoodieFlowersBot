# Woodie Flowers Bot
This is a bot created for the telegram group [@FRCGlobal](https://t.me/FRCGlobal). It has commands that are used to access [The Blue Alliance](https://thebluealliance.com) so users can quickly share information with others. The bot can be accessed at [@FRCGlobalAdminbot](https://t.me/FRCGlobalAdminBot)
## Plugins

### Tba

References [The Blue Alliance](https://thebluealliance.com)'s [API](https://www.thebluealliance.com/apidocs) to give information on teams, events, districts, or matches.


#### Team Information
All information from teams can be retrieved using the prefix `/tba team` and has an optional suffix for the year. Defaults to current year.
* `/tba team info 254`: A clean list of most team information.
* `/tba team name 254`: The current name of the team.
* `/tba team location 254`: The city that the team is based out of.
* `/tba team motto 254`: The motto that a team has set.
* `/tba team website 254`: The team's website.
* `/tba team school 254`: The team's school and or sponsors.
* `/tba team rookie_year 254`: The rookie year of the team.
* `/tba team events 254`: The events that the team is going to.
* `/tba team pics 254`: Team pictures uploaded to [The Blue Alliance](https://thebluealliance.com)
* `/tba team vids 254`: Team videos uploaded to [The Blue Alliance](https://thebluealliance.com)

#### Event Information
All information about events can be retrieved using the prefix `/tba event`, requires the year suffix. Events should be retrieved using the event key without the year.
* `/tba event name cmpmo 2017`: The name of the event.
* `/tba event location cmpmo 2017`: The city the event takes place in.
* `/tba event address cmpmo 2017`: The address of the event. Useful for google maps.
* `/tba event website cmpmo 2017`: The website of the event. Most likely useful for regionals only.
* `/tba event start_date cmpmo 2017`: The start date of the event.
* `/tba event stream cmpmo 2017`: A list of livestreams.
* `/tba event key cmpmo 2017`: The full event key.

#### Match Information
Still a work in progress. Uses regular expressions to make match selection easier.
`/tba match cmpmo qf1m1`: Shows information from Quarterfinal 1 Match 1

Example Match Keys:
```
* qf1m1
* qm1
* sf2m1
* Qualification Match 1
* Qual Match 1
* Qual M1
* Quarterfinal 1 Match 2
* Quarterfs 4 M 3 
```
#### District Information
Still a work in progress. Use `/tba district fim 2017` for a list of all events within that district.

### Team
A feature specific to the [@FRCGlobal](https://t.me/FRCGlobal) chat. Allows for users in the chat to get quick information about users' teams.
* `/team set 254`: Sets the user's team number to whatever is input.
* `/team get @czvni`: Returns the team number that the user set prior.
* `/team list 254`: Lists all users on a specific team.

### Meetup
Compiles a list of all teams that are attending one or more of the same event as another. Currently shows each team twice, so the first column of teams will have your team if you share an event.
Simply run `/meetup`

## Admin Features

### Warn
Gives the replied to user X amounts of warnings. Only usable by group admins.
If the user reaches the set amount of warnings (default 3), they will be kicked.
Usage: `/warn X reason` or `/warn reason`.

### Kick
Instantly kicks the replied to user. They will be able to instantly rejoin with the group link.
Usage: `/kick reason`

### Ban
Instantly bans the replied to user. They will be unable to rejoin until unbanned by an administrator.
Usage: `/ban reason`
___





