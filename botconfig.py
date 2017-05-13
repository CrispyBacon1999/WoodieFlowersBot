from plugins import about, best, betatba, bind, configure, kick, meetup, rank, request, rules, say, scouting, sub, tba, team, warn

TOKEN = ''
VERSION = 'v3.0'
plugins = []


def init_plugins(bot):
    plugins = [
        about.About(bot),
        about.About(bot),
        best.Best(bot),
        betatba.Beta(bot),
        bind.Bind(bot),
        configure.Configure(bot),
        kick.Kick(bot),
        meetup.Meetups(bot),
        rank.Rank(bot),
        request.Request(bot),
        rules.Rules(bot),
        say.Say(bot),
        scouting.Scouting(bot),
        sub.Sub(bot),
        tba.Tba(bot),
        team.Team(bot),
        warn.Warn(bot)
    ]

# Database Information
database = {
    'link': 'woodie.db',
    'tables': {
        'teams': {
            'name': 'memberteams',
            'columns': ['uid', 'team']
        },
        'ranks': {
            'name': 'ranks',
            'columns': ['uid', 'rank']
        },
        'stickers': {
            'name': 'stickerbinds',
            'columns': ['sticker', 'command']
        },
        'xp': {
            'name': 'userxp',
            'columns': ['uid', 'xp']
        },
        'messages': {
            'name': 'messages',
            'columns': ['key', 'message']
        },
        'requests': {
            'name': 'requests',
            'columns': ['uid', 'request']
        },
        'usernames': {
            'name': 'usernames',
            'columns': ['username', 'uid']
        },
        'warns': {
            'name': 'warns',
            'columns': ['uid', 'num']
        }
    }
}
